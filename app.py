from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_stock_data')
def stock_data():
    try:
        # Get stock data
        df = get_stock_data()
        
        # Get prediction data
        prediction_data = get_prediction()
        
        if prediction_data is None:
            raise Exception("Failed to get prediction data")
            
        return jsonify({
            'current_price': df['Close'].iloc[-1],
            'price_change_percentage_24h': ((df['Close'].iloc[-1] - df['Open'].iloc[0]) / df['Open'].iloc[0] * 100),
            'signal_strength': prediction_data['signal_strength'],
            'rsi': prediction_data['technical_indicators']['rsi'],
            'macd': prediction_data['technical_indicators']['macd'],
            'recommendation': prediction_data['recommendation'],
            'confidence': prediction_data['confidence'],
            'predicted_price': prediction_data['predicted_price'],
            'predicted_change': prediction_data['predicted_change_percent'],
            'prices': df['Close'].tolist(),
            'times': df.index.strftime('%H:%M').tolist()
        })
    except Exception as e:
        print(f"Error in stock_data route: {e}")
        return jsonify({
            'error': str(e)
        }), 500