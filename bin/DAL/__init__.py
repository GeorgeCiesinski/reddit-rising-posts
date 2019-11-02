#!/user/bin/python3

import psycopg2
from bin.DAL.Pg import Pg
from bin.DAL.Helper import Helper
from bin.DAL.Maintenance import Maintenance
from bin.DAL.Praw import Praw
from bin.DAL.Queue import Queue
from bin.DAL.Post import Post
from bin.DAL.Comment import Comment


class DAL:
	### Maintenance methods ###
	# Initialize the program (this should be run upon the program startup)
	def initialize_db_state(self):
		self.praw_thread_release(0)  # Release all praw logins
		self.maint_correct_scrape_schedules()  # Correct scrape schedules that may have corrupted
		self.subreddit_schedule_release(0)  # Release all subreddits, so that they can be crawled
		self.post_control_release(0)  # Release all posts, so that they can be scraped

	# Find any subreddits, posts, and comments, that are scheduled too far into the future
	def maint_correct_scrape_schedules(self):
		return Maintenance.maint_correct_scrape_schedules(self.pg)

	# Calculate (sync) the summarized columns in post_detail from the snapshot for a given post_id
	def maint_post_detail_sync(self, post_id):
		return Maintenance.maint_post_detail_sync(self.pg, post_id)

	### Praw authentication methods ###
	def praw_thread_get(self):
		return Praw.praw_thread_get(self.pg)

	def praw_thread_release(self, thread_id=0):
		return Praw.praw_thread_release(self.pg, thread_id)

	### Queueing methods ###
	def subreddits_to_crawl_get(self, thread_id, limit=10):
		return Queue.subreddits_to_crawl_get(self.pg, thread_id, limit)

	def subreddit_schedule_release(self, release_subreddit_name=0):
		return Queue.subreddit_schedule_release(self.pg, release_subreddit_name)

	def post_control_get(self, thread_id, limit=10):
		return Queue.post_control_get(self.pg, thread_id, limit)

	def post_control_release(self, release_id):
		return Queue.post_control_release(self.pg, release_id)

	def post_control_upsert(self, post_id, snap_frequency):
		return Queue.post_control_upsert(self.pg, post_id, snap_frequency)

	def post_detail_control_get(self, thread_id, limit=10):
		return Queue.post_detail_control_get(self.pg, thread_id, limit)

	def post_detail_control_insert(self, post_id):
		return Queue.post_detail_control_insert(self.pg, post_id)

	### Post related methods ###
	def post_details_upsert(self, post_id, subreddit_id, posted_by_id, title, body, posted_on):
		return Post.post_details_upsert(self.pg, post_id, subreddit_id, posted_by_id, title, body, posted_on)

	def post_snapshot_insert(self, post_id, thread_id, rank, upvote, downvot, comment, is_hot):
		return Post.post_snapshot_insert(pg, post_id, thread_id, rank, upvote, downvot, comment, is_hot)

	### Comment related methods ###
	def comment_details_upsert(self):
		pass

	def comment_snapshot_insert(self):
		pass

	### Archiving methods ###
	def archive_post(self):
		pass
