from flask import Blueprint, render_template, jsonify
from app.models.stock_model import get_stock_data, get_prediction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/api/stock-data')
def stock_data():
    try:
        df = get_stock_data()
        
        # Calculate 24h change
        current_price = float(df['Close'].iloc[-1])
        price_24h_ago = float(df['Close'].iloc[0])
        price_change_24h = current_price - price_24h_ago
        price_change_percentage_24h = (price_change_24h / price_24h_ago) * 100
        
        # Include volume for enhanced UI
        volume = int(df['Volume'].iloc[-1]) if 'Volume' in df.columns else 12500000
        
        # Include technical indicators
        return jsonify({
            'prices': df['Close'].tolist(),
            'times': df.index.strftime('%H:%M').tolist(),
            'current_price': current_price,
            'price_change_24h': price_change_24h,
            'price_change_percentage_24h': price_change_percentage_24h,
            'volume': volume,
            'technical_indicators': {
                'rsi': 62,  # Default values until calculation is implemented
                'macd': 0.67
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/prediction')
def prediction():
    try:
        result = get_prediction()
        if result is None:
            return jsonify({
                'error': 'Unable to generate prediction',
                'current_price': 0,
                'predicted_price': 0,
                'recommendation': 'N/A',
                'confidence': 'N/A',
                'signal_strength': 0,
                'predicted_change_percent': 0,
                'technical_indicators': {
                    'rsi': 0,
                    'macd': 0
                }
            }), 200
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'current_price': 0,
            'predicted_price': 0,
            'recommendation': 'N/A',
            'confidence': 'N/A',
            'signal_strength': 0,
            'predicted_change_percent': 0,
            'technical_indicators': {
                'rsi': 0,
                'macd': 0
            }
        }), 200

@main_bp.route('/api/prediction-data')
def prediction_data():
    """
    New endpoint to support the updated frontend that uses separate stock and prediction data
    """
    try:
        result = get_prediction()
        if result is None:
            return jsonify({
                'error': 'Unable to generate prediction',
                'predicted_price': 575.50,  # Default prediction value
                'confidence': 85,
                'recommendation': 'BUY'
            }), 200
            
        # Simplify the response for the new frontend
        return jsonify({
            'predicted_price': result.get('predicted_price', 575.50),
            'confidence': result.get('confidence', 85),
            'recommendation': result.get('recommendation', 'BUY')
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'predicted_price': 575.50,
            'confidence': 85,
            'recommendation': 'BUY'
        }), 200

@main_bp.route('/api/update-model', methods=['POST'])
def update_model():
    try:
        # Get the latest stock data
        df = get_stock_data()
        
        # Get prediction using existing function
        prediction_data = get_prediction()
        
        if prediction_data is None:
            return jsonify({
                'error': 'Unable to generate prediction'
            }), 500
            
        return jsonify(prediction_data)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500 