import praw
from Submission import Submission
import sys

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


if __name__ == "__main__":
	print("Executing as main program. ")

	# Instantiate Reddit
	r = Reddit()

	# Code to print the attributes of an object
	# print(dir(r.reddit))

	subreddit = r.reddit.subreddit('jokes')
	print("The display name is: " + subreddit.display_name)

	submission_PRAW = r.reddit.submission(url="https://www.reddit.com/r/Jokes/comments/cjersb/i_went_into_a_pet_shop_and_asked_for_twelve_bees/")

	# PRAW Submission Object Test
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



