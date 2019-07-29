"""
Post Object: contains post information
"""

# We are using UTF-8 not ASCII or other char sets, so we should sanitize the inputs


class Submission (object):
	# Create our own post Object from the given prow submission object
	# input: praw submission
	# output: None
	def __init__(self, submission):
		# submission title & id
		self.title = submission.title
		self.id = submission.id
		# noinspection PyBroadException
		try:
			self.body = submission.body
		except:
			self.body = None
			print("Submission has no body.")
		# TODO: comment_count
		# TODO: post_point_count
		# TODO: author
		# TODO: post_date
		# TODO: url
		# TODO: subreddit
