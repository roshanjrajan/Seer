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

from build_lstm_model import *

def normalize_window_np(window, indices):
    ret = window/(window[:][0]+1)-1
    return ret

# parsing inputs
try:
	mflagidx = sys.argv.index('-m')
	inputmodelname = sys.argv[mflagidx+1]
	cflagidx = sys.argv.index('-c')
	currencyname = sys.argv[cflagidx+1]
	dflagidx = sys.argv.index('-d')
	daycount = int(sys.argv[dflagidx+1])

except ValueError:
	# malformed command line arguments, print usage and exit
	print "usage: python ", sys.argv[0], "-m inputmodel.h5 -c currencyname -d daycount"
	exit()
# get most recent crypto data from database with SQL query
conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
cursor = conn.cursor()
query = "SELECT " + ", ".join(TRAINING_ATTRIBUTES) + " FROM ("\
        + "SELECT " + ", ".join(TRAINING_ATTRIBUTES)+", time FROM bitcoin "\
        + " WHERE UPPER(Currency)=UPPER(\'"+currencyname+"\')"\
        + " ORDER BY Time DESC LIMIT 10"\
        + ") as sub "\
        + " ORDER BY time ASC"
cursor.execute(query)
results = cursor.fetchall()
results = [[float(t) for t in a] for a in results]
df = pd.DataFrame(results, columns=TRAINING_ATTRIBUTES)
discover_features(df)
sample = df.as_matrix().copy()
sample = np.expand_dims(sample, axis=0)
print sample
conn.close()

# load model
model = load_model(inputmodelname)

preds = []

# predict the metrics for the given cryptocurrency for the subsequent d days
for d in range(daycount):
	# normalize input, predict values, unnormalize the prediction
        normalized_window = normalize_window_np(sample, [TRAINING_ATTRIBUTES.index(t) for t in COLS_TO_NORMALIZE])
        pred = model.predict(normalized_window)
        pred = (pred+1) * (np.average(sample, axis=1) - 1)
	# use prediction to modify input window, and add the prediction to the list of predictions
	preds.append(pred)

	sample = np.append(sample, [pred], axis=1)
	sample = np.delete(sample, 0, axis=1)
	
print preds
