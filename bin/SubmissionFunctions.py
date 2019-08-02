from bin.LIB3 import LIB
from bin.Submission import Submission

"""
Submission object: retrieves submission from subreddit
"""


class SubmissionFunctions:
	# Todo: praw queue.get()

	# Get hot posts from subreddit
	# input: String subreddit, integer limit
	# output: list praw submissions
	@staticmethod
	def get_hot(subreddit, limit, praw_q=None):
		print("initializing lib")
		lib = LIB(cfg="../config/SubmissionFunctions.cfg")
		print("initialized")
		try:
			while praw_q.empty():
				print("Waiting for Praw")
				lib.sleep(.5)
		except Exception as e:
			print(e)
		print("Got Praw")
		lib.write_log("Getting hot from subreddit %s" % subreddit)
		print("Getting hot from subreddit %s" % subreddit)
		praw = praw_q.get()
		submissions = praw.subreddit(subreddit).hot(limit=limit)
		for submission in submissions:
			s = Submission(submission)
			print(s.title)
			lib.write_log(s.to_string())

		print("Completed subreddit %s" % subreddit)
		praw_q.put(praw)

	# Get new posts from subreddit
	# input: String subreddit, integer limit
	# output: list praw submissions
	def get_new(self, subreddit=None, limit=10):
		pass

	# Get rising posts from subreddit
	# input: String subreddit, integer limit
	# output: list praw submissions
	def get_rising(self, subreddit=None, limit=10):
		pass

	# Get top posts from subreddit
	# input: String subreddit, integer limit
	# output: list praw submissions
	def get_top(self, subreddit=None, limit=10):
		pass

	# Get top posts from subreddit
	# input: String subreddit, integer limit
	# output: list praw submissions
	def get_controversial(self, subreddit=None, limit=10):
		pass
