import requests

# Obtener información de las criptomonedas desde la API de Coingecko
crypto_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"
response = requests.get(crypto_url)
crypto_data = response.json()

# Entender los datos obtenidos (precio actual, precio maximo historico, precio historico en general)
for crypto in crypto_data:
    name = crypto['name']
    current_price = crypto['current_price']
    ath = crypto['ath']
    high_24h = crypto['high_24h']
    low_24h = crypto['low_24h']
    print(f"{name}:\nCurrent Price: {current_price}\nAll-Time High: {ath}\n24h High: {high_24h}\n24h Low: {low_24h}\n")

# Entrenar la App para predecir los precios
from sklearn.linear_model import LinearRegression
import numpy as np

# Obtener los datos de precios históricos de Bitcoin
btc_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365"
response = requests.get(btc_url)
btc_data = response.json()

# Crear una matriz de características para la regresión lineal
X = []
y = []
for i in range(len(btc_data['prices'])-30):
    X.append([i])
    y.append(btc_data['prices'][i][1])

# Entrenar el modelo
model = LinearRegression()
model.fit(X, y)

# Predecir el precio futuro de Bitcoin
prediction = model.predict([[len(btc_data['prices'])+1]])

# Mostrar el precio actual y la predicción de Bitcoin
btc_price = [crypto for crypto in crypto_data if crypto['id'] == 'bitcoin'][0]['current_price']
print(f"Bitcoin: {btc_price}")
print(f"Proxima prediccion de Bitcoin: {prediction[0]}")
