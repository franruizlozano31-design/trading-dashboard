#!/bin/bash
# Script para forzar sync inmediato
# Uso: ./sync_now.sh

cd "$(dirname "$0")/.."
python3 scripts/auto_sync.py

# Mostrar resultado
if [ $? -eq 0 ]; then
    echo "✅ Sync completado exitosamente"
else
    echo "❌ Error en sync"
    exit 1
fi