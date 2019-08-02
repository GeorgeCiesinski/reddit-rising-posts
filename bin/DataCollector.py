"""
Description: Used to collect data from Reddit
"""

from . import SubmissionFunctions
from . import CommentFunctions
from .LIB3 import LIB
import sys


class DataCollector:

    # Start the data collector for subreddit. It is to collect submission and then collect comments for them
    # Input:String config,  String subreddit name
    # Output: None
    def __init__(self, cfg=None,  subreddit=None):
        lib = LIB(cfg=cfg)
        # TODO: get submissions from reddit for the subreddit (Submissions.get_hot(subreddit='funny', limit = 10) for example)

        # for each submission
            # TODO: Get comments (Comments.get_root_comments(Post post))

        # TODO: Print to screen (here is where we would send it to the database rather than printing it)

        pass
