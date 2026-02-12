# 📋 PLAN DE IMPLEMENTACIÓN - ESTRATEGIA AGRESIVA

## 🎯 **ESTADO ACTUAL (12 Feb 2026)**

### **Sistema Base (YA CONSTRUIDO)**
✅ Dashboard de trading con GitHub Pages  
✅ Sistema modular de votación  
✅ Portfolio tracking en tiempo real  
✅ APIs configuradas (DeepSeek, Binance, CoinGecko)  
✅ Auto-sync a GitHub (manual, a petición)  
✅ Script de actualización automática (`update_and_sync.sh`)

### **Capital Inicial**
- **Total**: 100.07€
- **En BTC**: 50.32€ (posición abierta, -5.38% actual)
- **Disponible**: 49.75€
- **Fase**: Paper trading

---

## 🚀 **FASE 1: CONFIGURACIÓN AGRESIVA (HOY - DÍA 1)**

### **✅ COMPLETADO (12 Feb 18:25)**
1. **Estrategia documentada** (`strategies/aggressive_short_term.md`)
2. **Configuración modular agresiva** (`analysis/modular/config.json`)
3. **Watchlist ampliada** con activos volátiles (`config/watchlist.json`)
4. **Configuración de estrategia** (`config/aggressive_strategy.json`)
5. **Screener básico** (`scripts/aggressive_screener.py`)

### **🔄 EN PROGRESO**
1. **Backtesting rápido** (scripts a crear)
2. **Dashboard mejorado** (señales agresivas)
3. **Alertas Telegram** (integración)

### **📅 PRÓXIMOS PASOS (HOY/TARDE)**
1. **Ejecutar screener** para ver señales actuales
2. **Crear script de backtesting** rápido
3. **Actualizar dashboard** para mostrar estrategia agresiva
4. **Plan de paper trading intensivo** (20-30 operaciones)

---

## 🔧 **HERRAMIENTAS CREADAS**

### **1. Screener Agresivo (`aggressive_screener.py`)**
```bash
cd trading/
python3 scripts/aggressive_screener.py
```
- **Monitoriza**: 9 activos volátiles (BTC, ETH, SOL, XRP, ADA, DOT, AVAX, MATIC, AAVE)
- **Frecuencia**: Cada 30 segundos
- **Señales**: BUY (score >4), SELL (score <-3)
- **Stop-loss**: 1.5%, Take-profit: 4%
- **Salida**: JSON en `data/signals.json`

### **2. Configuración Modular Agresiva**
- **Pesos**: Técnico+Momentum 35%, Volumen 25%, Noticias 20%, Catalizadores 15%, Riesgo 5%
- **Umbrales**: BUY >4 (antes 6), SELL <-3 (antes -4)
- **Target**: 4% por operación, Stop-loss 1.5%

### **3. Watchlist Volátil**
- **Base**: BTC, ETH, SOL, XRP, ADA (alta volatilidad)
- **Screener**: DOT, AVAX, MATIC, AAVE
- **Criterios**: >3% cambio 24h, >50M€ volumen

---

## 📊 **PAPER TRADING INTENSIVO (DÍA 2-7)**

### **Objetivo**
- **20-30 operaciones** paper trading
- **Win rate objetivo**: >55%
- **Profit factor**: >1.5
- **Ajustar parámetros** basado en resultados

### **Metodología**
1. **Ejecutar screener** continuamente
2. **Registrar cada señal** en journal
3. **Simular ejecución** con reglas estrictas
4. **Revisar resultados** diariamente
5. **Ajustar estrategia** cada 10 operaciones

### **Reglas Paper Trading**
- **Tamaño posición**: 20-30€ (20-30% capital)
- **Máx. 3 operaciones** simultáneas
- **Stop-loss OBLIGATORIO** 1.5%
- **Take-profit** 4% (o trailing stop 2%)
- **Comisiones**: 0.5% Bit2Me (ida+vuelta 1%)

---

## 💰 **CAPITAL REAL PEQUEÑO (SEMANA 2)**

### **Condiciones para pasar a real**
1. **Win rate paper**: >55% (20+ operaciones)
2. **Profit factor**: >1.5
3. **Drawdown máximo**: <20%
4. **Consistencia**: No más de 2 pérdidas consecutivas

### **Plan Capital Real**
- **Capital inicial**: 50€ (mitad disponible)
- **Tamaño posición**: 10-15€ (20-30%)
- **Objetivo semanal**: +5% (2.50€)
- **Drawdown máximo aceptable**: 15% (7.50€)
- **Comisiones incluidas** en cálculos

### **Gestión Psicológica**
- **Máximo 2 operaciones** diarias al inicio
- **Revisar** cada operación win/loss
- **Parar** tras 2 pérdidas consecutivas
- **Celebrar** wins, analizar losses

---

## 📈 **ESCALADO (SEMANA 3-4)**

### **Condiciones para escalar**
1. **2 semanas positivas** con capital real
2. **Win rate mantenido**: >55%
3. **Drawdown controlado**: <15%
4. **Comodidad psicológica** con pérdidas

### **Plan de Escalado**
- **Aumentar posición** a 20-30€ (si capital >100€)
- **Añadir activos** (hasta 12 total)
- **Considerar swing trades** complementarios
- **Implementar automatización** parcial

---

## ⚠️ **GESTIÓN DE RIESGO (CRÍTICO)**

### **Reglas NO NEGOCIABLES**
1. **NUNCA más del 30%** en una operación
2. **SIEMPRE stop-loss** (automático o mental)
3. **Máximo 3 operaciones** abiertas
4. **Parar trading** tras 2 pérdidas consecutivas
5. **No revenge trading** (operar por emociones)

