#!/user/bin/python3

from bin.DAL.Helper import Helper


class Queue:
	@staticmethod
	def subreddits_to_crawl_get(pg, thread_id, limit=10):
		with pg.cursor() as cur:
			cur.execute("select name, last_crawled from subreddits_to_crawl_get(%s, %s)", (thread_id, limit))

			output = []
			for row in cur:
				output.append(row)

		return output

	#
	@staticmethod
	def subreddit_schedule_release(pg, subreddit=''):
		with pg.cursor() as cur:
			cur.execute("select subreddit_schedule_release(%s)", (subreddit, ))
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
