"""
Comment Object: Contains comment information
"""


class Comment:

	def __init__(self, comment):
		"""
		Create our own comment object from the given praw comment object

		:param comment: Specified comment object
		"""

		self.permalink = comment.permalink
		self.body = comment.body
		self.author = comment.author
		self.score = comment.score
		self.created_utc = comment.created_utc
		self.edited = comment.edited
		self.id = comment.id
