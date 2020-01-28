import signal
from sys import exit

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

    def __init__(self, processname=None, submission_snapshot_praw_pull_q=None):

        # used to keep the process running until a kill signal is received.
        self.keep_running = True

        # make sure all the required parameters are given
        if (processname is None) or (submission_snapshot_praw_pull_q is None):
            exit(-1)

        # signal handler for terminate
        signal.signal(signal.SIGTERM, self.sig_handler)
        # signal handler for interrupt
        signal.signal(signal.SIGINT, self.sig_handler)
