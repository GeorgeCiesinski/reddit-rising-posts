"""
Description: Used to collect data from Reddit
"""

from .SubmissionFunctions import SubmissionFunctions
from . import CommentFunctions
from .LIB import LIB


class DataCollector:

    # Start the data collector for subreddit. It is to collect submission and then collect comments for them
    # Input:String config,  String subreddit name
    # Output: None
    def __init__(self, subreddit=None, praw_q = None):
        lib = LIB(cfg="config/DataCollection.cfg")
        lib.write_log("Data Collector {}".format(subreddit))

        submissionFunction = SubmissionFunctions()

        # TODO: get submissions from reddit for the subreddit (Submissions.get_hot(subreddit='funny', limit = 10) for example)
        submissions = submissionFunction.get_hot(subreddit=subreddit, limit=10, praw_q=praw_q)
        # for each submission
            # TODO: Get comments (Comments.get_root_comments(Post post))

        # TODO: Print to screen (here is where we would send it to the database rather than printing it)

        print(len(submissions))

        lib.end()
        pass
