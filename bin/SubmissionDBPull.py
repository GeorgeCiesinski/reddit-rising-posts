import signal
from sys import exit

from bin.LIB import LIB
from bin.DAL import *


class SubmissionDBPull:

    def sig_handler(self, sig, frame):
        """
        Signal handler will stop the main while loop
        :param sig:  The signal that was received
        :param frame: The execution stack frame
        :return:
        """
        self.keep_ruinning = False

    def __init__(self):
        pass