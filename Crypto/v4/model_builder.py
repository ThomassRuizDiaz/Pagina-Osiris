from keras.models import Sequential
from keras.layers import Dense, LSTM


def build_model(n_neurons, n_periods):
    model = Sequential()
    model.add(LSTM(units=n_neurons, return_sequences=True, input_shape=(n_periods, 1)))
    model.add(LSTM(units=n_neurons, return_sequences=True))
    model.add(LSTM(units=n_neurons))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model
