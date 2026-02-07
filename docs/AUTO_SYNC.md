# 🔄 Sistema de Sync GitHub (Manual)

## 📋 **Resumen**
Sistema **manual** que sincroniza los cambios del dashboard de trading con GitHub cuando se solicita explícitamente. Eliminado el cron job automático para mayor control.

## 🏗️ **Arquitectura**

### **Componentes:**
1. **`scripts/auto_sync.py`** - Script principal Python (ejecución manual)
2. **`scripts/sync_now.sh`** - Wrapper Bash para ejecución manual
3. **GitHub Token** - Autenticación segura
4. **Comandos manuales** - Control total del usuario

### **Flujo de trabajo (MANUAL):**
```
[Tú o Paco actualiza datos] → [Ejecutas comando sync] → [Detección de cambios] → [Commit inteligente] → [Push a GitHub] → [GitHub Pages actualizado]
```

## ⚙️ **Configuración**

### **Token de GitHub:**
- **Tipo**: Personal Access Token (Classic)
- **Scopes**: `repo` (full control), `workflow`
- **Almacenamiento**: En remote URL de git (seguro para uso local)
- **Nombre**: `OpenClaw Auto-Sync - Trading Dashboard`

### **Modo operativo:**
- **Manual**: Solo se ejecuta cuando tú lo pides
- **Sin cron jobs**: Eliminado el ejecución automática
- **Control total**: Decides cuándo sincronizar

## 🚀 **Uso (EXCLUSIVAMENTE MANUAL)**

### **Opción 1: Desde terminal**
```bash
# Desde el directorio trading/
./scripts/sync_now.sh

# O directamente
python3 scripts/auto_sync.py
```

### **Opción 2: Desde OpenClaw (Paco)**
```python
# Cuando actualizo datos y tú me pides "sube a GitHub"
exec("cd /home/fran/.openclaw/workspace/trading && ./scripts/sync_now.sh")
```

### **Opciones del script:**
```bash
# Sync normal (detecta cambios y hace commit+push)
python3 scripts/auto_sync.py

# Configurar cron job automático (NO RECOMENDADO)
python3 scripts/auto_sync.py --setup-cron

# Eliminar cron job automático
python3 scripts/auto_sync.py --remove-cron

# Ayuda
python3 scripts/auto_sync.py --help
```

### **Cuándo ejecutar sync:**
- **Después de actualizar precios** (cuando pides "actualiza la web")
- **Después de modificar portfolio** (nuevas operaciones)
- **Después de actualizar análisis** (cambios en decisiones)
- **Cuando quieras backup** en GitHub

**⚠️ Sin ejecuciones automáticas** - tú controlas cuándo se sincroniza.

## 📊 **Mensajes de Commit Inteligentes**

El sistema analiza los archivos cambiados y genera mensajes como:

- **`Auto-sync 2026-02-07 18:38:01 | Precios actualizados`**
- **`Auto-sync 2026-02-07 18:45:00 | Portfolio modificado | Análisis actualizado`**
- **`Auto-sync 2026-02-07 19:00:00 | Documentación actualizada`**

## 📁 **Estructura de Archivos**

```
trading/
├── scripts/
│   ├── auto_sync.py      # Script principal Python
│   └── sync_now.sh       # Wrapper Bash
├── logs/
│   ├── sync.log          # Log del script principal
│   └── cron.log          # Historial de ejecuciones automáticas (vacío ahora)
└── docs/
    └── AUTO_SYNC.md      # Esta documentación
```

## 🔍 **Monitoreo y Logs**

### **Ver logs:**
```bash
# Logs del script manual
tail -f logs/sync.log

# Ver últimos commits
git log --oneline -10
```

### **Verificar estado:**
```bash
# Verificar que NO hay cron jobs (debe estar vacío)
crontab -l | grep -i "auto_sync" || echo "✅ Sin cron jobs automáticos"

# Verificar token configurado
git remote -v

# Verificar cambios pendientes
git status

# Verificar última actualización
curl -s "https://franruizlozano31-design.github.io/trading-dashboard/data/prices.json" | grep -o '"lastUpdate":"[^"]*"' | head -1
```

## 🛠️ **Mantenimiento**

### **Actualizar token:**
```bash
git remote set-url origin https://franruizlozano31-design:NUEVO_TOKEN@github.com/franruizlozano31-design/trading-dashboard.git
```

### **Gestionar cron job (OPCIONAL - no recomendado):**
```bash
# Activar automático (NO USAR a menos que quieras)
python3 scripts/auto_sync.py --setup-cron

# Desactivar automático
python3 scripts/auto_sync.py --remove-cron

# Verificar estado
crontab -l | grep -i "auto_sync" || echo "✅ Modo manual activado"
```

### **Debugging:**
```bash
# Ejecutar en modo verbose
python3 scripts/auto_sync.py

# Ver errores de git
git status
git log --oneline -5
```

## ⚠️ **Consideraciones de Seguridad**

### **Token:**
- Solo tiene acceso al repositorio `trading-dashboard`
- Almacenado localmente en remote URL
- No se incluye en commits
- Se puede revocar desde GitHub en cualquier momento

### **Archivos excluidos:**
- Ninguna clave API o información sensible se sube
- `.gitignore` previene subir archivos temporales
- Solo archivos de datos y código

## 🔗 **GitHub Pages**

### **URL:**
https://franruizlozano31-design.github.io/trading-dashboard/dashboard.html

### **Actualización:**
- Los cambios se reflejan en 1-2 minutos tras push
- GitHub Pages se actualiza automáticamente
- No requiere acción manual

## 📝 **Historial de Versiones**

### **v1.1 (2026-02-07) - MODO MANUAL**
- **Eliminado cron job automático** → solo ejecución manual
- **Control total del usuario** - tú decides cuándo sincronizar
- **Añadidas opciones** `--setup-cron`, `--remove-cron`, `--help`
- **Documentación actualizada** para reflejar modo manual

### **v1.0 (2026-02-07)**
- Sistema inicial de auto-sync
- Commit y push automáticos
- Cron job cada 5 minutos
- Mensajes de commit inteligentes
- Documentación completa