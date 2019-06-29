"""
reddit-rising-posts

username = "top10tracket"
password = "k2T%5VuSJc8k"

client_id = "Zfl37rh1asVTjQ"
client_secret = "DX87ZhsDhvJrvxdoud0CXmcbLGA"
"""

import praw


# Reddit API Login
r = praw.Reddit(client_id="Zfl37rh1asVTjQ",
                client_secret="DX87ZhsDhvJrvxdoud0CXmcbLGA",
                username="top10tracket",
                password="k2T%5VuSJc8k",
                user_agent="reddit-rising-posts")

# Subreddits
subreddit = input("Which Subreddit do you want to look in? ")
sr = r.subreddit(subreddit)


if __name__ == "__main__":
    print("Executing as main program.")
