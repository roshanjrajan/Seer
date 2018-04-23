import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pred_with_lstm_model import *

DEFAULT_PAST_COUNT = 24*7
DEFAULT_FUTURE_COUNT = 24

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

	# get the past days data
    conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
    cursor = conn.cursor()
    query = "SELECT " + ", ".join(TRAINING_ATTRIBUTES) + ", time FROM ("\
	        + "SELECT " + ", ".join(TRAINING_ATTRIBUTES)+", time FROM cryptocurrency "\
	        + " WHERE UPPER(Currency)=UPPER(\'"+argcurrencyname+"\')"\
	        + " ORDER BY Time DESC LIMIT "+str(argpastcount)\
	        + ") as sub "\
	        + " ORDER BY time ASC"
    cursor.execute(query)
    results = cursor.fetchall()
    past_df = pd.DataFrame(results, columns=TRAINING_ATTRIBUTES+['time'])
    conn.close()

    # get time data
    past_times = past_df['time'].tolist()
    past_df = past_df.drop(columns=['time'])

    # get the predicted future data, create time data for it
    futr_df = predict_future(inputmodelname = argmodelname,
					currencyname = argcurrencyname,
					daycount = argfuturecount)
    time_width = past_times[1]-past_times[0]
    futr_times = (np.array(range(len(futr_df)))*time_width+(past_times[-1]+time_width))

    trans = past_df.tail(1).append(futr_df.head(1))

    # plot lines
    fig, back = plt.subplots(facecolor='#262626')
    plt.plot(past_times, past_df['open'], '#2AA198')
    plt.plot([past_times[-1], futr_times[0]], trans['open'], 'g')
    plt.plot(futr_times, futr_df['open'], 'g')

    # pretty up
    ax = plt.gca()
    ax.set_facecolor('#262626')
    for idx in ['top','bottom','left','right']:
        ax.spines[idx].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.savefig("../django/portfolio/static/portfolio/"+argcurrencyname+"_plot.png")

if __name__ == "__main__":
    main()
