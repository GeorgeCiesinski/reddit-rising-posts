import signal
from sys import exit

from bin.LIB import LIB
from bin.DAL import *


class SubredditDBPull:

    def sig_handler(self, sig, frame):
        self.keep_ruinning = False

    def process_end(self):
        self.lib.end()
        exit(0)

    def __init__(self, processname=None, submission_praw_pull_q=None):
        self.keep_ruinning = True
        if (processname is None) or (submission_praw_pull_q is None):
            exit(-1)
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        self.configfile = "config/SubredditDBPull.cfg"
        self.outfile_name = "{}_out.log".format(processname)
        self.errorfile_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg=self.configfile,out_log=self.outfile_name,err_log=self.errorfile_name)



        with Pg.pg_connect(processname) as my_db_connection:
            #TODO: write code for the file here
            while self.keep_ruinning:
                list_of_subreddits = Queue.subreddit_schedule_get(my_db_connection,limit=10)
                self.lib.write_log("Got Subreddits: {}".format(list_of_subreddits))
                for subreddit in list_of_subreddits:
                    submission_praw_pull_q.put(subreddit)
                if len(list_of_subreddits) == 0:
                    self.lib.sleep(.5)



        #Clean up when the process ends
        self.process_end()