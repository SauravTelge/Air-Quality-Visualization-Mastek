# -*- coding: utf-8 -*-
"""AQV_LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nm91BACGtvrah4-stjpuROkPj5dGRbK1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import keras
import plotly.graph_objects as go

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle
data = pd.read_csv(r"/content/drive/MyDrive/AQV-7/datasets/city_hour.csv")

from google.colab import drive
drive.mount('/content/drive')

print(data.head())

data = data.dropna()
print(data.head())

X = data['AQI'].values
X = np.reshape(X, (-1,1))
date = data['Datetime'].values

split_percent = 0.80
split = int(split_percent*len(X))

X_train = X[:split]
X_test = X[split:]

date_train = data['Datetime'][:split]
date_test = data['Datetime'][split:]

print(len(X_train))
print(len(X_test))
print(len(date_train))

look_back = 10

train_generator = TimeseriesGenerator(X_train, X_train, length=look_back, batch_size=20)     
test_generator = TimeseriesGenerator(X_test, X_test, length=look_back, batch_size=1)

model = Sequential()
model.add(LSTM(10, activation='relu', input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

model.fit_generator(train_generator, epochs=6, verbose=2)

print(X_test)

prediction = model.predict_generator(test_generator)
print(prediction)

plt.plot(date_test[:100], X_test[:100] )
#plt.plot(prediction, date_test)
#plt.legend(["Test value"],["Predicted value"])
plt.show()

plt.plot(date_test[:100], prediction[:100])
#plt.plot(prediction, date_test)
#plt.legend(["Test value"],["Predicted value"])
plt.show()

X_train = X_train.reshape((-1))
X_test = X_test.reshape((-1))
prediction = prediction.reshape((-1))

trace1 = go.Scatter(
    x = date_train,
    y = X_train,
    mode = 'lines',
    name = 'Data'
)
trace2 = go.Scatter(
    x = date_test,
    y = prediction,
    mode = 'lines',
    name = 'Prediction'
)
trace3 = go.Scatter(
    x = date_test,
    y = X_test,
    mode='lines',
    name = 'Ground Truth'
)
layout = go.Layout(
    title = "AQI",
    xaxis = {'title' : "Date"},
    yaxis = {'title' : "AQI"}
)
fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
fig.show()

def predict(num_prediction, model):
    prediction_list = X_test[-look_back:]
    
    for _ in range(num_prediction):
        x = prediction_list[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = model.predict(x)[0][0]
        prediction_list = np.append(prediction_list, out)
    prediction_list = prediction_list[look_back-1:]
        
    return prediction_list
    
def predict_dates(num_prediction):
    last_date = date_test.values[-1]
    prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
    return prediction_dates

num_prediction = 30
forecast = predict(num_prediction, model)
forecast_dates = predict_dates(num_prediction)

forecast= forecast.reshape((-1))
X_test = X_test.reshape((-1))
trace1 = go.Scatter(
    x = date_test,
    y = X_test,
    mode = 'lines',
    name = 'Data'
)
trace2 = go.Scatter(
    x = forecast_dates,
    y = forecast,
    mode = 'lines',
    name = 'Prediction'
)
layout = go.Layout(
    title = "AQI",
    xaxis = {'title' : "Date"},
    yaxis = {'title' : "AQI"}
)
fig = go.Figure(data=[trace1, trace2], layout=layout)
fig.show()
pickle.dump(fig.show(),open('model.pkl','wb'))

model =pickle.load(open('model.pkl','rb'))
