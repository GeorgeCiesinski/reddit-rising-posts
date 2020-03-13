"""
Description: Used to Submission snapshots or source
"""

import signal
from sys import exit
import datetime

import bin.SubmissionFunctions as SubmissionFunctions
from bin.LIB import LIB
from bin.DAL import *

class SubmissionPrawPull:

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


    def __init__(self, processname=None, submission_praw_pull_q = None, submission_db_push_q = None, comment_db_push_q = None ):
        """
        Pull submission from praw and put them in submission bd push queue and comment db push queue
        :param processname: Name of this process, used to identify logs.
        :param submission_praw_pull_q: queue used to get subreddit where posts should be pulled from
        :param submission_db_push_q: queue of submissions for db push
        :param comment_db_push_q: queue of comment for db push
        """
        self.keep_ruinning = True #used to keep the process running
        if (processname is None) or (submission_praw_pull_q is None) or (submission_db_push_q is None) or (comment_db_push_q is None): # make sure all the required parameters are given
            exit(-1)
        signal.signal(signal.SIGTERM, self.sig_handler) #signal handler for terminate
        signal.signal(signal.SIGINT, self.sig_handler)#signal handler for interrupt
        self.output_name = "{}_output.log".format(processname)
        self.error_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg="config/SubmissionPrawPull.cfg", out_log=self.output_name, err_log=self.error_name) #make lib instance

        with Pg.pg_connect(processname) as my_db_connection:
            self.praw = None
            while self.praw is  None:
                self.praw = Praw.praw_login_get(self.lib,my_db_connection)

        while self.keep_ruinning: # keep this process running
            if not submission_praw_pull_q.empty(): #make sure there is a subreddit in the queue
                subreddit = submission_praw_pull_q.get() #get a subreddit from the queue
                subreddit_filer = self.lib.get_config_value("SubredditFilter", "top")
                try:
                    submission_limit = int(self.lib.get_config_value("SubmissionLimit", 10))
                except:
                    submission_limit = 10
                self.lib.write_log("{} {} {}".format(subreddit[0], subreddit_filer, submission_limit))
                if subreddit_filer.lower() == "rising":
                    submission_list = SubmissionFunctions.get_rising(lib=self.lib,praw=self.praw,subreddit=subreddit[0],limit=submission_limit)
                    for submission in submission_list:
                        self.lib.write_log("Submission ID '{}'".format(submission.id))
                        submission_db_push_q.put(submission)
                        comment_db_push_q.put(submission)
                elif subreddit_filer.lower() == "top":
                    submission_list = SubmissionFunctions.get_top(lib=self.lib,praw=self.praw,subreddit=subreddit[0],limit=submission_limit)
                    for submission in submission_list:
                        self.lib.write_log("Submission ID '{}'".format(submission.id))
                        submission_db_push_q.put(submission)
                        comment_db_push_q.put(submission)
                elif subreddit_filer.lower() == "hot":
                    submission_list = SubmissionFunctions.get_hot(lib=self.lib,praw=self.praw,subreddit=subreddit[0],limit=submission_limit)
                    for submission in submission_list:
                        self.lib.write_log("Submission ID '{}'".format(submission.id))
                        submission_db_push_q.put(submission)
                        comment_db_push_q.put(submission)

                try:
                    # Call subreddit_schedule_release to inform the DB that the subreddit has been crawled and to release and reschedule it
                    with Pg.pg_connect(processname) as my_db_connection:
                        Queue.subreddit_schedule_release(my_db_connection, str(subreddit), str(datetime.datetime.now()))
                except Exception:
                    self.lib.write_log("Failed to release and reschedule the subreddit due to the exception: ")
                    self.lib.write_log(Exception)
                    raise

            else:
                self.lib.sleep(self.lib.get_config_value("SleepOnEmptyQueue",60))

        self.lib.write_log("Stopping process {}".format(processname))
        self.process_end()