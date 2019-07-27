import sys
import signal
import multiprocessing as MP

from bin.LIB3 import LIB
from bin.DataCollector import DataCollector as DC


# used to listen for ^C to gracefully terminate the program
# input: not sure
# output: None
def sig_handler(sig,frame):
    exit()

# Gracefully exit the program, clean ups to be done here
# input: None
# output: None
def exit():
    lib.write_log("Exiting..")
    #kill all processes that were started by the program
    for process in PROCESSLIST:
        process.terminate()
    sys.exit()

# Main of the program
if __name__ == '__main__':
    # Signal Listener
    signal.signal(signal.SIGINT, sig_handler)

    # Create the lib object
    config_file = "config/RedditRisingPost.cfg"
    lib = LIB(cfg=config_file)

    # Read the config file program specific values, and define other variables
    PROCESSLIST = []

    # TODO: Start datacollector for subreddits
    try:
        subreddits = ['funny'] # get  this list from DB
        for subreddit in subreddits:
            lib.write_log("Starting Data Collection for {}".format(subreddit))
            cfg = "config/DataCollection.cfg"
            process = MP.Process(target=DC, args=(cfg, subreddit))
            process.start()
            PROCESSLIST.append(process)
            lib.write_log("Done starting Data Collection for {}".format(subreddit))
    except Exception as E:
        pass

    # TODO: Remove, this is here for testing.
    while True:
            lib.sleep(1)
            for process in PROCESSLIST:
                    if not process.is_alive():
                            PROCESSLIST.remove(process)
            if len(PROCESSLIST) == 0:
                    exit()

# Don't import this file, run it directly
if __name__ == "RedditRisingPost":
    print("NO IMPORTS")
    sys.exit()
