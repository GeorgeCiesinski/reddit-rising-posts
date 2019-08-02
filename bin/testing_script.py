import praw
from bin.Submission import Submission
from bin.Comment import Comment
from bin.SubmissionFunctions import SubmissionFunctions
from bin.CommentFunctions import CommentFunctions
import sys
import multiprocessing as MP
from time import sleep

"""
This script is temporary and is not part of reddit-rising-posts.
The purpose is simply to invoke instances of classes for testign purposes.
Delete once the purpose has been fulfilled.
"""

"""
ACCOUNT INFO - To be updated & deleted

reddit-rising-posts
username = "top10tracket"
password = "k2T%5VuSJc8k"
client_id = "Zfl37rh1asVTjQ"
client_secret = "DX87ZhsDhvJrvxdoud0CXmcbLGA"
"""


class Reddit:

	def __init__(self):
		# Reddit API Login
		self.reddit = praw.Reddit(
			client_id="Zfl37rh1asVTjQ",
			client_secret="DX87ZhsDhvJrvxdoud0CXmcbLGA",
			username="top10tracket",
			password="k2T%5VuSJc8k",
			user_agent="reddit-rising-posts"
		)

		print("API has logged in. \n")

	def get_praw(self):
		return self.reddit


if __name__ == "__main__":
	print("Executing as main program. ")

	# Instantiate Reddit
	r = Reddit()

	praw_q = MP.Queue()
	praw_q.put(r.get_praw())

	# todo: this list is to be retrieved from the DB
	subreddits = ['science', 'funny']

	# loop through the subreddits
	processes = []
	for r in subreddits:
		p = MP.Process(name=r, target=SubmissionFunctions.get_hot, args=(r, 10, praw_q))
		p.start()
		processes.append(p)
	while True:
		for p in processes:
			if not p.is_alive():
				print("%s process ended" % p.name)
				p.join()
				del processes[p]
		if len(processes) == 0:
			break
		sleep(1)

	sys.exit()



	"""
	# SUBREDDIT TEST CODE
	
	subreddit = r.reddit.subreddit('jokes')
	print("The display name is: " + subreddit.display_name)
	"""

	"""
	# SUBMISSION TEST CODE
	
	submission_PRAW = r.reddit.submission(url="https://www.reddit.com/r/Jokes/comments/cjersb/i_went_into_a_pet_shop_and_asked_for_twelve_bees/")

	# PRAW Submission Object
	print("\nUSING PRAW SUBMISSION OBJECT \n")
	print("The submission title is: " + submission_PRAW.title)
	print("The submission id is: " + submission_PRAW.id)
	print("The submission body contains: \n\n" + submission_PRAW.selftext + "\n")
	print("The number of comments is: " + str(submission_PRAW.num_comments))
	print("The score is: " + str(submission_PRAW.score))
	print("The author is: " + str(submission_PRAW.author))
	print("This post was created on: " + str(submission_PRAW.created_utc))
	# TODO: Research correct method to convert UTC time into readible format
	print("The url is: " + submission_PRAW.url)
	print("The subreddit is: " + str(submission_PRAW.subreddit))

	# Our Submission Object
	s = Submission(submission_PRAW)
	print("\nUSING OUR OWN SUBMISSION OBJECT \n")
	print("The submission title is: " + s.title)
	print("The submission id is: " + s.id)
	print("The submission body contains: \n\n" + s.selftext + "\n")
	print("The number of comments is: " + str(s.num_comments))
	print("The score is: " + str(s.score))
	print("The author is: " + str(s.author))
	print("This post was created on: " + str(s.created_utc))
	# TODO: Research correct method to convert UTC time into readible format
	print("The url is: " + s.url)
	print("The subreddit is: " + str(s.subreddit))
	"""

	# COMMENT TEST CODE

	"""
	comment_praw = r.reddit.comment(url="https://www.reddit.com/r/Jokes/comments/cjersb/i_went_into_a_pet_shop_and_asked_for_twelve_bees/evd67qn/")

	# PRAW Comment Object
	print("\nUSING PRAW COMMENT OBJECT\n")
	print("The comment url is: " + comment_praw.permalink + "\n")
	print("The comment body contains: \n\n" + comment_praw.body + "\n")
	print("The comment author is: " + str(comment_praw.author))
	print("The comment score is: " + str(comment_praw.score))
	# Requires update to accurately display number of top level replies
	print("The reply count is: " + str(comment_praw.replies.__len__()))
	print("This comment was created on: " + str(comment_praw.created_utc))
	print("Has this comment been edited: " + str(comment_praw.edited))

	# Our Comment Object
	c = Comment(comment_praw)
	print("\nUSING OUR OWN COMMENT OBJECT\n")
	print("The comment url is: " + c.permalink + "\n")
	print("The comment body contains: \n\n" + c.body + "\n")
	print("The comment author is: " + str(c.author))
	print("The comment score is: " + str(c.score))
	# Requires update to accurately display number of top level replies
	# print("The reply count is: " + str(comment_praw.replies.__len__()))
	print("This comment was created on: " + str(c.created_utc))
	print("Has this comment been edited: " + str(c.edited))
	"""
