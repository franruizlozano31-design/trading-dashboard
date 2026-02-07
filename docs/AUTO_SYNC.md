# 🔄 Sistema de Auto-Sync GitHub

## 📋 **Resumen**
Sistema automático que sincroniza todos los cambios del dashboard de trading con GitHub cada 5 minutos y tras actualizaciones manuales.

## 🏗️ **Arquitectura**

### **Componentes:**
1. **`scripts/auto_sync.py`** - Script principal Python
2. **`scripts/sync_now.sh`** - Wrapper Bash para ejecución manual
3. **Cron job** - Ejecución automática cada 5 minutos
4. **GitHub Token** - Autenticación segura

### **Flujo de trabajo:**
```
[Cambios en archivos] → [Detección automática] → [Commit inteligente] → [Push a GitHub] → [GitHub Pages actualizado]
```

## ⚙️ **Configuración**

### **Token de GitHub:**
- **Tipo**: Personal Access Token (Classic)
- **Scopes**: `repo` (full control), `workflow`
- **Almacenamiento**: En remote URL de git (seguro para uso local)
- **Nombre**: `OpenClaw Auto-Sync - Trading Dashboard`

### **Cron Job:**
```bash
*/5 * * * * cd /home/fran/.openclaw/workspace/trading && /usr/bin/python3 scripts/auto_sync.py >> logs/cron.log 2>&1
```

## 🚀 **Uso**

### **Sync automático (cada 5 minutos):**
- Se ejecuta automáticamente vía cron
- Detecta cambios en cualquier archivo
- Genera mensajes de commit descriptivos
- Hace push a `main` branch

### **Sync manual inmediato:**
```bash
# Desde el directorio trading/
./scripts/sync_now.sh

# O directamente
python3 scripts/auto_sync.py
```

### **Desde OpenClaw (Paco):**
```python
# Después de actualizar datos
exec("cd /home/fran/.openclaw/workspace/trading && ./scripts/sync_now.sh")
```

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
│   └── cron.log          # Log del cron job
└── docs/
    └── AUTO_SYNC.md      # Esta documentación
```

## 🔍 **Monitoreo y Logs**

### **Ver logs:**
```bash
# Logs del script
tail -f logs/sync.log

# Logs del cron job
tail -f logs/cron.log

# Ver últimos commits
git log --oneline -10
```

### **Verificar estado:**
```bash
# Verificar cron job
crontab -l | grep auto_sync

# Verificar token configurado
git remote -v

# Verificar cambios pendientes
git status
```

## 🛠️ **Mantenimiento**

### **Actualizar token:**
```bash
git remote set-url origin https://franruizlozano31-design:NUEVO_TOKEN@github.com/franruizlozano31-design/trading-dashboard.git
```

### **Reconfigurar cron job:**
```bash
python3 scripts/auto_sync.py --setup-cron
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

### **v1.0 (2026-02-07)**
- Sistema inicial de auto-sync
- Commit y push automáticos
- Cron job cada 5 minutos
- Mensajes de commit inteligentes
- Documentación completa