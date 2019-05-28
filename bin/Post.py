class Post (object):
	def __init__(self, post):
		self.title = post.title
		self.id = post.id
		try:
			self.body = post.body
		except:
			self.body = None

	def write_to_control(self):
		# Write to the post_control table
		# It will also update the post_control table
		# Start as a new thread
		pass

	def write_detail(self):
		pass
