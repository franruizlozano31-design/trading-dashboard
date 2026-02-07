#!/bin/bash
# Script para actualizar precios, portfolio y hacer sync automático a GitHub
# Uso: ./update_and_sync.sh

set -e  # Salir en error

cd "$(dirname "$0")/.."

echo "🔄 Actualizando precios de mercado..."

# Obtener timestamp actual
TIMESTAMP=$(date -Iseconds)
echo "📅 Timestamp: $TIMESTAMP"

# Función para obtener precio de Binance
get_binance_price() {
    local symbol=$1
    local url="https://api.binance.com/api/v3/ticker/price?symbol=${symbol}"
    local price=$(curl -s "$url" | python3 -c "import sys, json; print(json.load(sys.stdin)['price'])" 2>/dev/null || echo "0")
    echo "$price"
}

# Función para obtener cambio 24h de Binance
get_binance_change() {
    local symbol=$1
    local url="https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol}"
    local change=$(curl -s "$url" | python3 -c "import sys, json; print(json.load(sys.stdin)['priceChangePercent'])" 2>/dev/null || echo "0")
    echo "$change"
}

# Obtener precios actuales
echo "📊 Obteniendo precios de Binance..."
BTC_PRICE=$(get_binance_price "BTCEUR")
ETH_PRICE=$(get_binance_price "ETHEUR")
SOL_PRICE=$(get_binance_price "SOLEUR")
LINK_PRICE=$(get_binance_price "LINKEUR")

# Obtener cambios 24h
BTC_CHANGE=$(get_binance_change "BTCEUR")
ETH_CHANGE=$(get_binance_change "ETHEUR")
SOL_CHANGE=$(get_binance_change "SOLEUR")
LINK_CHANGE=$(get_binance_change "LINKEUR")

# Obtener AAVE de CoinGecko
echo "📊 Obteniendo AAVE de CoinGecko..."
AAVE_PRICE=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=aave&vs_currencies=eur" | python3 -c "import sys, json; print(json.load(sys.stdin)['aave']['eur'])" 2>/dev/null || echo "0")
AAVE_CHANGE="0.0"  # CoinGecko no da cambio 24h fácilmente

echo "✅ Precios obtenidos:"
echo "   BTC:  €$BTC_PRICE ($BTC_CHANGE%)"
echo "   ETH:  €$ETH_PRICE ($ETH_CHANGE%)"
echo "   SOL:  €$SOL_PRICE ($SOL_CHANGE%)"
echo "   LINK: €$LINK_PRICE ($LINK_CHANGE%)"
echo "   AAVE: €$AAVE_PRICE"

# Actualizar prices.json
echo "📝 Actualizando prices.json..."
python3 -c "
import json
import sys

