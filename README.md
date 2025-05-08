# NVIDIA Stock Price Predictor

A machine learning project that predicts NVIDIA stock prices using historical data and sentiment analysis from news articles.

## Project Overview

This project combines traditional stock price analysis with sentiment analysis from news articles to predict NVIDIA's stock price movements. The system uses multiple machine learning models and provides a web interface for visualization and predictions.

## Features

- Historical stock data analysis
- News article scraping and sentiment analysis
- Multiple ML models (Linear Regression, Random Forest/XGBoost, LSTM)
- Feature engineering with technical indicators
- Web interface for visualization
- Automated updates and model retraining

## Project Structure

```mermaid
graph TD
    A[Start Project] --> B[Load Historical NVIDIA Stock Data (CSV)]
    B --> C[Preprocess Data (clean, format dates, remove nulls)]
    C --> D[Feature Engineering (Lag features, MA5, MA10, etc.)]
    D --> E[Scrape NVIDIA News Articles]
    E --> F[Clean and Preprocess Text]
    F --> G[Perform Sentiment Analysis (VADER/TextBlob)]
    G --> H[Aggregate Daily Sentiment Scores]
    H --> I[Merge Sentiment Scores with Stock Data by Date]
    I --> J[Train Machine Learning Model]
    J --> K{Choose Model Type}
    
    K --> L1[Linear Regression]
    K --> L2[Random Forest / XGBoost]
    K --> L3[LSTM (Time-Series Deep Learning)]

    L1 --> M[Evaluate Model Performance]
    L2 --> M
    L3 --> M

    M --> N[Visualize Predictions and Sentiment Trends]
    N --> O[Deploy to Web App (Streamlit/Flask)]
    O --> P[Schedule Automatic Updates (Scraper + Model Re-train)]
    P --> Q[Done 🚀]
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nvidia-stock-predictor.git
cd nvidia-stock-predictor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Data Collection:
   - Historical stock data will be automatically downloaded
   - News articles will be scraped from configured sources

2. Model Training:
```bash
python train_model.py
```

3. Run the Web Interface:
```bash
python app.py
```

## Model Details

The project implements three different machine learning approaches:

1. **Linear Regression**: Baseline model for price prediction
2. **Random Forest/XGBoost**: Advanced ensemble methods for better accuracy
3. **LSTM**: Deep learning approach for time series prediction

## Data Sources

- Historical stock data from Yahoo Finance
- News articles from various financial news sources
- Technical indicators calculated from price data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- VADER and TextBlob for sentiment analysis
- Various financial data providers
- Open source machine learning libraries

## Contact

For questions or suggestions, please open an issue in the repository. 