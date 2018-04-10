#https://github.com/dashee87/blogScripts/blob/master/Jupyter/2017-11-20-predicting-cryptocurrency-prices-with-deep-learning.ipynb

import sys
import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model

# parsing inputs
def printUsage(): print "usage: python ", sys.argv[0], "-i inputdatafile.csv -o outputmodel.h5"
try:
	iflagidx = sys.argv.index('-i')
	inputfilename = sys.argv[iflagidx+1]
	oflagidx = sys.argv.index('-o')
	outputfilename = sys.argv[oflagidx+1]
except ValueError:
	printUsage()

''' Putting data into a dataframe '''
# slug,symbol,name,date,ranknow,open,high,low,close,volume,market,close_ratio,spread
all_data = pd.read_csv(inputfilename)
# make a new column turning date strings into numerical times,
# sort by name and time, then drop non-numerical attributes
all_data['time'] = all_data.apply(lambda t: time.mktime(datetime.strptime(t['date'], '%Y-%m-%d').timetuple()), axis=1)
all_data = all_data.sort_values(by=['name','time'])
all_data = all_data.drop(['slug','symbol','name','date','ranknow'], 1)

# per-row attribute modification
all_data['open_ratio'] = all_data['open']/all_data['high']
all_data['open_high_diff'] = all_data['close']-all_data['high']
all_data['close_high_diff'] = all_data['close']-all_data['high']

# make train test split: train on x% of data before a date, test on data after
train_percentage = .8
tpth_percentile_time = np.percentile(np.asarray(all_data['time']), train_percentage*100)
train_data, test_data = all_data[all_data['time']<tpth_percentile_time], all_data[all_data['time']>=tpth_percentile_time]
# drop time  column
train_data = train_data.drop('time',1)
test_data = test_data.drop('time',1)

''' creating windows of timeseries data '''
window_len = 10
cols_to_normalize = ['open','high','low','close','open_ratio','close_ratio',\
					 'open_high_diff','close_high_diff']

lstm_train_input = []
for i in range(len(train_data)-window_len):
	w = train_data[i:(i+window_len)].copy()
	# per-window attribute modification
	# normalize the specified columns to the value of the first entry
	# for col in cols_to_normalize:
	# 	w.loc[:,col] = w[col]/w[col].iloc[0]-1
	lstm_train_input.append(w)
lstm_train_output = \
  (train_data['open'][window_len:].values/train_data['open'][:-window_len].values)-1

lstm_test_input = []
for i in range(len(test_data)-window_len):
	w = test_data[i:(i+window_len)].copy()
	# for col in cols_to_normalize:
	# 	w.loc[:,col] = w[col]/w[col].iloc[0]-1
	lstm_test_input.append(w)
lstm_test_output = \
  (test_data['open'][window_len:].values/test_data['open'][:-window_len].values)-1

''' putting input windows into numpy arrays '''
lstm_train_input = [np.array(window) for window in lstm_train_input]
lstm_train_input = np.array(lstm_train_input)
lstm_test_input = [np.array(window) for window in lstm_test_input]
lstm_test_input = np.array(lstm_test_input)


def build_model(inputs, output_size, neurons, activ_func = "linear",
                dropout =0.25, loss="mae", optimizer="adam"):
    model = Sequential()

    model.add(LSTM(neurons, input_shape=(inputs.shape[1], inputs.shape[2])))
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))

    model.compile(loss=loss, optimizer=optimizer)
    return model

# build the model
m = build_model(lstm_train_input, output_size=1, neurons=20)
out = (train_data['open'][window_len:].values/train_data['open'][:-window_len].values)-1
hist = m.fit(lstm_train_input, lstm_train_output, epochs=10, batch_size=1, verbose=2, shuffle=True)

# save the model
m.save(outputfilename)