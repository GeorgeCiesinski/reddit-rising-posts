import signal
from sys import exit

from bin.LIB import LIB
from bin.DAL import *


class SubredditDBPull:

    def sig_handler(self, sig, frame):
        """
        Signal handler will stop the main while loop
        :param sig:  The signal that was received
        :param frame: The execution stack frame
        :return:
        """
        self.keep_ruinning = False

    def process_end(self):
        """
        End the lib instance (its own cleanup), and end this process
        :return:
        """
        self.lib.end()
        exit(0)

    def __init__(self, processname=None, submission_praw_pull_q=None):
        """
        Pull subreddits from the database that need to have their posts pulled
        :param processname: Name of this process, used for identify logs.
        :param submission_praw_pull_q:  Name of the queue that is used by Submission Praw pull when waiting for a subreddit to get data from.
        """
        self.keep_ruinning = True #used to keep the process running until a kill signal is received.
        if (processname is None) or (submission_praw_pull_q is None): #make sure all the required parameters are given
            exit(-1)
        signal.signal(signal.SIGTERM, self.sig_handler) #signal handler for terminate
        signal.signal(signal.SIGINT, self.sig_handler) #siignal handler for interrupt
        self.configfile = "config/SubredditDBPull.cfg"
        self.outfile_name = "{}_out.log".format(processname)
        self.errorfile_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg=self.configfile,out_log=self.outfile_name,err_log=self.errorfile_name) # make a lib instance

        #make database connection
        with Pg.pg_connect(processname) as my_db_connection:
            #TODO: write code for the file here
            while self.keep_ruinning: #keep this process running
                list_of_subreddits = Queue.subreddit_schedule_get(my_db_connection,limit=10) # pull a list of subreddits from the database
                self.lib.write_log("Got Subreddits: {}".format(list_of_subreddits))
                for subreddit in list_of_subreddits:
                    submission_praw_pull_q.put(subreddit) # put the subreddits into the queue for SubmissionPrawPull
                if len(list_of_subreddits) == 0:
                    self.lib.sleep(self.lib.get_config_value("SleepOnEmptyQueue",60))

        self.lib.write_log("Stopping process {}".format(processname))
        self.process_end() #after kill signal, properly shutdown