import praw
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
	# print("The subreddit title is: " + subreddit.title)

	submission = r.reddit.submission(url="https://www.reddit.com/r/Jokes/comments/cjersb/i_went_into_a_pet_shop_and_asked_for_twelve_bees/")
	print("The submission title is: " + submission.title + "\n")
	print("The submission id is: " + submission.id + "\n")
	print("The submission body contains: \n" + submission.selftext + "\n")
	print("The number of comments is: " + str(submission.num_comments))
	print("The score is: " + str(submission.score))
	print("The author is: " + str(submission.author))
	print("This post was created on: " + str(submission.created_utc))
	print("The url is: " + submission.url)
	print("The subreddit is: " + str(submission.subreddit))



