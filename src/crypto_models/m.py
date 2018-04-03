# https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/

import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout

''' Putting data into a dataframe '''
# slug,symbol,name,date,ranknow,open,high,low,close,volume,market,close_ratio,spread
df = pd.read_csv('test_data/bitcoin.csv')
# make a new column turning date strings into numerical times
df['time'] = df.apply(lambda t: time.mktime(datetime.strptime(t['date'], '%Y-%m-%d').timetuple()), axis=1)
df = df.sort_values(by=['name','time'])
df = df[['open','high','low','close','volume','close_ratio','spread']] #,'time']] sorted by time, don't use in modeling?

''' moving from dataframe to numpy stuff '''
window_len = 10; windows = []
for i in range(len(df)-window_len):
	windows.append(df[i:(i+10)].copy())


# expects inputs to be a 3D dataframe
# first dimension - list of dataframes
# second dimension - list of currency data entries
# third dimension - list of values for an entry
def build_model(inputs, output_size, neurons, activ_func = "linear",
                dropout =0.25, loss="mae", optimizer="adam"):
    model = Sequential()

    model.add(LSTM(neurons, input_shape=(10,7)))#inputs.shape[1], inputs.shape[2])))
    model.add(Dropout(dropout))

    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))

    model.compile(loss=loss, optimizer=optimizer)
    return model

m = build_model(windows, output_size=1, neurons=20)
out = (windows['open'][window_len:].values/windows['open'][:-window_len].values)-1
hist = m.fit(templist, out, epochs=50, batch_size=1, verbose=2, shuffle=True)
