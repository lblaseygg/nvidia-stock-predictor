import pandas as pd
import numpy as np

class NvidiaTradingSignals:
    def __init__(self):
        pass

    def calculate_technical_indicators(self, df):
        """Calculate technical indicators for better decision making"""
        # Create a copy of the dataframe to avoid SettingWithCopyWarning
        df = df.copy()
        
        # Calculate moving averages
        df.loc[:, 'SMA_20'] = df['Close'].rolling(window=20).mean()
        df.loc[:, 'SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Calculate RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df.loc[:, 'RSI'] = 100 - (100 / (1 + rs))
        
        # Calculate MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df.loc[:, 'MACD'] = exp1 - exp2
        df.loc[:, 'Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        return df

    def generate_trading_signals(self, current_data, prediction):
        """Generate trading signals based on multiple factors"""
        # Calculate technical indicators
        df = self.calculate_technical_indicators(current_data)
        
        # Get the latest values
        latest = df.iloc[-1]
        
        # Initialize signal strength (0 to 100)
        signal_strength = 50
        
        # 1. Price Prediction Analysis
        current_price = latest['Close']
        predicted_price = prediction
        price_change_percent = ((predicted_price - current_price) / current_price) * 100
        
        if price_change_percent > 5:
            signal_strength += 15
        elif price_change_percent > 2:
            signal_strength += 10
        elif price_change_percent < -5:
            signal_strength -= 15
        elif price_change_percent < -2:
            signal_strength -= 10
            
        # 2. RSI Analysis
        if latest['RSI'] < 30:  # Oversold
            signal_strength += 10
        elif latest['RSI'] > 70:  # Overbought
            signal_strength -= 10
            
        # 3. Moving Average Analysis
        if latest['Close'] > latest['SMA_20'] and latest['SMA_20'] > latest['SMA_50']:
            signal_strength += 10  # Uptrend
        elif latest['Close'] < latest['SMA_20'] and latest['SMA_20'] < latest['SMA_50']:
            signal_strength -= 10  # Downtrend
            
        # 4. MACD Analysis
        if latest['MACD'] > latest['Signal_Line']:
            signal_strength += 5  # Bullish
        else:
            signal_strength -= 5  # Bearish
            
        # 5. Volume Analysis
        avg_volume = df['Volume'].rolling(window=20).mean().iloc[-1]
        if latest['Volume'] > avg_volume * 1.5:
            signal_strength += 5  # High volume
            
        # Generate final recommendation
        if signal_strength >= 70:
            recommendation = "STRONG BUY"
            confidence = "High"
        elif signal_strength >= 60:
            recommendation = "BUY"
            confidence = "Moderate"
        elif signal_strength <= 30:
            recommendation = "STRONG SELL"
            confidence = "High"
        elif signal_strength <= 40:
            recommendation = "SELL"
            confidence = "Moderate"
        else:
            recommendation = "HOLD"
            confidence = "Low"
            
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'signal_strength': signal_strength,
            'predicted_price': predicted_price,
            'current_price': current_price,
            'predicted_change_percent': price_change_percent
        } 