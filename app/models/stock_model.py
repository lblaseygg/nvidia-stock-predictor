import yfinance as yf
import pandas as pd
import numpy as np
from .trading_signals import NvidiaTradingSignals

def get_stock_data():
    """Fetch latest NVIDIA stock data"""
    nvda = yf.Ticker("NVDA")
    df = nvda.history(period="1d", interval="1m")
    return df

def get_prediction():
    """Get latest prediction and trading signals"""
    try:
        # Get latest data
        df = get_stock_data()
        if df.empty:
            raise Exception("No stock data available")
            
        # Calculate a simple prediction based on recent trend
        recent_prices = df['Close'].tail(20)
        price_trend = recent_prices.pct_change().mean()
        current_price = df['Close'].iloc[-1]
        predicted_price = current_price * (1 + price_trend)
        
        # Get trading signals
        trading_advisor = NvidiaTradingSignals()
        signals = trading_advisor.generate_trading_signals(df, predicted_price)
        
        # Calculate technical indicators
        technical_indicators = calculate_technical_indicators(df)
        
        return {
            'current_price': current_price,
            'predicted_price': predicted_price,
            'recommendation': signals['recommendation'],
            'confidence': signals['confidence'],
            'signal_strength': signals['signal_strength'],
            'predicted_change_percent': ((predicted_price - current_price) / current_price) * 100,
            'technical_indicators': technical_indicators
        }
    except Exception as e:
        print(f"Error getting prediction: {e}")
        return None

def calculate_technical_indicators(data):
    """Calculate RSI and MACD"""
    try:
        # Calculate RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        # Calculate MACD
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = (exp1 - exp2).iloc[-1]
        
        return {
            'rsi': round(rsi, 2),
            'macd': round(macd, 2)
        }
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        return {
            'rsi': 0,
            'macd': 0
        }
