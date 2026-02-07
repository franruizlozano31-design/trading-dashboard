#!/usr/bin/env python3
"""
Script de auto-sync para GitHub.
Ejecuta automáticamente commit y push cuando detecta cambios.
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Configuración
TRADING_DIR = Path(__file__).parent.parent
LOG_FILE = TRADING_DIR / "logs" / "sync.log"
GIT_EXEC = "/usr/bin/git"

def setup_logging():
    """Configura directorio de logs si no existe."""
    log_dir = LOG_FILE.parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

def log_message(message):
    """Escribe mensaje en log y stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    
    print(log_entry)

def run_command(cmd, cwd=None):
    """Ejecuta comando shell y retorna resultado."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd or TRADING_DIR,
            capture_output=True, 
            text=True, 
            encoding="utf-8"
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def check_git_status():
    """Verifica si hay cambios pendientes."""
    returncode, stdout, stderr = run_command(f"{GIT_EXEC} status --porcelain")
    
    if returncode != 0:
        log_message(f"Error en git status: {stderr}")
        return []
    
    # Parsear output: lista de archivos cambiados
    changed_files = []
    for line in stdout.split("\n"):
        if line.strip():
            # Formato: " M file.txt" o "?? newfile.txt"
            status = line[:2].strip()
            filename = line[3:].strip()
            changed_files.append((status, filename))
    
    return changed_files

def generate_commit_message(changed_files):
    """Genera mensaje de commit inteligente basado en archivos cambiados."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Analizar tipos de archivos cambiados
    categories = {
        "prices": False,
        "portfolio": False,
        "analysis": False,
        "docs": False,
        "config": False
    }
    
    for status, filename in changed_files:
        if "prices.json" in filename:
            categories["prices"] = True
        elif "portfolio.json" in filename:
            categories["portfolio"] = True
        elif "analysis/" in filename:
            categories["analysis"] = True
        elif filename.endswith(".md"):
            categories["docs"] = True
        elif "config/" in filename or filename.endswith(".json"):
            categories["config"] = True
    
    # Construir mensaje
    message_parts = [f"Auto-sync {timestamp}"]
    
    if categories["prices"]:
        message_parts.append("Precios actualizados")
    if categories["portfolio"]:
        message_parts.append("Portfolio modificado")
    if categories["analysis"]:
        message_parts.append("Análisis actualizado")
    if categories["docs"]:
        message_parts.append("Documentación actualizada")
    if categories["config"]:
        message_parts.append("Configuración modificada")
    
    if len(message_parts) == 1:
        message_parts.append("Cambios varios")
    
    return " | ".join(message_parts)

def auto_commit_and_push():
    """Ejecuta commit y push automático si hay cambios."""
    log_message("=== Iniciando auto-sync ===")
    
    # Verificar cambios
    changed_files = check_git_status()
    
    if not changed_files:
        log_message("No hay cambios pendientes. Saliendo.")
        return True
    
    log_message(f"Encontrados {len(changed_files)} archivo(s) cambiado(s):")
    for status, filename in changed_files[:10]:  # Mostrar solo primeros 10
        log_message(f"  {status} {filename}")
    if len(changed_files) > 10:
        log_message(f"  ... y {len(changed_files) - 10} más")
    
    # Generar commit message
    commit_msg = generate_commit_message(changed_files)
    log_message(f"Mensaje de commit: {commit_msg}")
    
    # Agregar todos los cambios
    log_message("Agregando cambios...")
    returncode, stdout, stderr = run_command(f"{GIT_EXEC} add .")
    
    if returncode != 0:
        log_message(f"Error en git add: {stderr}")
        return False
    
    # Commit
    log_message("Haciendo commit...")
    returncode, stdout, stderr = run_command(f'{GIT_EXEC} commit -m "{commit_msg}"')
    
    if returncode != 0:
        # Posiblemente no hay cambios reales (solo whitespace)
        if "nothing to commit" in stderr.lower():
            log_message("Sin cambios reales para commit (solo whitespace?).")
            return True
        log_message(f"Error en git commit: {stderr}")
        return False
    
    log_message(f"Commit realizado: {stdout}")
    
    # Push
    log_message("Haciendo push a GitHub...")
    returncode, stdout, stderr = run_command(f"{GIT_EXEC} push origin main")
    
    if returncode != 0:
        log_message(f"Error en git push: {stderr}")
        return False
    
    log_message(f"Push exitoso: {stdout}")
    log_message("=== Auto-sync completado ===")
    return True

def setup_cron_job():
    """Configura cron job para ejecutar cada 5 minutos."""
    cron_line = "*/5 * * * * cd /home/fran/.openclaw/workspace/trading && /usr/bin/python3 scripts/auto_sync.py >> logs/cron.log 2>&1"
    
    # Verificar si ya está en crontab
    returncode, stdout, stderr = run_command("crontab -l", cwd=None)
    cron_content = stdout if returncode == 0 else ""
    
    if "auto_sync.py" not in cron_content:
        # Agregar al crontab
        new_cron = cron_content + "\n" + cron_line + "\n" if cron_content else cron_line + "\n"
        
        # Crear archivo temporal
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(new_cron)
            temp_file = f.name
        
        try:
            returncode, stdout, stderr = run_command(f"crontab {temp_file}", cwd=None)
            if returncode == 0:
                log_message("⚠️ Cron job configurado para ejecución cada 5 minutos (automático).")
                log_message("⚠️ Para eliminar: python3 scripts/auto_sync.py --remove-cron")
            else:
                log_message(f"Error configurando cron: {stderr}")
        finally:
            os.unlink(temp_file)
    else:
        log_message("Cron job ya está configurado.")

def remove_cron_job():
    """Elimina cron job del sistema."""
    log_message("=== Eliminando cron job ===")
    
    # Obtener crontab actual
    returncode, stdout, stderr = run_command("crontab -l", cwd=None)
    
    if returncode != 0:
        log_message("No hay cron jobs configurados.")
        return True
    
    # Filtrar línea de auto_sync
    lines = stdout.split("\n")
    new_lines = [line for line in lines if "auto_sync.py" not in line]
    
    if len(new_lines) == len(lines):
        log_message("No se encontró cron job para auto_sync.")
        return True
    
    # Crear nuevo crontab sin la línea
    new_cron = "\n".join(new_lines) + ("\n" if new_lines else "")
    
    # Guardar en archivo temporal
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(new_cron)
        temp_file = f.name
    
    try:
        returncode, stdout, stderr = run_command(f"crontab {temp_file}", cwd=None)
        if returncode == 0:
            log_message("✅ Cron job eliminado exitosamente.")
            log_message("   El sistema ahora funciona solo cuando se ejecuta manualmente.")
            return True
        else:
            log_message(f"❌ Error eliminando cron: {stderr}")
            return False
    finally:
        os.unlink(temp_file)

if __name__ == "__main__":
    setup_logging()
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup-cron":
            setup_cron_job()
        elif sys.argv[1] == "--remove-cron":
            remove_cron_job()
        elif sys.argv[1] == "--help":
            print("Uso: python3 auto_sync.py [OPCIÓN]")
            print()
            print("Opciones:")
            print("  (sin opciones)     Ejecuta sync manual si hay cambios")
            print("  --setup-cron       Configura cron job automático cada 5 min")
            print("  --remove-cron      Elimina cron job automático")
            print("  --help             Muestra esta ayuda")
        else:
            print(f"Opción desconocida: {sys.argv[1]}")
            print("Usa --help para ver opciones disponibles")
            sys.exit(1)
    else:
        success = auto_commit_and_push()
        sys.exit(0 if success else 1)