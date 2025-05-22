@app.route('/api/update-model', methods=['POST'])
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

@app.route('/api/stock-data')
def stock_data():
    try:
        print("Fetching stock data...")
        df = get_stock_data()
        
        if df.empty:
            print("No data available")
            return jsonify({'error': 'No stock data available'}), 500
            
        print(f"Data shape: {df.shape}")
        print(f"First few rows:\n{df.head()}")
        
        # Calculate 24h change
        current_price = float(df['Close'].iloc[-1])
        price_24h_ago = float(df['Close'].iloc[0])
        price_change_24h = current_price - price_24h_ago
        price_change_percentage_24h = (price_change_24h / price_24h_ago) * 100
        
        print(f"Current price: {current_price}")
        print(f"24h ago price: {price_24h_ago}")
        print(f"Price change: {price_change_24h}")
        print(f"Price change percentage: {price_change_percentage_24h}")
        
        # Validate the calculated values
        if not all(isinstance(x, (int, float)) for x in [current_price, price_24h_ago, price_change_24h, price_change_percentage_24h]):
            raise Exception("Invalid calculated values")
        
        # Convert prices to float and ensure they're valid
        prices = [float(x) for x in df['Close'].tolist()]
        if not all(isinstance(x, (int, float)) and x > 0 for x in prices):
            raise Exception("Invalid price values in data")
        
        # Get volume data
        volume = int(df['Volume'].iloc[-1]) if 'Volume' in df.columns else 12500000
        
        response_data = {
            'prices': prices,
            'times': df.index.strftime('%I:%M %p').tolist(),
            'current_price': current_price,
            'price_change_24h': price_change_24h,
            'price_change_percentage_24h': price_change_percentage_24h,
            'volume': volume,
            'technical_indicators': {
                'rsi': 62,  # Default values until calculation is implemented
                'macd': 0.67
            }
        }
        
        print(f"Response data: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in stock_data endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_stock_data():
    """Fetch latest NVIDIA stock data"""
    try:
        print("Initializing yfinance Ticker...")
        nvda = yf.Ticker("NVDA")
        
        print("Fetching history...")
        df = nvda.history(period="1d", interval="1m")
        
        if df.empty:
            print("No data returned from yfinance")
            raise Exception("No stock data available")
            
        print(f"Raw data shape: {df.shape}")
        print(f"Raw data columns: {df.columns}")
        
        # Ensure we have valid numeric data
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df = df.dropna(subset=['Close'])
        
        if df.empty:
            print("No valid price data after cleaning")
            raise Exception("No valid price data available")
            
        # Additional validation
        if len(df) < 2:
            print("Insufficient data points")
            raise Exception("Insufficient data points for price change calculation")
            
        # Ensure the data is sorted by time
        df = df.sort_index()
        
        # Validate the last price
        last_price = df['Close'].iloc[-1]
        if not isinstance(last_price, (int, float)) or last_price <= 0:
            print(f"Invalid last price: {last_price}")
            raise Exception("Invalid price data")
            
        print(f"Cleaned data shape: {df.shape}")
        print(f"First few rows of cleaned data:\n{df.head()}")
        print(f"Last price: {last_price}")
        
        return df
        
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stock/<symbol>')
def stock_page(symbol):
    if symbol == 'NVDA':
        return render_template('index.html')
    return render_template('coming_soon.html', symbol=symbol) 