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
except ValueError:
	# malformed command line arguments, print usage and exit
	print "usage: python ", sys.argv[0], "-m inputmodel.h5 -i inputsample.csv"
	exit()

sample = np.genfromtxt(inputsamplename,delimiter=',')
sample = np.expand_dims(sample, axis=0)

model = load_model(inputmodelname)
pred = model.predict(sample)
print pred