### **Límites Diarios**
- **Pérdida máxima**: 5% capital total (5€ con 100€)
- **Ganancia objetivo**: 2-3% diario (2-3€)
- **Operaciones máx.**: 5 por día
- **Horario**: Mercado cripto 24/7, pero descansar 8h

### **Comisiones y Costes**
```
Operación 30€ → Comisión 0.15€ entrada + 0.15€ salida = 0.30€ total
Para ser rentable necesita ganar >1% (0.30€) solo para cubrir comisiones
Objetivo 4% = 1.20€ ganancia neta (después comisiones)
```

---

## 🛠️ **PRÓXIMAS MEJORAS TÉCNICAS**

### **Prioridad ALTA (esta semana)**
- [ ] **Backtesting rápido** con datos históricos
- [ ] **Dashboard mejorado** con señales agresivas
- [ ] **Alertas Telegram** automáticas
- [ ] **Journal de trading** automatizado

### **Prioridad MEDIA (semanas 2-3)**
- [ ] **Automatización parcial** (ejecución semi-auto)
- [ ] **Análisis de sentimiento** (Twitter/Reddit)
- [ ] **Indicadores avanzados** (Fibonacci, Ichimoku)
- [ ] **Correlación entre activos**

### **Prioridad BAJA (mes 2)**
- [ ] **Machine learning** para predicción
- [ ] **Arbitraje** entre exchanges
- [ ] **Opciones/derivados** (si capital >500€)
- [ ] **Portfolio optimization**

---

## 📱 **COMUNICACIÓN Y SEGUIMIENTO**

### **Daily Check-ins**
- **Mañana**: Revisar mercado, oportunidades del día
- **Tarde**: Revisar operaciones, ajustar si necesario
- **Noche**: Resumen diario, preparar siguiente día

### **Seguimiento Semanal**
- **Lunes**: Plan semanal, objetivos
- **Viernes**: Review semanal, ajustes estratégicos
- **Domingo**: Análisis profundo, backtesting

### **Alertas y Notificaciones**
- **Telegram**: Señales BUY/SELL importantes
- **Dashboard**: Estado en tiempo real
- **GitHub Pages**: Datos actualizados cada sync

---

## 🎯 **OBJETIVOS POR ETAPAS**

### **Etapa 1 (Paper Trading - 1 semana)**
- ✅ Win rate >55%
- ✅ Profit factor >1.5
- ✅ 20+ operaciones registradas
- ✅ Sistema calibrado y confiable

### **Etapa 2 (Capital Pequeño - 2 semanas)**
- 🎯 Retorno semanal: +5%
- 🎯 Drawdown máximo: <15%
- 🎯 Consistencia psicológica
- 🎯 Sistema probado en real

### **Etapa 3 (Escalado - 1 mes)**
- 🚀 Retorno mensual: +20%
- 🚀 Capital >150€
- 🚀 Sistema semi-automatizado
- 🚀 Múltiples estrategias complementarias

### **Etapa 4 (Consolidación - 3 meses)**
- 💪 Retorno trimestral: +50-100%
- 💪 Capital >300€
- 💪 Sistema completamente probado
- 💪 Transición a trading semi-profesional

---

## 🚨 **CONTINGENCIAS Y PLAN B**

### **Si drawdown >20%**
1. **Reducir tamaño posición** a la mitad
2. **Enfocar solo en 2-3 activos** mejor conocidos
3. **Aumentar stop-loss** a 2% (menos operaciones, más seguras)
4. **Objetivo**: Recuperar 10% antes de escalar

### **Si 3 pérdidas consecutivas**
1. **Parar trading 24 horas**
2. **Analizar causas** (mercado, estrategia, ejecución)
3. **Ajustar parámetros** o cambiar activos
4. **Retomar** con tamaño reducido

### **Si ganancia rápida >30%**
1. **Retirar 20%** de ganancias (proteger capital)
2. **Operar con "house money"** (menos presión)
3. **No aumentar tamaño** por sobreconfianza
4. **Mantener disciplina** de riesgo

---

## 📝 **INICIO INMEDIATO**

### **PASO 1: Probemos el screener (AHORA)**
```bash
cd /home/fran/.openclaw/workspace/trading
python3 scripts/aggressive_screener.py
```
**Ejecutar por 5-10 minutos** para ver señales en mercado actual.

### **PASO 2: Revisar señales generadas**
```bash
cat data/signals.json
```

### **PASO 3: Planificar primera sesión paper trading**
- **Horario**: 1-2 horas esta tarde/noche
- **Objetivo**: 3-5 operaciones paper
- **Enfoque**: Seguir señales del screener
- **Registro**: Anotar cada operación en journal

### **PASO 4: Revisión mañana**
- **Analizar** operaciones de hoy
- **Ajustar** parámetros si necesario
- **Planificar** siguiente sesión

---

## 🤝 **COLABORACIÓN PACO-FRAN**

### **Mi rol (Paco)**
- **Desarrollo técnico** (scripts, dashboard, APIs)
- **Análisis de datos** y backtesting
- **Monitorización** continua del sistema
- **Alertas** y notificaciones
- **Soporte estratégico**

### **Tu rol (Fran)**
- **Ejecución** de operaciones (paper/real)
- **Gestión psicológica** y disciplina
- **Revisión crítica** de resultados
- **Toma de decisiones** finales
- **Aprendizaje continuo**

### **Comunicación**
- **Telegram**: Principal canal
- **Dashboard**: Estado en tiempo real
- **GitHub**: Código y documentación
- **Journal**: Registro de operaciones

---

**¿Listo para comenzar?** 🦅

Empecemos con el PASO 1: ejecutar el screener y ver qué señales genera en el mercado actual.