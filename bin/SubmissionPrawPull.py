"""
Description: Used to Submission snapshots or source
"""

import bin.SubmissionFunctions as SubmissionFunctions
import signal
from sys import exit

from bin.LIB import LIB
from bin.DAL import *

class SubmissionPrawPull:

    def sig_handler(self, sig, frame):
        self.keep_ruinning = False

    def process_end(self):
        self.lib.end()
        exit(0)


    def __init__(self, processname=None, submission_praw_pull_q = None, submission_db_push_q = None, comment_db_push_q = None ):
        self.keep_ruinning = True
        if (processname is None) or (submission_praw_pull_q is None) or (submission_db_push_q is None) or (comment_db_push_q is None):
            exit(-1)
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        self.output_name = "{}_output.log".format(processname)
        self.error_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg="config/SubmissionPrawPull.cfg", out_log=self.output_name, err_log=self.error_name)

        with Pg.pg_connect(processname) as my_db_connection:
            while self.keep_ruinning:
                