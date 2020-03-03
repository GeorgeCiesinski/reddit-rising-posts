import signal
from sys import exit

import bin.SubmissionFunctions as SubmissionFunctions

from bin.LIB import LIB
from bin.DAL import *


"""
Notes - Delete later:

- See subredditdbpull
- You will need handler
- Line 36 & 37
- Use correct multiprocessing queue
- List of submission objects get returned from db
"""


class SubmissionDBPull:

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

    def __init__(self, processname=None, submission_snapshot_praw_pull_q=None):

        # used to keep the process running until a kill signal is received.
        self.keep_running = True

        # make sure all the required parameters are given
        if (processname is None) or (submission_snapshot_praw_pull_q is None):
            exit(-1)

        signal.signal(signal.SIGTERM, self.sig_handler)  # signal handler for terminate
        signal.signal(signal.SIGINT, self.sig_handler)  # siignal handler for interrupt
        self.configfile = "config/SubmissionDBPull.cfg"
        self.outfile_name = "{}_output.log".format(processname)
        self.errorfile_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg=self.configfile, out_log=self.outfile_name, err_log=self.errorfile_name)  # make a lib instance

        # make database connection
        with Pg.pg_connect(processname) as my_db_connection:
            # TODO: write code for the file here
            while self.keep_running:  # keep this process running
                list_of_submissions = SubmissionFunctions.submission_db_pull(self.lib, my_db_connection,limit=10)  # pull a list of submissions from the database
                self.lib.write_log("Got Submission: {}".format(list_of_submissions))
                for subreddit in list_of_submissions:
                    submission_snapshot_praw_pull_q.put(subreddit)  # put the submission into the queue for SubmissionSnapshotPrawPull
                if len(list_of_submissions) == 0:
                    self.lib.sleep(self.lib.get_config_value("SleepOnEmptyQueue", 60))

        self.lib.write_log("Stopping process {}".format(processname))
        self.process_end()  # after kill signal, properly shutdown

