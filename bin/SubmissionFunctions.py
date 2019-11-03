from bin.Submission import Submission

"""
Submission functions: retrieves submission from subreddit
"""

# Todo: Rewrite function to use PRAW object instead of praw_q. MP is not needed for this.
def get_hot(lib=None, praw_q=None, subreddit=None, limit=None):
	"""
	Gets hot posts using PRAW

	:param lib: Anu's lib file
	:param praw_q: PRAW object
	:param subreddit: Specified Subreddit
	:param limit: Number of posts
	:return: List of submissions
	:rtype: list
	"""
	# Ensure lib, praw_instance and subreddit are not none
	if (lib is None) or (praw_q is None) or (subreddit is None):
		return None
	try:
		while praw_q.empty():
			lib.sleep(lib.get_config_value("prawqueuewait", .5))
		praw = praw_q.get()
	except Exception as e:
		lib.write_error("ERROR: {}".format(e))
	lib.write_log("Getting hot from subreddit {}".format(subreddit))
	# Get hot submissions from subreddit limited by given value
	try:
		submissions = praw.subreddit(subreddit).hot(limit=limit)
	except Exception as e:
		lib.write_log("Failed to get hot submissions due to the exception: {}".format(str(e)))
		return None
	submission_list = []
	# Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	# Puts praw instance back into queue
	praw_q.put(praw)
	# Return submissions list
	return submission_list


# Todo: Rewrite function to use PRAW object instead of praw_q. MP is not needed for this.
def get_rising(lib=None, praw_q=None, subreddit=None, limit=None):
	"""
	Get rising posts using PRAW

	:param lib: Anu's lib file
	:param praw_q: PRAW object
	:param subreddit: Specified Subreddit
	:param limit: Number of posts
	:return: List of submissions
	:rtype: list
	"""
	# Ensure lib, praw_instance and subreddit are not none
	if (lib is None) or (praw_q is None) or (subreddit is None):
		return None
	try:
		while praw_q.empty():
			lib.sleep(lib.get_config_value("prawqueuewait",.5))
		praw = praw_q.get()
	except Exception as e:
		lib.write_error("ERROR: {}".format(e))
	lib.write_log("Getting rising from subreddit {}".format(subreddit))
	# Get rising submissions from subreddit limited by given value
	try:
		praw = praw_q
		submissions = praw.subreddit(subreddit).rising(limit=limit)
	except Exception as e:
		lib.write_log("Failed to get rising submissions due to the exception: {}".format(str(e)))
		return None
	submission_list = []
	# Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	# Puts praw instance back into queue
	praw_q.put(praw)
	# Return submissions list
	return submission_list


# Todo: Rewrite function to use PRAW object instead of praw_q. MP is not needed for this.
def get_top(lib=None, praw_q=None, subreddit=None, time_filter='all', limit=None):
	"""
	Get top posts using PRAW

	:param lib: Anu's lib file
	:param praw_q: PRAW object
	:param subreddit: Specified Subreddit
	:param time_filter: Specified time-filter
	:param limit: Number of posts
	:return: List of submissions
	:rtype: list
	"""
	# Ensure lib, praw_instance and subreddit are not none
	if (lib is None) or (praw_q is None) or (subreddit is None):
		return None
	try:
		while praw_q.empty():
			lib.sleep(lib.get_config_value("prawqueuewait",.5))
		praw = praw_q.get()
	except Exception as e:
		lib.write_error("ERROR: {}".format(e))
	lib.write_log("Getting top from subreddit {}".format(subreddit))
	# Get top submissions from subreddit limited by given value
	try:
		praw = praw_q
		# time_filter – Can be one of: all, day, hour, month, week, year (default: all).
		submissions = praw.subreddit(subreddit).top(time_filter=time_filter, limit=limit)
	except Exception as e:
		lib.write_log("Failed to get top submissions due to the exception: {}".format(str(e)))
		return None
	submission_list = []
	# Make submissions objects
	for submission in submissions:
		s = Submission(submission)
		submission_list.append(s)
		lib.write_log(s.title)
	lib.write_log("Completed subreddit {}".format(subreddit))
	# Puts praw instance back into queue
	praw_q.put(praw)
	# Return submissions list
	return submission_list


def get_snapshot(lib=None, praw_q=None, submission_id=None):

	pass
