# Make submissions snapshot and detail line up with the Submission and Comment object
#	*Rename post tables to submission
#
#	*Change post.subreddit_id to int (normalize)
#	/Drop post.body
#	/Add post.url
#	/Add post.user (author) (normalize)
#
# 	/Change post_snapshot.rank to score
#	/Drop post_snapshot.upvotes
#	/Drop post_snapshot.downvotes
#	/Rename post_snapshot.comments to num_comments
#	/Add post_snapshot.upvote_ratio
#	/Drop post_snapshot.thread_id
#	/Drop post_snapshot.is_hot
#
# /Populate Comment.py
#

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


# Perform tests:
with Pg.pg_connect() as pg:
	# Release all praw logins
	Praw.praw_login_release(pg, 0)
	# Grab a praw login
	print(Praw.praw_login_get(pg))

	# Release all scheduled subreddits
	Queue.subreddit_schedule_release(pg, '')
	# Grab the subreddits scheduled for crawling
	print(Queue.subreddit_schedule_get(pg, 10))

	# Insert a submission
	print(Submission.submission_detail_upsert(pg, s))
	print(Submission.submission_snapshot_insert(pg, s))
	print(Submission.submission_schedule_set(pg, s, 60))

	# Release all scheduled submissions
	print(Queue.submission_schedule_release(pg, None))
	# Grab all scheduled submissions
	qsub = Queue.submission_schedule_get(pg, 10)
	print(qsub)
	# Release one of the submissions
	print(Queue.submission_schedule_release(pg, s))

	# Clean up
	Praw.praw_login_release(pg, 0)
	Queue.subreddit_schedule_release(pg, '')
	Queue.submission_schedule_release(pg, None)
