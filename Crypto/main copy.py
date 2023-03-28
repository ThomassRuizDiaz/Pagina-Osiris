import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

def get_crypto_data(crypto_symbol, time_interval):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart?vs_currency=usd&days={time_interval}"
    response = requests.get(url)
    prices = response.json()["prices"]
    prices_df = pd.DataFrame(prices, columns=["timestamp", "price"])
    prices_df["timestamp"] = pd.to_datetime(prices_df["timestamp"], unit="ms")
    prices_df.set_index("timestamp", inplace=True)
    return prices_df

def prepare_data(data, n_periods):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)
    x, y = [], []
    for i in range(n_periods, len(data)):
        x.append(data_scaled[i-n_periods:i, 0])
        y.append(data_scaled[i, 0])
    x, y = np.array(x), np.array(y)
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))
    return x, y, scaler

def build_model(n_neurons, n_periods):
    model = Sequential()
    model.add(LSTM(units=n_neurons, return_sequences=True, input_shape=(n_periods, 1)))
    model.add(LSTM(units=n_neurons, return_sequences=True))
    model.add(LSTM(units=n_neurons))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model

def train_model(model, x_train, y_train):
    model.fit(x_train, y_train, epochs=50, batch_size=32)

def run_crypto_predictor(crypto_symbol, n_periods=60, n_neurons=50, time_interval="30d"):
    # Obtener datos de la criptomoneda
    data = get_crypto_data(crypto_symbol, time_interval)

    # Preparar datos para el modelo
    x, y, scaler = prepare_data(data.values, n_periods)

    # Construir modelo
    model = build_model(n_neurons, n_periods)

    # Entrenar modelo
    train_model(model, x, y)

    # Realizar predicción
    last_n_periods = data.tail(n_periods).values
    last_n_periods_scaled = scaler.transform(last_n_periods)
    x_input = np.array(last_n_periods_scaled)
    x_input = np.reshape(x_input, (1, n_periods, 1))
    predicted_price = model.predict(x_input)
    predicted_price = scaler.inverse_transform(predicted_price)

    # Mostrar gráfica con predicción
    plt.plot(data)
    plt.plot(data.index[-1] + pd.Timedelta(1, "d"), predicted_price, 'ro')
    plt.show()

    # Guardar datos en archivo CSV
    data.to_csv(f"{crypto_symbol}_data.csv")

# Ejemplo de uso
run_crypto_predictor("bitcoin")