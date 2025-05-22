# NVIDIA Stock - Next-Day Closing Price Predictor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
df = pd.read_csv('NVDA_stock.csv')  # Replace with your CSV path

# 2. Clean Commas from Numbers
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace(',', '')
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. Clean Dates & Drop Nulls
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(inplace=True)
df = df.sort_values('Date')

# 4. Create Next-Day Target Column
df['Tomorrow_Close'] = df['Close'].shift(-1)
df.dropna(inplace=True)

# 5. Define Features and Labels
features = ['Open', 'High', 'Low', 'Volume']
target = 'Tomorrow_Close'

X = df[features]
y = df[target]

# 6. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Evaluate Model
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
r2 = r2_score(y_test, preds)

print(f"📊 Mean Squared Error: {mse:.2f}")
print(f"📈 R² Score: {r2:.2f}")

# 9. Predict Next-Day Closing Price
latest_input = df[features].iloc[-1].values.reshape(1, -1)
next_day_prediction = model.predict(latest_input)[0]
print(f"\n🔮 Predicted Close Price for Next Trading Day: ${next_day_prediction:.2f}")

# 10. Visualization: Actual vs Predicted
plt.figure(figsize=(14, 6))
sns.set_style("whitegrid")
plt.plot(y_test.values, label='📌 Actual Tomorrow Close', color='royalblue')
plt.plot(preds, label='✨ Predicted Tomorrow Close', color='orange', linestyle='--')

# Highlight the predicted next-day closing price
plt.scatter(len(preds), next_day_prediction, color='red', marker='*', s=200, label='🔮 Next Day Prediction')
plt.annotate(f"${next_day_prediction:.2f}",
             (len(preds), next_day_prediction),
             textcoords="offset points",
             xytext=(0,10),
             ha='center',
             color='red',
             fontsize=12,
             fontweight='bold')

plt.title("NVIDIA Stock — Tomorrow's Close Price Prediction", fontsize=15)
plt.xlabel("Test Sample Index")
plt.ylabel("Price (USD)")
plt.legend()
plt.tight_layout()
plt.show()
