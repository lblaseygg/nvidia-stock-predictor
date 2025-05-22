# Trendly

Trendly is an AI-powered stock analysis platform that provides real-time insights and predictions for NVIDIA stock. The platform combines technical analysis, machine learning predictions, and real-time market data to help investors make informed decisions.

## Features

- **Real-time Stock Data**: Live NVIDIA stock data with price updates and volume information
- **Technical Analysis**: Comprehensive technical indicators including RSI, MACD, and more
- **AI Predictions**: Machine learning-based price predictions with confidence levels
- **Interactive Charts**: Dynamic visualization of stock data and predictions
- **Responsive Design**: Modern, mobile-friendly interface

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Analysis**: Pandas, NumPy
- **Machine Learning**: scikit-learn
- **Data Visualization**: Chart.js
- **Stock Data**: yfinance
- **Styling**: Custom CSS with modern design principles

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lblaseygg/trendly.git
   cd trendly
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your configuration:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

5. Run the application:
   ```bash
   python run.py
   ```

The application will be available at `http://127.0.0.1:5000`

## Project Structure

```
trendly/
├── app/
│   ├── models/         # ML models and data processing
│   ├── static/         # CSS, JavaScript, and assets
│   └── templates/      # HTML templates
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
└── run.py             # Application entry point
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Luis Feliciano - [LinkedIn](https://www.linkedin.com/in/luisfernandofeliciano/)

Project Link: [https://github.com/lblaseygg/trendly](https://github.com/lblaseygg/trendly) 