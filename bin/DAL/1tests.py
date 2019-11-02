from bin.DAL.Pg import Pg
from bin.DAL.Praw import Praw

with Pg.pg_connect() as pg:
	# Release all praw logins
	Praw.praw_thread_release(pg, 0)

	# Grab a praw login
	print(Praw.get_praw_login(pg))

	