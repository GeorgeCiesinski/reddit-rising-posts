#!/user/bin/python3

from DAL import Helper

"""
A note about the Queue class. All of the methods require a "thread_id", which is returned as part of the
Praw.praw_thread_get() method. That method gets a thread_id from the "praw" table in Postgres.
This thread_id is used to keep track of which subreddit/post control row is assigned to each process, and can
help with troubleshooting and profiling.
"""
class Queue:
	#
	@staticmethod
	def subreddits_to_crawl_get(pg, thread_id, limit=10):
		cur = pg.cursor()
		cur.execute("select * from subreddits_to_crawl_get(%s, %s)", (thread_id, limit))

		# todo: change this to map()?
		output = []
		for row_raw in cur.fetchall():
			row = Helper.pg_col_map(cur.description, row_raw)
			output.append(row)

		cur.close()
		return output

	#
	@staticmethod
	def subreddit_schedule_release(pg, subreddit=''):
		cur = pg.cursor()
		cur.execute("select subreddit_schedule_release(%s)", (subreddit, ))
		cur.close()
		return True

	#
	@staticmethod
	def post_control_get(pg, thread_id, limit=10):
		cur = pg.cursor()
		cur.execute("select * from post_control_get(%s, %s)", (thread_id, limit))

		# todo: change this to map()?
		output = []
		for row_raw in cur.fetchall():
			row = Helper.pg_col_map(cur.description, row_raw)
			output.append(row)

		cur.close()
		return output

	#
	@staticmethod
	def post_control_release(pg, release_id):
		cur = pg.cursor()
		cur.execute("select post_control_release(%s)", (release_id,))
		cur.close()
		return True

	#
	@staticmethod
	def post_control_upsert(pg, post_id, snap_freq):
		cur = pg.cursor()
		cur.execute("select post_control_upsert(%s, %s)", (post_id, snap_freq))
		cur.close()
		return True

	#
	@staticmethod
	def post_detail_control_get(pg, thread_id, limit=10):
		cur = pg.cursor()
		cur.execute("select * from post_detail_control_get(%s, %s)", (thread_id, limit))

		# todo: change this to map()?
		output = []
		for row_raw in cur.fetchall():
			row = Helper.pg_col_map(cur.description, row_raw)
			output.append(row)

		cur.close()
		return output

	#
	@staticmethod
	def post_detail_control_insert(pg, post_id):
		cur = pg.cursor()
		cur.execute("select post_detail_control_insert(%s)", (post_id,))
		cur.close()
		return True
