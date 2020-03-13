"""
Description: Used to Submission snapshots or source
"""

import signal
from sys import exit

import bin.SubmissionFunctions as SubmissionFunctions
from bin.LIB import LIB
from bin.DAL import *

class SubmissionSnapshotPrawPull:

    def sig_handler(self, sig, frame):
        """
        Signal handler will stop the main while loop
        :param sig:  The signal that was received
        :param frame: The execution stack frame
        :return:
        """
        self.keep_running = False

    def process_end(self):
        """
        End the lib instance (its own cleanup), and end this process
        :return:
        """
        self.lib.end()
        exit(0)


    def __init__(self, processname=None, submission_snapshot_praw_pull_q = None, submission_snapshot_db_push_q = None):
        """
        Pull submission from praw and put them in submission bd push queue and comment db push queue
        :param processname: Name of this process, used to identify logs.
        :param submission_snapshot_praw_pull_q: queue used to get subreddit where posts should be pulled from
        :param submission_snapshot_db_push_q: queue of submissions for db push
        :param comment_db_push_q: queue of comment for db push
        """
        self.keep_running = True #used to keep the process running
        if (processname is None) or (submission_snapshot_praw_pull_q is None) or (submission_snapshot_db_push_q is None): # make sure all the required parameters are given
            exit(-1)
        signal.signal(signal.SIGTERM, self.sig_handler) #signal handler for terminate
        signal.signal(signal.SIGINT, self.sig_handler)#signal handler for interrupt
        self.output_name = "{}_output.log".format(processname)
        self.error_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg="config/SubmissionSnapshotPrawPull.cfg", out_log=self.output_name, err_log=self.error_name) #make lib instance

        with Pg.pg_connect(processname) as my_db_connection:
            self.praw = None
            while self.praw is  None:
                self.praw = Praw.praw_login_get(self.lib, my_db_connection)
                if self.praw is None:
                    self.lib.sleep(self.lib.get_config_value("SleepOnPrawLoginFail", 60))

        while self.keep_running: # keep this process running
            if not submission_snapshot_praw_pull_q.empty(): #make sure there is a subreddit in the queue
                submissions = submission_snapshot_praw_pull_q.get() #get a subreddit from the queue
                self.lib.write_log("Calling PRAW")
                submission = SubmissionFunctions.submission_snapshot_praw_pull(lib=self.lib, praw=self.praw, submission=submissions)
                self.lib.write_log("Got Submission ID Snapshot '{}'".format(submission.id))
                submission_snapshot_db_push_q.put(submission)
            else:
                self.lib.sleep(self.lib.get_config_value("SleepOnEmptyQueue",60))

        self.lib.write_log("Stopping process {}".format(processname))
        self.process_end()