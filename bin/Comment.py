
"""
Comment Object: Contains comment information
"""

"""
Notes for George:
*Temporary, will delete when not needed anymore.
Reddit rising posts will start the DataCollector.py
DataCollector.py will call commend and post functions
CommentFunctions.py
- get_all_comments gets all the comments, converts it into our own comment object
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
		# TODO: Comment replies is not working. Requires further research
		self.created_utc = comment.created_utc
		self.edited = comment.edited
		self.id = comment.id
