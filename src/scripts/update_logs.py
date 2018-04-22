import time
f= open("crontab_logs.txt","a+")
output = "Job ran at " + str(time.time()) + "\n"
f.write(output)
