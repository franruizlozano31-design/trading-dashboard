#!/usr/bin/env python3
"""
Screener agresivo para trading de corto plazo.
Monitorea activos volátiles y genera señales de entrada/salida rápida.
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys
from typing import Dict, List, Optional
import statistics

# Configuración
TRADING_DIR = Path(__file__).parent.parent
CONFIG_PATH = TRADING_DIR / "analysis" / "modular" / "config.json"
WATCHLIST_PATH = TRADING_DIR / "config" / "watchlist.json"
DATA_DIR = TRADING_DIR / "data"
LOG_FILE = TRADING_DIR / "logs" / "screener.log"

# APIs
BINANCE_BASE = "https://api.binance.com/api/v3"
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

class AggressiveScreener:
    def __init__(self):
        self.config = self.load_config()
        self.watchlist = self.load_watchlist()
        self.signals = []
        self.price_history = {}  # Para calcular volatilidad
        
    def load_config(self):
        """Cargar configuración modular agresiva."""
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_watchlist(self):
        """Cargar watchlist actual."""
        with open(WATCHLIST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def log_message(self, message: str):
        """Registrar mensaje en log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
        
        print(log_entry)
    
    async def fetch_price(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Obtener precio y datos de Binance."""
        try:
            # Para cripto en Binance (formato BTCEUR, ETHEUR, etc.)
            if symbol in ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'DOT', 'LINK', 'AVAX', 'MATIC', 'ATOM', 'UNI', 'AAVE']:
                ticker_url = f"{BINANCE_BASE}/ticker/24hr?symbol={symbol}EUR"
                async with session.get(ticker_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'symbol': symbol,
                            'price': float(data['lastPrice']),
                            'change24h': float(data['priceChangePercent']),
                            'volume': float(data['volume']),
                            'high24h': float(data['highPrice']),
                            'low24h': float(data['lowPrice'])
                        }
            
            # Para acciones (simulado por ahora)
            else:
                # Podríamos integrar Yahoo Finance o otra API
                return None
                
        except Exception as e:
            self.log_message(f"Error fetching {symbol}: {e}")
            return None
    
    def calculate_volatility(self, symbol: str, prices: List[float]) -> float:
        """Calcular volatilidad basada en precios recientes."""
        if len(prices) < 5:
            return 0.0
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
        
        if returns:
            return statistics.stdev(returns) * 100  # Volatilidad en %
        return 0.0
    
    def analyze_momentum(self, data: Dict) -> Dict:
        """Análisis de momentum para señales rápidas."""
        score = 0
        reasoning = []
        
        # 1. Cambio 24h (peso alto)
        change = data['change24h']
        if change > 8:
            score += 3
            reasoning.append(f"📈 Cambio 24h muy fuerte: +{change:.2f}%")
        elif change > 4:
            score += 2
            reasoning.append(f"📈 Cambio 24h fuerte: +{change:.2f}%")
        elif change > 2:
            score += 1
            reasoning.append(f"📈 Cambio 24h positivo: +{change:.2f}%")
        elif change < -4:
            score -= 2
            reasoning.append(f"📉 Cambio 24h negativo: {change:.2f}%")
        
        # 2. Volumen relativo (simulado)
        volume = data.get('volume', 0)
        if volume > 1000000:  # Alto volumen
            score += 1
            reasoning.append("💧 Volumen alto")
        
        # 3. Posición en rango 24h
        price = data['price']
        high = data['high24h']
        low = data['low24h']
        
        if high > low:  # Evitar división por cero
            position_in_range = (price - low) / (high - low)
            if position_in_range > 0.8:  # Cerca del máximo
                score -= 1
                reasoning.append(f"⚡ Cerca de máximo diario ({position_in_range*100:.0f}% del rango)")
            elif position_in_range < 0.2:  # Cerca del mínimo
                score += 1
                reasoning.append(f"📊 Cerca de mínimo diario ({position_in_range*100:.0f}% del rango)")
        
        # 4. Tendencias rápidas (simuladas)
        # En producción, usaríamos más datos históricos
        
        return {
            'score': score,
            'max_score': 5,
            'reasoning': " | ".join(reasoning) if reasoning else "Sin señales claras"
        }
    
    def generate_signal(self, symbol: str, analysis: Dict, data: Dict) -> Optional[Dict]:
        """Generar señal de trading basada en análisis."""
        score = analysis['score']
        
        # Umbrales del config agresivo
        buy_threshold = self.config['thresholds']['buy']  # 4
        sell_threshold = self.config['thresholds']['sell']  # -3
        
        if score >= buy_threshold:
            signal_type = "BUY"
            confidence = min(score / 10, 0.9)  # 0-0.9
        elif score <= sell_threshold:
            signal_type = "SELL"
            confidence = min(abs(score) / 10, 0.9)
        else:
            return None
        
        # Calcular stop-loss y take-profit basados en volatilidad
        price = data['price']
        change24h = abs(data['change24h'])
        
        # Stop-loss más ajustado para estrategia agresiva
        stop_loss_pct = 1.5  # 1.5% stop-loss
        take_profit_pct = 4.0  # 4% take-profit
        
        # Ajustar basado en volatilidad
        if change24h > 8:
            stop_loss_pct = 2.0
            take_profit_pct = 5.0
        
        stop_loss = price * (1 - stop_loss_pct/100) if signal_type == "BUY" else price * (1 + stop_loss_pct/100)
        take_profit = price * (1 + take_profit_pct/100) if signal_type == "BUY" else price * (1 - take_profit_pct/100)
        
        return {
            'symbol': symbol,
            'type': signal_type,
            'price': price,
            'confidence': confidence,
            'score': score,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'stop_loss_pct': stop_loss_pct,
            'take_profit_pct': take_profit_pct,
            'reasoning': analysis['reasoning'],
            'timestamp': datetime.now().isoformat()
        }
    
    async def screen_assets(self, assets: List[str]):
        """Analizar lista de activos."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for symbol in assets:
                tasks.append(self.fetch_price(session, symbol))
            
            results = await asyncio.gather(*tasks)
            
            for i, data in enumerate(results):
                if data is None:
                    continue
                
                symbol = assets[i]
                
                # Actualizar historial de precios
                if symbol not in self.price_history:
                    self.price_history[symbol] = []
                
                self.price_history[symbol].append(data['price'])
                if len(self.price_history[symbol]) > 20:  # Mantener últimos 20 precios
                    self.price_history[symbol].pop(0)
                
                # Análisis de momentum
                analysis = self.analyze_momentum(data)
                
                # Generar señal si aplica
                signal = self.generate_signal(symbol, analysis, data)
                
                if signal:
                    self.signals.append(signal)
                    self.log_message(f"🚨 SEÑAL {signal['type']} {symbol} @ {signal['price']:.2f}€ (Score: {signal['score']}, Conf: {signal['confidence']:.1%})")
                    self.log_message(f"   Reasoning: {signal['reasoning']}")
                    self.log_message(f"   SL: {signal['stop_loss']:.2f}€ ({signal['stop_loss_pct']:.1f}%) | TP: {signal['take_profit']:.2f}€ ({signal['take_profit_pct']:.1f}%)")
    
    def save_signals(self):
        """Guardar señales en archivo JSON."""
        signals_file = DATA_DIR / "signals.json"
        
        signals_data = {
            'lastUpdate': datetime.now().isoformat(),
            'totalSignals': len(self.signals),
            'signals': self.signals
        }
        
        with open(signals_file, 'w', encoding='utf-8') as f:
            json.dump(signals_data, f, indent=2)
        
        self.log_message(f"💾 Guardadas {len(self.signals)} señales en {signals_file}")
    
    async def run(self):
        """Ejecutar screener continuamente."""
        self.log_message("🚀 Iniciando screener agresivo de corto plazo")
        self.log_message(f"📊 Config: Buy >{self.config['thresholds']['buy']}, Sell <{self.config['thresholds']['sell']}")
        
        # Obtener activos a monitorizar
        assets = self.watchlist['currentActive']['total']
        self.log_message(f"👀 Monitorizando {len(assets)} activos: {', '.join(assets)}")
        
        try:
            while True:
                self.signals = []  # Resetear señales
                
                # Ejecutar screener
                await self.screen_assets(assets)
                
                # Guardar señales
                if self.signals:
                    self.save_signals()
                
                # Esperar antes de siguiente scan (30 segundos para tiempo real)
                self.log_message(f"⏳ Esperando 30 segundos para próximo scan...")
                await asyncio.sleep(30)
                
        except KeyboardInterrupt:
            self.log_message("👋 Screener detenido por usuario")
        except Exception as e:
            self.log_message(f"❌ Error en screener: {e}")

def main():
    """Función principal."""
    # Crear directorio de logs si no existe
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    screener = AggressiveScreener()
    
    try:
        asyncio.run(screener.run())
    except KeyboardInterrupt:
        print("\n✅ Screener detenido")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()