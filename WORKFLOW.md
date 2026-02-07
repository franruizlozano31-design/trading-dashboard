# 🔄 Workflow Multi-Modelo

## Modelos Configurados

| Modelo | ID | Uso | Coste |
|--------|-----|-----|-------|
| 🚀 **Fast** | `deepseek/deepseek-chat` | Precios, JSONs, tareas simples | Muy bajo |
| 🧠 **Analysis** | `groq/deepseek-r1-distill-llama-70b` | Análisis modular, razonamiento | Bajo |
| 🎯 **Critical** | `anthropic/claude-sonnet-4-20250514` | Decisiones críticas, verificación | Medio |

---

## Flujo: "Paco actualiza"

```
PASO 1: Fast (DeepSeek V3)
├── Fetch precios CoinGecko/Yahoo
├── Actualizar prices.json
└── Screener básico (filtros simples)

PASO 2: Analysis (Groq R1)
├── Análisis modular completo
├── Calcular scores (5 módulos)
├── Detectar divergencias corto/largo plazo
└── Generar recomendaciones

PASO 3: Critical (Claude) - SOLO SI:
├── Score > +5 (cerca de BUY)
├── Score < -3 (cerca de SELL)
└── Oportunidad detectada por screener
```

---

## Flujo: "Compra X"

```
PASO 1: Fast
└── Obtener precio actual

PASO 2: Analysis
├── Verificar análisis modular
├── Confirmar niveles entrada/stop
└── Calcular riesgo

PASO 3: Critical - SOLO SI:
├── Operación > 30€
└── O score en zona límite

PASO 4: Fast
└── Ejecutar y actualizar portfolio
```

---

## Comandos de Cambio de Modelo

```
/model deepseek/deepseek-chat          # Fast
/model groq/deepseek-r1-distill-llama-70b  # Analysis
/model anthropic/claude-sonnet-4-20250514  # Critical
```

---

## Estimación de Costes

| Acción | Modelos usados | Coste aprox |
|--------|----------------|-------------|
| Actualización simple | Fast | ~$0.001 |
| Actualización + análisis | Fast + Analysis | ~$0.005 |
| Decisión crítica | Fast + Analysis + Critical | ~$0.02 |
| Operación pequeña | Fast + Analysis | ~$0.005 |
| Operación grande | Todos | ~$0.03 |

---

## Notas

- **Por defecto**: Groq R1 (balance coste/capacidad)
- **Fast**: Para tareas repetitivas sin razonamiento
- **Critical**: Solo cuando hay dinero en juego real
