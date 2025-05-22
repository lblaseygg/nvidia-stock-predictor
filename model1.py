# NVIDIA Stock - Closing Price Predictor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from news_scraper import NvidiaNewsScraper

# Set the style for a professional look
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def train_model(df):
    """Train the model with the provided data"""
    # 2. Clean Commas from Numbers
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Clean Dates & Drop Nulls
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
    df.dropna(inplace=True)
    df = df.sort_values('Date')

    # Get news data
    news_scraper = NvidiaNewsScraper()
    news_df = news_scraper.get_all_news()
    
    # Create daily news features
    daily_news = news_df.groupby(news_df['published_at'].dt.date).size().reset_index()
    daily_news.columns = ['Date', 'news_count']
    daily_news['Date'] = pd.to_datetime(daily_news['Date'], utc=True)
    
    # Merge news data with stock data
    df = df.merge(daily_news, on='Date', how='left')
    df['news_count'] = df['news_count'].fillna(0)

    # 4. Set Target Column to Today's Close
    target = 'Close'

    # 5. Define Features and Labels
    features = ['Open', 'High', 'Low', 'Volume', 'news_count']
    X = df[features]
    y = df[target]

    # 6. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 7. Train Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, X_test, y_test, df

if __name__ == "__main__":
    # Load data
    df = pd.read_csv('NVDA_stock.csv')
    
    # Train model
    model, X_test, y_test, df = train_model(df)
    
    # Save model
    joblib.dump(model, 'nvidia_model.joblib')
    
    # Make predictions
    preds = model.predict(X_test)
    
    # Calculate error for statistics
    error = np.abs(y_test.values - preds)
    
    # Initialize trading signals
    from trading_signals import NvidiaTradingSignals
    trading_advisor = NvidiaTradingSignals()
    
    # Get the latest data for analysis
    latest_data = df.tail(100)
    
    # Generate trading signals
    signals = trading_advisor.generate_trading_signals(latest_data, preds[-1])
    
    # Print trading advice
    trading_advisor.print_trading_advice(signals)
    
    # Print statistics
    print("\nDetailed Statistics:")
    print(f"Average Prediction Error: ${np.mean(error):.2f}")
    print(f"Maximum Prediction Error: ${np.max(error):.2f}")
    print(f"Minimum Prediction Error: ${np.min(error):.2f}")
    print(f"Standard Deviation of Error: ${np.std(error):.2f}")

# Add after loading the stock data
news_df = pd.read_csv('nvidia_news.csv')
news_df['published_at'] = pd.to_datetime(news_df['published_at'])

# Create daily news features
daily_news = news_df.groupby(news_df['published_at'].dt.date).size().reset_index()
daily_news.columns = ['Date', 'news_count']
daily_news['Date'] = pd.to_datetime(daily_news['Date'])  # Convert to datetime

# Comment out or remove the visualization code
"""
# 9. Enhanced Visualization for LinkedIn
fig = plt.figure(figsize=(12, 12))  # Increased height for better spacing
gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.5)  # Increased spacing

# Plot 1: Price Prediction
ax1 = fig.add_subplot(gs[0])
ax1.plot(y_test.values, label='Actual Price', color='#1f77b4', linewidth=2.5)
ax1.plot(preds, label='Predicted Price', color='#ff7f0e', linewidth=2.5)

# Add error bands
error = np.abs(y_test.values - preds)
ax1.fill_between(range(len(preds)), 
                 preds - error, 
                 preds + error, 
                 alpha=0.1, 
                 color='#ff7f0e', 
                 label='Error Range')

# Customize first subplot
ax1.set_title("Price Prediction Performance", fontsize=16, pad=30, fontweight='bold')
ax1.set_ylabel("Price (USD)", fontsize=12, fontweight='bold', labelpad=10)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='both', which='major', labelsize=10)

# Move legend to upper right with better styling
ax1.legend(fontsize=10, loc='upper right', framealpha=0.9, 
          edgecolor='gray', fancybox=True, bbox_to_anchor=(1, 1))

# Add statistics box to upper left with improved styling
stats_text = f'''
Model Performance Metrics:
• MSE: ${mse:.2f}
• R² Score: {r2:.2f}
• Avg Error: ${np.mean(error):.2f}
• Max Error: ${np.max(error):.2f}
'''
ax1.text(0.02, 0.98, stats_text,
         transform=ax1.transAxes,
         verticalalignment='top',
         fontsize=10,
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, 
                  edgecolor='gray', pad=0.5))

# Plot 2: Error Distribution
ax2 = fig.add_subplot(gs[1])
sns.histplot(error, ax=ax2, color='#1f77b4', bins=30, kde=True)
ax2.set_title("Prediction Error Distribution", fontsize=16, pad=30, fontweight='bold')
ax2.set_xlabel("Absolute Error (USD)", fontsize=12, fontweight='bold', labelpad=10)
ax2.set_ylabel("Frequency", fontsize=12, fontweight='bold', labelpad=10)
ax2.tick_params(axis='both', which='major', labelsize=10)

# Add mean error line with improved styling
mean_error = np.mean(error)
ax2.axvline(mean_error, color='#ff7f0e', linestyle='--', linewidth=2,
            label=f'Mean Error: ${mean_error:.2f}')
ax2.legend(fontsize=10, framealpha=0.9, edgecolor='gray', fancybox=True)

# Add a subtle background color
fig.patch.set_facecolor('#f8f9fa')
ax1.set_facecolor('#ffffff')
ax2.set_facecolor('#ffffff')

# Adjust layout without using tight_layout
plt.subplots_adjust(top=0.95, hspace=0.5)

# Save the figure with high quality
plt.savefig('nvidia_prediction.png', dpi=300, bbox_inches='tight', 
            facecolor='#f8f9fa', pad_inches=0.5)
plt.show()
"""
