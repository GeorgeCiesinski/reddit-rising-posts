#!/user/bin/python3

import praw


class Praw:
	# Get the login information for praw
	@staticmethod
	def praw_login_get(pg, thread_id):
		# Get the login information
		with pg.cursor() as cur:
			cur.execute("select client_id, client_secret, username, password, user_agent from praw_login_get()")
			login = cur.fetchone()

		# Build the praw object
		p = praw.Reddit(
			client_id=login['client_id'],
			client_secret=login['client_secret'],
			username=login['username'],
			password=login['password'],
			user_agent=login['user_agent'],
		)

		return p

	# Release the praw login for a new process to pick it up
	@staticmethod
	def praw_login_release(pg, release_thread_id=0):
		cur = pg.cursor()
		cur.execute("select praw_login_release(%s)", (release_thread_id,))
		cur.close()
		return True
