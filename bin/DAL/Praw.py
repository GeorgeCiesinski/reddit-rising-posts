#!/user/bin/python3


class Praw:
	# Get the login information for praw
	@staticmethod
	def praw_login_get(pg, thread_id):
		with pg.cursor() as cur:
			cur.execute(
				"select client_id, client_secret, username, password, user_agent from praw_login_get(%s)",
				(thread_id,)
			)
			row = cur.fetchone()

		return row

	# Release the praw login for a new process to pick it up
	@staticmethod
	def praw_login_release(pg, release_thread_id=0):
		cur = pg.cursor()
		cur.execute("select praw_login_release(%s)", (release_thread_id,))
		cur.close()
		return True
