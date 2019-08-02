#!/user/bin/python3

from DAL.Helper import Helper


class Praw:
	# Get the login information for praw
	@staticmethod
	def praw_thread_get(pg):
		cur = pg.cursor()
		cur.execute("select praw_thread_get()")
		row = Helper.pg_col_map(cur.description, cur.fetchone())
		cur.close()
		return row

	# Release the praw login for a new process to pick it up
	@staticmethod
	def praw_thread_release(pg, release_thread_id=0):
		cur = pg.cursor()
		cur.execute("select praw_thread_release(%s)", (release_thread_id,))
		cur.commit()
		cur.close()
		return True
