#!/user/bin/python3

class Post:
	@staticmethod
	def post_details_upsert(pg, post_id, subreddit_id, posted_by_id, title, body, posted_on):
		cur = pg.cursor()
		cur.execute("select post_details_upsert(%s, %s, %s, %s, %s, %s)",
					(post_id, subreddit_id, posted_by_id, title, body, posted_on)
				)
		cur.close()
		return True

	@staticmethod
	def post_snapshot_insert(pg, post_id, thread_id, rank, upvote, downvot, comment, is_hot):
		cur = pg.cursor()
		cur.execute("select post_snapshot_insert(%s, %s, %s, %s, %s, %s, %s)",
					(post_id, thread_id, rank, upvote, downvot, comment, is_hot)
				)
		cur.close()
		return True
