from bin.DAL.Pg import Pg
from bin.DAL.Praw import Praw
from bin.DAL.Queue import Queue


thread_id = 1
with Pg.pg_connect() as pg:
	# Release all praw logins
	Praw.praw_login_release(pg, 0)
	# Grab a praw login
	print(Praw.praw_login_get(pg, thread_id))




	# Release all scheduled subreddits
	Queue.subreddit_schedule_release(pg, '')
	print(Queue.subreddits_to_crawl_get(pg, thread_id, 10))

	# Clean up
	Praw.praw_login_release(pg, 0)
	Queue.subreddit_schedule_release(pg, '')
