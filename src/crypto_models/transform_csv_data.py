import sys
import pandas as pd
import numpy as np
import time
from datetime import datetime

# parsing inputs
try:
	iflagidx = sys.argv.index('-i')
	inputfilename = sys.argv[iflagidx+1]
	oflagidx = sys.argv.index('-o')
	outputfilename = sys.argv[oflagidx+1]
except ValueError:
	# malformed command line arguments, print usage and exit
	print "usage: python ", sys.argv[0], "-i inputdatafile.csv -o outputdatafile.csv"
	exit()


''' Putting data into a dataframe '''
all_data = pd.read_csv(inputfilename)

# make a new column turning date strings into numerical times,
# sort by name and time, then drop non-numerical attributes
all_data['time'] = all_data.apply(lambda t: time.mktime(datetime.strptime(t['date'], '%Y-%m-%d').timetuple()), axis=1)
all_data = all_data.sort_values(by=['name','time'])
all_data = all_data.drop(['slug','symbol','name','date','ranknow','time'], 1)

# per-row attribute modification
# all_data['close_off_high'] = 2*(all_data['high']-all_data['close'])\
#                              /(all_data['high']-all_data['low'])-1
# all_data['volatility'] = (all_data['high']-all_data['low'])/all_data['open']

all_data.to_csv(outputfilename, encoding='utf-8', index=False)
