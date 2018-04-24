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

WINDOW_LEN = 24
MAX_TRAIN_SIZE = 5000
NEURON_COUNT = 20
NUM_EPOCHS = 10
TRAINING_ATTRIBUTES = ['open', 'high', 'low', 'close', 'volumefrom', 'volumeto']
COLS_TO_NORMALIZE = ['open','high','low','close']
DISCOVERED_COLS = ['volatility']

# normalize each value in the window to fit the value
# of the first value in the window
def normalize_window_df(window, columnNames):
    for col in columnNames:
    	window.loc[:,col] = window[col]/(window[col].iloc[0]) - 1

def discover_features(frame):
    frame['volatility'] = (frame['high']-frame['low'])/(frame['close']+1)

def main():
	# parsing inputs
	try:
		cflagidx = sys.argv.index('-c')
		currencyname = sys.argv[cflagidx+1]
	except ValueError:
		# malformed command line arguments, print usage and exit
		print "usage: python ", sys.argv[0], "-c nameOfCurrency"
		exit()

	''' SQL Query for Training Data '''
        conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
	cursor = conn.cursor()
	query = "SELECT " + ", ".join(TRAINING_ATTRIBUTES) + " FROM cryptocurrency"\
	        + " WHERE UPPER(Currency)=UPPER(\'"+currencyname+"\')"\
	        + " ORDER BY time ASC"
	cursor.execute(query)
	results = cursor.fetchall()
	all_data = pd.DataFrame(results, columns=TRAINING_ATTRIBUTES)
        del(results)
        conn.close()

	# feature discovery
	discover_features(all_data)

	# make train test split: train on x% of data before a date, test on data after
	train_percentage = 1.0; train_num = int(len(all_data)*train_percentage)
        train_data = all_data[-min(MAX_TRAIN_SIZE, len(all_data)):]
        del(all_data)

	''' creating windows of timeseries data and normalising windows '''
	lstm_train_input = []
	for i in range(len(train_data)-WINDOW_LEN):
	    w = train_data[i:(i+WINDOW_LEN)].copy()
	    lstm_train_input.append(w)
	for i in range(len(lstm_train_input)):
            normalize_window_df(lstm_train_input[i], COLS_TO_NORMALIZE)
	lstm_train_output = \
	 (train_data[WINDOW_LEN:].values/(train_data[:-WINDOW_LEN].values+1))-1 # normalized
        del(train_data)

	''' putting input windows into numpy arrays '''
	lstm_train_input = [np.array(window) for window in lstm_train_input]
	lstm_train_input = np.array(lstm_train_input)

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
	m = build_model(lstm_train_input, output_size=np.shape(lstm_train_input)[2], neurons=NEURON_COUNT)
        hist = m.fit(lstm_train_input, lstm_train_output, epochs=NUM_EPOCHS, batch_size=1, verbose=2, shuffle=True)

	# save the model
	m.save("models/"+currencyname+"_model.h5")

if __name__ == "__main__":
    main()
