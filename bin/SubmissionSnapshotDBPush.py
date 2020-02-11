"""
Moved to SubmissionFunctions
function: submission_snapshot_db_push
Adjust your code and delete this once it's no longer needed
"""


import signal
from sys import exit

import bin.SubmissionFunctions as SubmissionFunctions
from bin.LIB import LIB
from bin.DAL import *


class SubmissionSnapshotDBPush:

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

    def __init__(self,processname=None,submission_snapshot_db_push_q=None):
        self.keep_ruinning = True  # used to keep the process running
        if (processname is None) or (submission_snapshot_db_push_q is None):  # make sure all the required parameters are given
            exit(-1)
        signal.signal(signal.SIGTERM, self.sig_handler)  # signal handler for terminate
        signal.signal(signal.SIGINT, self.sig_handler)  # signal handler for interrupt
        self.output_name = "{}_output.log".format(processname)
        self.error_name = "{}_error.log".format(processname)
        self.lib = LIB(cfg="config/SubmissionSnapshotDBPush.cfg", out_log=self.output_name, err_log=self.error_name)  # make lib instance

        with Pg.pg_connect(processname) as my_db_conneciton:
            while self.keep_ruinning:
                if not submission_snapshot_db_push_q.empty():
                    m_submission = submission_snapshot_db_push_q.get()
                    SubmissionFunctions.submission_snapshot_db_push(self.lib, my_db_conneciton, m_submission)
                else:
                    self.lib.sleep(self.lib.get_config_value("SleepOnEmptyQueue", 60))

        self.lib.write_log("Stopping process {}".format(processname))
        self.process_end()