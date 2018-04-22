#https://github.com/dashee87/blogScripts/blob/master/Jupyter/2017-11-20-predicting-cryptocurrency-prices-with-deep-learning.ipynb

import sys
import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
import psycopg2

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model

WINDOW_LEN = 10

def normalize_window(window, columnNames):
	for col in columnNames:
			w.loc[:,col] = pw[col]/(w[col].iloc[0]+1) - 1

def main():
	# parsing inputs
	try:
		cflagidx = sys.argv.index('-c')
		currencyname = sys.argv[cflagidx+1]
		oflagidx = sys.argv.index('-o')
		outputfilename = sys.argv[oflagidx+1]
	except ValueError:
		# malformed command line arguments, print usage and exit
		print "usage: python ", sys.argv[0], "-c nameOfCurrency -o outputmodel.h5"
		exit()

	''' Stuff about our data for querying '''
	trainingAttributes = ['open', 'high', 'low', 'close', 'volumefrom', 'volumeto']

	''' SQL Query for Training Data '''
        conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
	cursor = conn.cursor()
	query = "SELECT " + ", ".join(trainingAttributes) + " FROM bitcoin"\
	        + " WHERE Currency=\'"+currencyname+"\'"\
	        + " ORDER BY time ASC"
	cursor.execute(query)
	results = cursor.fetchall()
	all_data = pd.DataFrame(results, columns=trainingAttributes)
        conn.close()

	# feature discovery
	all_data['volatility'] = (all_data['high']-all_data['low'])/all_data['close']


	# make train test split: train on x% of data before a date, test on data after
	train_percentage = 1.0; train_num = int(len(all_data)*train_percentage)
	train_data, test_data = all_data[0:train_num], all_data[train_num:]

	''' creating windows of timeseries data '''
	# per-window attribute modification
		# normalize the specified columns to the value of the first entry
	#['high','low','close','open_high_diff','close_high_diff']
	cols_to_normalize = ['open','high','low','close']

	lstm_train_input = []
	for i in range(len(train_data)-WINDOW_LEN):
		w = train_data[i:(i+WINDOW_LEN)].copy()
		lstm_train_input.append(w)
	for w in lstm_train_input: normalize_window(w, cols_to_normalize)
	lstm_train_output = \
	 (train_data[WINDOW_LEN:].values/(train_data[:-WINDOW_LEN].values+1))-1 # normalized
	# train_data['close'][WINDOW_LEN:].values unnormalized

	lstm_test_input = []
	for i in range(len(test_data)-WINDOW_LEN):
		w = test_data[i:(i+WINDOW_LEN)].copy()
		lstm_test_input.append(w)
	for w in lstm_test_input: normalize_window(w, cols_to_normalize) 
	lstm_test_output = \
	(test_data[WINDOW_LEN:].values/(test_data[:-WINDOW_LEN].values+1))-1 # normalized
	# test_data['close'][WINDOW_LEN:].values unnormalized

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
	m = build_model(lstm_train_input, output_size=np.shape(lstm_test_input)[2], neurons=20)
	out = (train_data[WINDOW_LEN:].values/(train_data[:-WINDOW_LEN].values+1))-1
	hist = m.fit(lstm_train_input, lstm_train_output, epochs=10, batch_size=1, verbose=2, shuffle=True)

	# save the model
	m.save(outputfilename)

if __name__ == "__main__":
	main()
