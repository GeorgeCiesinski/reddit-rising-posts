import praw
import unittest
from Submission import Submission
import SubmissionFunctions
import CommentFunctions
from LIB import LIB


class Praw:

	@staticmethod
	def login():
		r = praw.Reddit(
			client_id='nrE5x4yJ_LUo9Q',
			client_secret='m8ItmlnLRlJ6GVVS1KD5tWsvhsQ',
			user_agent='cussbot by /u/th1nker',
			username='cussbot',
			password='SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS'
		)

		return r


class SubmissionFunctionUnitTest(unittest.TestCase):
	"""Test for SubmissionFunctions.py"""

	def __init__(self, lib, reddit, sr, sub_id, limit):

		# Prints test name
		print('\nTesting results for SubmissionFunctions.py : ')

		# Tests get_hot
		self.get_hot_test(lib, reddit, sr, limit)

		# Tests get_rising
		self.get_rising_test(lib, reddit, sr, limit)

		# Tests get_top
		self.get_top_test(lib, reddit, sr, limit)

		# Tests get_snapshot
		self.get_snapshot_test(lib, reddit, sub_id)

	@staticmethod
	def get_hot_test(lib, reddit, subreddit, limit):

		# Gets submission list
		submission_list = SubmissionFunctions.get_hot(lib, reddit, subreddit, limit)

		# Testing
		assert isinstance(submission_list, list)
		assert len(submission_list) == limit

		# Print results
		print('\nResults of get_hot: ')

		# Testing for item in list
		for ls in submission_list:
			assert isinstance(ls.id, str)
			print(ls.id)

	@staticmethod
	def get_rising_test(lib, reddit, subreddit, limit):

		# Gets submission list
		submission_list = SubmissionFunctions.get_rising(lib, reddit, subreddit, limit)

		# Testing
		assert isinstance(submission_list, list)
		assert len(submission_list) == limit

		# Print results
		print('\nResults of get_rising: ')

		# Testing for item in list
		for ls in submission_list:
			assert isinstance(ls.id, str)
			print(ls.id)

	@staticmethod
	def get_top_test(lib, reddit, subreddit, limit):

		# Gets submission list
		submission_list = SubmissionFunctions.get_top(lib, reddit, subreddit, 'all', limit)

		# Testing
		assert isinstance(submission_list, list)
		assert len(submission_list) == limit

		# Print results
		print('\nResults of get_top: ')

		# Testing for item in list
		for ls in submission_list:
			assert isinstance(ls.id, str)
			print(ls.id)

	@staticmethod
	def get_snapshot_test(lib, reddit, id):

		# Gets snapshot of submission
		snapshot = SubmissionFunctions.get_snapshot(lib, reddit, id)

		# Testing
		assert snapshot.id == id
		assert isinstance(snapshot.title, str)

		# Print Results
		print('\nResults of snapshot: ')
		print(snapshot.id)
		print(snapshot.title)


class CommentFunctionsUnitTest(unittest.TestCase):
	"""Test for CommentFunctions.py"""

	def __init__(self, lib, submission, replace_more):

		# Prints test name
		print('\nTesting results for SubmissionFunctions.py : ')

		# Tests get_all_comments
		self.get_all_comments_test(lib, submission, replace_more)

	@staticmethod
	def get_all_comments_test(lib, submission, replace_more):

		# Gets Comment List
		comment_list = CommentFunctions.get_all_comments(lib, submission, replace_more)

		# Testing
		assert isinstance(comment_list, list)

		# Print a few comments

		print('\nResults of get_all_comments')
		for x in range(4):
			print(comment_list[x].id)

	def get_root_comments_test(self):

		# Gets Comment List

		# Testing

		# Print a few comments

		pass


if __name__ == "__main__":

	"""
	Universal settings
	"""

	# LIB
	lib = LIB()

	# Praw Login
	praw = Praw.login()

	# Submission ID
	sub_id = 'dr35z5'

	"""
	SubmissionFunctions.py Settings
	"""

	# Subreddit
	sr = 'funny'

	# Limit
	limit = 4

	"""
	CommentFunctions.py Settings
	"""

	submission = praw.submission(sub_id)
	s = Submission(submission)

	replace_more = 32

	"""
	Testing Classes
	"""

	# SubmissionFunctions.py Unit Test
	sf = SubmissionFunctionUnitTest(lib, praw, sr, sub_id, limit)
	cf = CommentFunctionsUnitTest(lib, s, replace_more)

	# Cleanup
	lib.end()
