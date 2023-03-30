import numpy as np
from sklearn.preprocessing import MinMaxScaler

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
