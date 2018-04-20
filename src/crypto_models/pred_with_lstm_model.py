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
try:
	mflagidx = sys.argv.index('-m')
	inputmodelname = sys.argv[mflagidx+1]
	iflagidx = sys.argv.index('-i')
	inputsamplename = sys.argv[iflagidx+1]
	dflagidx = sys.argv.index('-d')
	daycount = int(sys.argv[dflagidx+1])

except ValueError:
	# malformed command line arguments, print usage and exit
	print "usage: python ", sys.argv[0], "-m inputmodel.h5 -i inputsample.csv -d daycount"
	exit()

# load sample
sample = np.genfromtxt(inputsamplename,delimiter=',')
sample = np.expand_dims(sample, axis=0)

# load model
model = load_model(inputmodelname)

preds = []

# predict the metrics for the given cryptocurrency for the subsequent d days
for d in range(daycount):
	# predict values, unnormalize the prediction
	pred = model.predict(sample)
	pred = (pred+1) * (np.average(sample,axis=1) - 1)
	# use prediction to modify input window, and add the prediction to the list of predictions
	preds.append(pred)

	sample = np.append(sample, [pred], axis=1)
	sample = np.delete(sample, 0, axis=1)
	
print preds