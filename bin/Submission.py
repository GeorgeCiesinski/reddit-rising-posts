"""
Post Object: contains post information
"""

# We are using UTF-8 not ASCII or other char sets, so we should sanitize the inputs


# noinspection PyBroadException
class Submission (object):

	# Create our own post Object from the given prow submission object
	# input: praw submission
	# output: None
	def __init__(self, submission):

		# submission title & id
		self.title = submission.title
		self.id = submission.id

		# below comment is for pycharm to ignore broad exception warning
		# noinspection PyBroadException
		try:
			self.selftext = submission.selftext
		except:
			self.selftext = None
			print("Submission has no body.")

		# number of comments
		self.num_comments = submission.num_comments

		# score
		self.score = submission.score

		# author
		try:
			self.author = submission.author
		except:
			# in case author is deleted or otherwise doesn't exist
			self.author = None

		# post_date
		self.created_utc = submission.created_utc

		# url
		self.url = submission.url

		# subreddit
		self.subreddit = submission.subreddit
