from collections import namedtuple
from datetime import datetime

from bin.DAL.Pg import Pg
from bin.DAL.Praw import Praw
from bin.DAL.Queue import Queue
from bin.DAL.Submission import Submission


# Test data:
# Create a submission (simulate a response from praw object by creating a named tuple)
SubmissionTuple = namedtuple(
	'SubmissionTuple',
	'id title url subreddit selftext num_comments comments score author created_utc'
)
s = SubmissionTuple(
	'SubID#1', 'SubTitle', 'SubURL', 'SubredditName', 'SubSelftext',
	10, 'SubComments', 20, 'test_user', datetime.now()
)

thread_id = 1

# Perform tests:
with Pg.pg_connect() as pg:
	# Release all praw logins
	Praw.praw_login_release(pg, 0)
	# Grab a praw login
	print(Praw.praw_login_get(pg, thread_id))

	# Release all scheduled subreddits
	Queue.subreddit_schedule_release(pg, '')
	print(Queue.subreddits_to_crawl_get(pg, thread_id, 10))

	# Insert a submission
	print(Submission.submission_detail_upsert(pg, s))
	print(Submission.submission_snapshot_insert(pg, s))

	# Clean up
	Praw.praw_login_release(pg, 0)
	Queue.subreddit_schedule_release(pg, '')
