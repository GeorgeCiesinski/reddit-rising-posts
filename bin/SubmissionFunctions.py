from bin.Submission import Submission

"""
Submission functions: retrieves submission from subreddit
"""

"""
# Get hot posts from subreddit
# input: Lib lib, MP Queue, String subreddit, integer limit
# output: list our submissions
def get_hot(lib=None, praw_q=None, subreddit=None, limit=None):
	#TODO: Ensure lib, praw_q and subreddit are not none
	if (lib is None) or (praw_q is None) or (subreddit is None):
		return None
	lib.write_log("Getting hot from subreddit {}".format(subreddit))
	#TODO: Get praw instance from queue to use, wait until one is available
	try:
		while praw_q.empty():
			lib.sleep(.5)
	except Exception as e:
		lib.write_error("ERROR: {}".format(e))
	praw = praw_q.get()
	#TODO: Get hot submissions from subreddit limited by given value
	submissions = praw.subreddit(subreddit).hot(limit=limit)
	submission_list = []
	#TODO: Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	#TODO: Return praw instance to queue
	praw_q.put(praw)
	#TODO: Return submissions list
	return submission_list
"""


# Get hot without MP, for testing purposes
def get_hot(lib=None, praw_instance=None, subreddit=None, limit=None):
	# TODO: Ensure lib, praw_instance and subreddit are not none
	if (lib is None) or (praw_instance is None) or (subreddit is None):
		return None
	lib.write_log("Getting hot from subreddit {}".format(subreddit))
	# TODO: Get hot submissions from subreddit limited by given value
	try:
		praw = praw_instance
		submissions = praw.subreddit(subreddit).hot(limit=limit)
	except Exception as e:
		lib.write_log("Failed to get hot submissions due to the exception: {}".format(e.message))
	submission_list = []
	# TODO: Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	# TODO: Return submissions list
	return submission_list


# Get rising posts from subreddit
# input: Lib lib, MP Queue, String subreddit, integer limit
# output: list our submissions
def get_rising(lib=None, praw_instance=None, subreddit=None, limit=None):
	# TODO: Ensure lib, praw_instance and subreddit are not none
	if (lib is None) or (praw_instance is None) or (subreddit is None):
		return None
	lib.write_log("Getting rising from subreddit {}".format(subreddit))
	# TODO: Get rising submissions from subreddit limited by given value
	try:
		praw = praw_instance
		submissions = praw.subreddit(subreddit).rising(limit=limit)
	except Exception as e:
		lib.write_log("Failed to get rising submissions due to the exception: {}".format(e.message))
	submission_list = []
	# TODO: Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	# TODO: Return submissions list
	return submission_list


# Get top posts from subreddit
# input: Lib lib, MP Queue, String subreddit, integer limit
# output: list our submissions
def get_top(lib=None, praw_instance=None, subreddit=None, limit=None):
	# TODO: Ensure lib, praw_instance and subreddit are not none
	if (lib is None) or (praw_instance is None) or (subreddit is None):
		return None
	lib.write_log("Getting top from subreddit {}".format(subreddit))
	# TODO: Get top submissions from subreddit limited by given value
	try:
		praw = praw_instance
		submissions = praw.subreddit(subreddit).top(limit=limit)
	except Exception as e:
		lib.write_log("Failed to get top submissions due to the exception: {}".format(e.message))
	submission_list = []
	# TODO: Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	# TODO: Return submissions list
	return submission_list

