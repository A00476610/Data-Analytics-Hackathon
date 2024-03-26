# src/logger.py
from datetime import datetime

log_file = "./log_file.txt"

def log_progress(message):
    ''' This function logs the mentioned message at a given stage 
    of the code execution to a log file. Function returns nothing'''

    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ' : ' + message + '\n')