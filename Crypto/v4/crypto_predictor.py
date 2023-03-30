import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from model_builder import build_model
from data_preparer import prepare_data
from data_fetcher import DataFetcher

# Cargar datos de mercado para entrenar el modelo
fetcher = DataFetcher()
symbols = ["BTC", "ETH", "LTC", "XRP", "BCH"]
data = fetcher.get_market_data(symbols)

# Preparar datos para entrenamiento
preparer = prepare_data(data)
df = preparer.prepare_data()

# Crear modelo y entrenarlo
builder = build_model(df)
model = builder.build_model()
print("Modelo creado y entrenado exitosamente.")

# Obtener datos más recientes para hacer la predicción
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - pd.Timedelta(days=30)).strftime('%Y-%m-%d')
data = fetcher.get_crypto_data(symbols, start_date, end_date)

# Preparar datos para predicción
preparer = prepare_data(data)
df = preparer.prepare_data()

# Hacer predicción
X_pred = df.drop(['Close'], axis=1)
y_pred = model.predict(X_pred)

# Mostrar predicción
for i in range(len(symbols)):
    print("Predicción para", symbols[i], "en 30 días: $", round(y_pred[i], 2))
