#!/user/bin/python3

from bin.DAL.Helper import Helper


class Queue:
	@staticmethod
	def subreddit_schedule_get(pg, limit=10):
		with pg.cursor() as cur:
			cur.execute("select name, last_crawled from subreddits_to_crawl_get(%s)", (limit, ))

			output = [row for row in cur]

		return output

	#
	@staticmethod
	def subreddit_schedule_release(pg, subreddit=''):
		with pg.cursor() as cur:
			cur.execute("select subreddit_schedule_release(%s)", (subreddit, ))
		return True

	#
	@staticmethod
	def submission_schedule_get(pg, limit=10):
		cur = pg.cursor()
		cur.execute("select id from submission_control_get(%s)", (limit,))

		output = [row for row in cur]

		cur.close()
		return output

	#
	@staticmethod
	def submission_schedule_release(pg, submission=None):
		if submission is None:
			release_id = ''
		else:
			release_id = submission.id

		with pg.cursor() as cur:
			cur.execute("select submission_schedule_release(%s)", (release_id,))

		return True
