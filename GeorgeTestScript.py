"""
Don't delete this just yet as it contains the usage of the SubmissionFunctions.py and CommentFunctions.py under
several applications. Use this as an example
"""

import praw

import bin.SubmissionFunctions as SubmissionFunctions
import bin.CommentFunctions as CommentFunctions
from bin.Submission import Submission
from bin.LIB import LIB

subreddit = "funny"
output_name = "{}_output.log".format(subreddit)
error_name = "{}_error.log".format(subreddit)
lib = LIB(cfg="config/DataCollection.cfg", out_log=output_name, err_log=error_name)

reddit = praw.Reddit(
    client_id="Zfl37rh1asVTjQ",
    client_secret="DX87ZhsDhvJrvxdoud0CXmcbLGA",
    username="top10tracket",
    password="k2T%5VuSJc8k",
    user_agent="reddit-rising-posts"
)
"""
# Uncomment for CommentFunctions.py testing
submission_entry = reddit.submission(id="cx596s")
submission = Submission(submission_entry)
"""

"""
# Get Hot
submissions = SubmissionFunctions.get_hot(lib=lib, subreddit=subreddit, limit=10, praw_instance=reddit)

for submission in submissions:
    print(submission.title)
    print(submission.score)
    print(submission.id)
"""
"""
# Get Rising
submissions = SubmissionFunctions.get_rising(lib=lib, subreddit=subreddit, limit=10, praw_instance=reddit)

for submission in submissions:
    print(submission.title)
    print(submission.score)
    print(submission.id)
"""

# Get Top
# time_filter – Can be one of: all, day, hour, month, week, year (default: all).
submissions = SubmissionFunctions.get_top(lib=lib, praw_instance=reddit, subreddit=subreddit, time_filter='week', limit=10)

for submission in submissions:
    print(submission.title)
    print(submission.score)
    print(submission.id)


"""
# Get top-level comments
comments = CommentFunctions.get_root_comments(lib=lib, praw_instance=reddit, submission=submission)

num_comments = len(comments)
print("There are", len(comments), "top-level comments.\n")

for comment in comments:
    print(comment.body)
"""

"""
# Get all comments
# None should replace ad-infinitum

comments = CommentFunctions.get_all_comments(lib=lib, praw_instance=reddit, submission=submission, replace_more_limit=None)

if comments is not None:

    num_comments = len(comments)
    print("There are", len(comments), "comments.\n")

    for comment in comments:
        print(comment.body)
"""
