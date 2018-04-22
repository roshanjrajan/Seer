import numpy as np
import matplotlib.pyplot as plt
from pred_with_lstm_model import *

DEFAULT_PAST_COUNT = 24*30
DEFAULT_FUTURE_COUNT = 24*10

def main():
	# parsing inputs
	try:
		argpastcount = DEFAULT_PAST_COUNT
		argfuturecount = DEFAULT_FUTURE_COUNT

		mflagidx = sys.argv.index('-m')
		argmodelname = sys.argv[mflagidx+1]
		cflagidx = sys.argv.index('-c')
		argcurrencyname = sys.argv[cflagidx+1]
		
		if '-p' in sys.argv:
			pflagidx = sys.arg.index('-p')
			argpastcount = sys.argv[[pflagidx+1]]
		if '-f' in sys.argv:
			fflagidx = sys.argv.index('-f')
			argdaycount = sys.argv[fflagidx+1]


	except ValueError:
		# malformed command line arguments, print usage and exit
		print "usage: python ", sys.argv[0], "-m model.h5 -c nameOfCurrency -p pastcount -f futurecount"
		print "-p and -f optional"
		exit()

        currencyname = argcurrencyname
        pastcount = argpastcount
        futurecount = argfuturecount
        currencyname = argcurrencyname
        modelname = argmodelname

	# get the past days data
	conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
	cursor = conn.cursor()
	query = "SELECT " + ", ".join(TRAINING_ATTRIBUTES) + " FROM ("\
	        + "SELECT " + ", ".join(TRAINING_ATTRIBUTES)+", time FROM bitcoin "\
	        + " WHERE UPPER(Currency)=UPPER(\'"+currencyname+"\')"\
	        + " ORDER BY Time DESC LIMIT "+str(pastcount)\
	        + ") as sub "\
	        + " ORDER BY time ASC"
	cursor.execute(query)
	results = cursor.fetchall()
	past_df = pd.DataFrame(results, columns=TRAINING_ATTRIBUTES)
	conn.close()

	# get the predicted future data
	future_df = predict_future(inputmodelname = modelname,
					currencyname = currencyname,
					daycount = futurecount)

	print past_df
        print future_df

if __name__ == "__main__":
	main()
