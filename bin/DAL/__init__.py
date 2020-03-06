#!/user/bin/python3

from bin.DAL.Pg import Pg
from bin.DAL.Helper import Helper
from bin.DAL.Maintenance import Maintenance
from bin.DAL.Praw import Praw
from bin.DAL.Queue import Queue
from bin.DAL.Submission import Submission


class DAL:
	# Initialize the program (this should be run upon the program startup)
	def initialize_db_state(self):
		Praw.praw_login_release(0)  # Release all praw logins
		Maintenance.maint_correct_scrape_schedules()  # Correct scrape schedules that may have corrupted
		Queue.subreddit_schedule_release(0)  # Release all subreddits, so that they can be crawled
		Queue.submission_schedule_release(0)  # Release all posts, so that they can be scraped
