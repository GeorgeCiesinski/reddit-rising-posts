import praw

import bin.SubmissionFunctions as SubmissionFunctions
from bin.LIB import LIB

subreddit = "funny"

reddit = praw.Reddit(
    client_id="Zfl37rh1asVTjQ",
    client_secret="DX87ZhsDhvJrvxdoud0CXmcbLGA",
    username="top10tracket",
    password="k2T%5VuSJc8k",
    user_agent="reddit-rising-posts"
)

submissions = SubmissionFunctions.get_hot(lib=LIB, subreddit=subreddit, limit=10, praw_q=reddit)
print(submissions)
