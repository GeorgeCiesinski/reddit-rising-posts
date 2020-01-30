from collections import namedtuple
from datetime import datetime

from bin.DAL.Pg import Pg
from bin.DAL.Praw import Praw
from bin.DAL.Queue import Queue
from bin.DAL.Submission import Submission
from bin.DAL.Comment import Comment


# Test data:
# Create a submission (simulate a response from praw object by creating a named tuple)
SubmissionTuple = namedtuple(
	'SubmissionTuple',
	'id title url subreddit num_comments score author created_utc upvote_ratio'
)
my_submission = SubmissionTuple(
	'SubID#1', 'SubTitle', 'SubURL', 'SubredditName',
	10, 9001, 'test_user', datetime.now(), 0.5
)

# Create a comment (simulate a response from praw object by creating a named tuple)
CommentTuple = namedtuple(
	'SubmissionTuple',
	'id link_id score created_utc'
)
my_comment = CommentTuple(
	'ComID#1', 'SubID#1', 300, datetime.now()
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
	print(Submission.submission_detail_upsert(pg, my_submission))
	print(Submission.submission_snapshot_insert(pg, my_submission))
	print(Submission.submission_schedule_set(pg, my_submission, 60))

	# Release all scheduled submissions
	print(Queue.submission_schedule_release(pg, None))
	# Grab all scheduled submissions
	qsub = Queue.submission_schedule_get(pg, 10)
	print(qsub)
	# Release one of the submissions
	print(Queue.submission_schedule_release(pg, my_submission))

	# Insert a comment
	print(Comment.comment_detail_upsert(pg, my_comment))
	print(Comment.comment_snapshot_insert(pg, my_comment))

	# Clean up
	Praw.praw_login_release(pg, 0)
	Queue.subreddit_schedule_release(pg, '')
	Queue.submission_schedule_release(pg, None)
