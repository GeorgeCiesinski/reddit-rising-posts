from bin.LIB import LIB
from bin.Submission import Submission

"""
Submission object: retrieves submission from subreddit
"""


class SubmissionFunctions:
	# Todo: praw queue.get()

	lib = None

	def __init__(self):
		self.lib = LIB(cfg="config/SubmissionFunctions.cfg")

	# Get hot posts from subreddit
	# input: String subreddit, integer limit
	# output: list praw submissions
	def get_hot(self, subreddit=None, limit=None , praw_q=None):
		self.lib.write_log("Getting hot from subreddit %s" % subreddit)
		try:
			while praw_q.empty():
				self.lib.write_log("No praw instance, waiting for one to be available")
				self.lib.sleep(.5)
		except Exception as e:
			self.lib.write_error("ERROR: {}".format(e))
		praw = praw_q.get()
		submissions = praw.subreddit(subreddit).hot(limit=limit)
		submission_list = []
		for submission in submissions:
			s = Submission(submission)
			submission_list.append(s)
			self.lib.write_log(s.title)

		self.lib.write_log("Completed subreddit %s" % subreddit)
		praw_q.put(praw)
		return submission_list

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
