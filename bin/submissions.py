"""
reddit-rising-posts

username = "top10tracket"
password = "k2T%5VuSJc8k"

client_id = "Zfl37rh1asVTjQ"
client_secret = "DX87ZhsDhvJrvxdoud0CXmcbLGA"
"""

import praw
import sys


class Reddit:

    # Default subreddit is funny
    subreddit = "funny"
    option = None
    loopvar = 1

    # init b/c Pep8 complained
    def __init__(self):
        # Reddit API Login
        reddit = praw.Reddit(client_id="Zfl37rh1asVTjQ",
                             client_secret="DX87ZhsDhvJrvxdoud0CXmcbLGA",
                             username="top10tracket",
                             password="k2T%5VuSJc8k",
                             user_agent="reddit-rising-posts")

        print("API has logged in. \n")

    def menu(self):
        print("menu called. ")

        while self.loopvar == 1:

            print("\nThe selected subreddit is " + self.subreddit + "\n")
            print("1 - Different subreddit. \n" +
                  "2 - Print first 10 submission IDs. \n" +
                  "3 - Return data for first 10 submission IDs. \n" +
                  "4 - Quit."
                  )
            self.option = input("Select an option: ")
            # print(type(self.option))

            if self.option == "1":
                self.change_subreddit()
            elif self.option == "2":
                self.print_ten()
            elif self.option == "3":
                self.store_ten()
            elif self.option == "4" or "quit" or "Quit":
                print("The program will now quit. ")
                sys.exit()
            else:
                print("Please enter a valid option. \n")

    # Change Subreddit
    def change_subreddit(self):
        self.subreddit = input("\nPlease enter the name of the subreddit: ")

    # Print first 10 submission IDs
    def print_ten(self):
        print("print_ten called. ")

        # Stores 10 submissions in list

    # Loop through IDs and print Submission ID, Title, Upvotes, and Message Body
    def store_ten(self):
        print("store_ten called. ")


if __name__ == "__main__":
    print("Executing as main program. ")

    # Instantiate Reddit and login
    r = Reddit()

    # Open Menu
    r.menu()

"""
# Subreddits
subreddit = input("Which Subreddit do you want to look in? ")
sr = Reddit.r.subreddit(subreddit)

"""
