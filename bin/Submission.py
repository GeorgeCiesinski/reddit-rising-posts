from bin.LIB import LIB

"""
Post Object: contains post information
"""

# Script relies on UTF-8 not ASCII or other char sets / inputs should be sanitized


class Submission (object):

	# Create our own post Object from the given prow submission object
	# input: praw submission
	# output: None
	def __init__(self, submission):

		self.title = submission.title
		self.id = submission.id
		self.url = submission.url
		self.subreddit = submission.subreddit

		try:
			self.selftext = submission.selftext
		except Exception as e:
			self.selftext = None
			# Todo: Update logs with error?

		self.num_comments = submission.num_comments
		self.comments = submission.comments
		self.score = submission.score

		try:
			self.author = submission.author
		except:
			# In case author is deleted or otherwise doesn't exist
			self.author = None
			# Todo: Update logs with error?

		# created date
		self.created_utc = submission.created_utc

	def to_string(self):
		return str(self)