try:
    with open('data/prices.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Actualizar crypto
    data['lastUpdate'] = '$TIMESTAMP'
    data['crypto']['BTC']['eur'] = float('$BTC_PRICE')
    data['crypto']['BTC']['change24h'] = float('$BTC_CHANGE')
    data['crypto']['ETH']['eur'] = float('$ETH_PRICE')
    data['crypto']['ETH']['change24h'] = float('$ETH_CHANGE')
    data['crypto']['SOL']['eur'] = float('$SOL_PRICE')
    data['crypto']['SOL']['change24h'] = float('$SOL_CHANGE')
    data['crypto']['LINK']['eur'] = float('$LINK_PRICE')
    data['crypto']['LINK']['change24h'] = float('$LINK_CHANGE')
    data['crypto']['AAVE']['eur'] = float('$AAVE_PRICE')
    data['crypto']['AAVE']['change24h'] = float('$AAVE_CHANGE')
    
    # Mantener stocks igual (podrían actualizarse aquí si fuera necesario)
    data['stocks']['NVDA']['usd'] = 185.10
    data['stocks']['NVDA']['eur'] = 171.39
    data['stocks']['NVDA']['change'] = 7.22
    
    data['stocks']['TSLA']['usd'] = 411.50
    data['stocks']['TSLA']['eur'] = 380.93
    data['stocks']['TSLA']['change'] = 3.42
    
    with open('data/prices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print('✅ prices.json actualizado')
except Exception as e:
    print(f'❌ Error actualizando prices.json: {e}')
    sys.exit(1)
"

# Calcular P/L actual del portfolio
echo "🧮 Calculando P/L del portfolio..."
python3 -c "
import json
import sys

try:
    # Leer portfolio
    with open('data/portfolio.json', 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
    
    # Leer precios actualizados
    with open('data/prices.json', 'r', encoding='utf-8') as f:
        prices = json.load(f)
    
    # Actualizar posición BTC si existe
    if 'positions' in portfolio and len(portfolio['positions']) > 0:
        for pos in portfolio['positions']:
            if pos['symbol'] == 'BTC':
                # Obtener precio actual
                current_price = prices['crypto']['BTC']['eur']
                quantity = pos['quantity']
                entry_price = pos['entryPrice']
                entry_value = pos['entryValue']
                
                # Calcular valores actuales
                current_value = quantity * current_price
                profit_loss = current_value - entry_value
                profit_loss_pct = (profit_loss / entry_value) * 100
                
                # Actualizar posición
                pos['currentPrice'] = current_price
                pos['currentValue'] = current_value
                pos['profitLoss'] = profit_loss
                pos['profitLossPct'] = profit_loss_pct
                
                # Actualizar balance
                portfolio['balance']['invested'] = current_value
                portfolio['balance']['total'] = portfolio['balance']['available'] + current_value
                portfolio['balance']['totalWithGains'] = portfolio['balance']['total']
                
                # Actualizar stats
                portfolio['stats']['totalProfitLoss'] = profit_loss
                
                # Actualizar meta
                portfolio['meta']['lastSync'] = '$TIMESTAMP'
                
                print(f'💰 BTC: {quantity:.6f} @ €{entry_price:.0f}')
                print(f'   Valor actual: €{current_value:.2f}')
                print(f'   P/L: €{profit_loss:.2f} ({profit_loss_pct:.2f}%)')
                break
    
    # Guardar portfolio actualizado
    with open('data/portfolio.json', 'w', encoding='utf-8') as f:
        json.dump(portfolio, f, indent=2)
    
    print('✅ portfolio.json actualizado')
except Exception as e:
    print(f'❌ Error actualizando portfolio: {e}')
    sys.exit(1)
"

# Actualizar análisis BTC básico
echo "🧠 Actualizando análisis BTC..."
python3 -c "
import json
import sys

try:
    with open('analysis/modular/BTC.json', 'r', encoding='utf-8') as f:
        btc_data = json.load(f)
    
    with open('data/prices.json', 'r', encoding='utf-8') as f:
        prices = json.load(f)
    
    # Actualizar precio y cambio
    btc_data['lastUpdate'] = '$TIMESTAMP'
    btc_data['price'] = float('$BTC_PRICE')
    btc_data['change24h'] = float('$BTC_CHANGE')
    
    # Actualizar reasoning según precio
    btc_price = float('$BTC_PRICE')
    btc_change = float('$BTC_CHANGE')
    
    if btc_change < -2:
        btc_data['modules']['technical']['reasoning'] = f'BTC retrocedió {btc_change:.2f}% desde ayer. Pullback fuerte. Corto plazo bajista. Largo plazo alcista.'
        btc_data['modules']['momentum']['reasoning'] = f'Momentum negativo. Caída {btc_change:.2f}% en 24h. Volumen normal.'
        btc_data['modules']['momentum']['shortTerm']['roc_24h'] = btc_change
    elif btc_change < 0:
        btc_data['modules']['technical']['reasoning'] = f'BTC retrocedió {btc_change:.2f}% desde ayer. Leve corrección. Corto plazo neutral. Largo plazo alcista.'
        btc_data['modules']['momentum']['reasoning'] = f'Momentum negativo pero leve. Caída {btc_change:.2f}% en 24h.'
        btc_data['modules']['momentum']['shortTerm']['roc_24h'] = btc_change
    else:
        btc_data['modules']['technical']['reasoning'] = f'BTC subió {btc_change:.2f}% desde ayer. Recuperación en curso. Corto plazo alcista. Largo plazo alcista.'
        btc_data['modules']['momentum']['reasoning'] = f'Momentum positivo. Subida {btc_change:.2f}% en 24h.'
        btc_data['modules']['momentum']['shortTerm']['roc_24h'] = btc_change
    
    # Actualizar reasoning final
    portfolio_path = 'data/portfolio.json'
    with open(portfolio_path, 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
    
    if 'positions' in portfolio and len(portfolio['positions']) > 0:
        for pos in portfolio['positions']:
            if pos['symbol'] == 'BTC':
                pl_pct = pos['profitLossPct']
                pl_sign = '+' if pl_pct >= 0 else ''
                btc_data['reasoning'] = f'Score {btc_data[\"finalScore\"]:.2f}. BTC {btc_change:.2f}% desde ayer. Tu posición: {pl_sign}{pl_pct:.2f}% P/L.'
                break
    
    # Guardar
    with open('analysis/modular/BTC.json', 'w', encoding='utf-8') as f:
        json.dump(btc_data, f, indent=2)
    
    print('✅ BTC.json actualizado')
except Exception as e:
    print(f'⚠️ Error actualizando BTC.json: {e}')
    print('Continuando con sync...')
"

# Hacer sync a GitHub
echo "🚀 Haciendo sync automático a GitHub..."
./scripts/sync_now.sh

echo "🎉 ¡Actualización completa y sync realizado!"
echo "🌐 GitHub Pages se actualizará en 1-2 minutos:"
echo "   https://franruizlozano31-design.github.io/trading-dashboard/dashboard.html"