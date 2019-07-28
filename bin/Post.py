"""
Post Object: contains post information
"""


class Post (object):
	# Create our own post Object from the given prow submission object
	# input: praw submission
	# output: None
	def __init__(self, post):
		self.title = post.title
		self.id = post.id
		# noinspection PyBroadException
		try:
			self.body = post.body
		except:
			self.body = None
		# TODO: comment_count
		# TODO: post_point_count
		# TODO: author
		# TODO: post_date
		# TODO: url
