"""
Comment Object: Contains comment information
"""


class Comment:
	# Create our own comment object from the given praw comment object
	# input: praw comment
	# output: None
	def __init__(self, comment):

		self.permalink = comment.permalink
		self.body = comment.body
		self.author = comment.author
		self.score = comment.score
		self.created_utc = comment.created_utc
		self.edited = comment.edited
		self.id = comment.id
