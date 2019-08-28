import praw

import bin.SubmissionFunctions as SubmissionFunctions
import bin.CommentFunctions as CommentFunctions
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


# Get Hot
submissions = SubmissionFunctions.get_hot(lib=lib, subreddit=subreddit, limit=10, praw_instance=reddit)
"""
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
"""
# Get Top
submissions = SubmissionFunctions.get_top(lib=lib, subreddit=subreddit, limit=10, praw_instance=reddit)

for submission in submissions:
    print(submission.title)
    print(submission.score)
    print(submission.id)
"""

comments = CommentFunctions.get_all_comments(lib=lib, praw_instance=reddit, submission_id="cwl2do")

for comment in comments:
    print(comment.body)
