#!/user/bin/python3

import praw
from bin.LIB  import LIB
import os

class Praw:
	# Get the login information for praw
	@staticmethod
	def praw_login_get(lib,pg):

		# Get the login information
		with pg.cursor() as cur:
			cur.execute("select client_id, client_secret, username, password, user_agent from praw_login_get()")
			login = cur.fetchone()

		try:
			lib.write_log("Loging in as {}".format(login['username']))
			# Build the praw object
			p = praw.Reddit(
			client_id=login['client_id'],
			client_secret=login['client_secret'],
			username=login['username'],
			password=login['password'],
			user_agent=login['user_agent'],
			)
		except Exception as e:
			lib.write_log("Praw log in fail due to exception: {}".format(str(e)))
			return None
		else:
			lib.write_log("Praw Log in successful")

		return p

	# Release the praw login for a new process to pick it up
	@staticmethod
	def praw_login_release(pg, release_thread_id=0):
		cur = pg.cursor()
		cur.execute("select praw_login_release(%s)", (release_thread_id,))
		cur.close()
		return True
