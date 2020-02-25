"""
Post Object: contains post information
"""

# Script relies on UTF-8 not ASCII or other char sets / inputs should be sanitized


class Submission (object):

	def __init__(self, lib, submission):
		"""
		Create our own post Object from the given prow submission object

		:param lib: Anu's LIB file
		:param submission: Submission object
		"""

		if submission is None:
			self.title = None
			self.id = None
			self.url = None
			self.subreddit = None
			self.score = None
			self.upvote_ratio = None
			self.author = None
			self.created_utc = None

		else:

			self.title = submission.title
			self.id = submission.id
			self.url = submission.url
			self.subreddit = submission.subreddit
			self.num_comments = submission.num_comments
			self.score = submission.score
			self.upvote_ratio = submission.upvote_ratio

			try:
				self.author = submission.author
			except:
				# In case author is deleted or otherwise doesn't exist
				self.author = None
				lib.write_log(f'Submission {submission.id} does not have author.')

			# created date
			self.created_utc = submission.created_utc
