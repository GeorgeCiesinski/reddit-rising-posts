import praw
from Post import Post
from Comment import Comment


def get_subreddits():
	# get list of subreddits from the DB
	return ['funny', 'sad']


def populate_comments(submission):
	# Get comments
	# Flatten them
	for comment in []:
		if comment != "root":
			continue
		comment = Comment(comment)
		comment.write_to_control()
		comment.write_detail()
	pass


def populate_subreddits(subreddit):
	subreddits = get_subreddits()
	for sr in subreddits:
		subreddit = reddit.subreddit(sr)
		l = subreddit.hot(limit=10)
		for submission in subreddit.hot(limit=10):
			p = Post(submission)
			p.write_to_control()
			p.write_detail()
			populate_comments(submission)


def main(reddit):
	# Each function needs to be its own thread
	populate_subreddits(reddit)





if __name__ == '__main__':
	reddit = praw.Reddit(client_id='nrE5x4yJ_LUo9Q',
						 client_secret='m8ItmlnLRlJ6GVVS1KD5tWsvhsQ',
						 username='cussbot',
						 password='SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS',
						 user_agent='cussbot by /u/th1nker')
	main(reddit)
