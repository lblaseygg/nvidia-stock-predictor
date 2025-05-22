import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import joblib
from model1 import train_model
import schedule
import time
import sys

def fetch_latest_data():
    """Fetch the latest NVIDIA stock data"""
    # Get data for the last 2 years to ensure enough data for training
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    # Fetch data from Yahoo Finance
    nvda = yf.Ticker("NVDA")
    df = nvda.history(start=start_date, end=end_date)
    
    # Reset index to make Date a column
    df = df.reset_index()
    
    # Save to CSV
    df.to_csv('NVDA_stock.csv', index=False)
    return df

def update_model():
    """Update the model with latest data"""
    try:
        print(f"\nUpdating model at {datetime.now()}")
        
        # Fetch latest data
        df = fetch_latest_data()
        
        # Train new model
        model = train_model(df)
        
        # Save updated model
        joblib.dump(model, 'nvidia_model.joblib')
        
        print("Model updated successfully!")
        sys.exit(0)  # Exit after successful update
        
    except Exception as e:
        print(f"Error updating model: {e}")
        sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    # Run initial update
    update_model()
