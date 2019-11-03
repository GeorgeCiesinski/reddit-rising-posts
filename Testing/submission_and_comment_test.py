import praw
import unittest
import SubmissionFunctions
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


# Todo: Write test cases for SubmissionFunctions.py
class SubmissionFunctionUnitTest(unittest.TestCase):
	"""Test for SubmissionFunctions.py"""

	def __init__(self, lib, reddit, sr, limit):

		# Tests get_hot
		self.get_hot_test(lib, reddit, sr, limit)

		# Tests get_rising
		self.get_rising_test(lib, reddit, sr, limit)

		# Tests get_top
		self.get_top_test(lib, reddit, sr, limit)

	@staticmethod
	def get_hot_test(lib, login, subreddit, limit):

		# Gets submission list
		submission_list = SubmissionFunctions.get_hot(lib, login, subreddit, limit)

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
	def get_rising_test(lib, login, subreddit, limit):

		# Gets submission list
		submission_list = SubmissionFunctions.get_rising(lib, login, subreddit, limit)

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
	def get_top_test(lib, login, subreddit, limit):

		# Gets submission list
		submission_list = SubmissionFunctions.get_top(lib, login, subreddit, 'all', limit)

		# Testing
		assert isinstance(submission_list, list)
		assert len(submission_list) == limit

		# Print results
		print('\nResults of get_top: ')

		# Testing for item in list
		for ls in submission_list:
			assert isinstance(ls.id, str)
			print(ls.id)


# Todo: Start Unittest
if __name__ == "__main__":

	# Print test
	print('Running')

	# LIB
	lib = LIB()

	# Praw Login
	reddit = Praw.login()

	# Subreddit
	sr = 'funny'

	# Limit
	limit = 4

	# SubmissionFunctions.py Unit Test
	sf = SubmissionFunctionUnitTest(lib, reddit, sr, limit)

	# Cleanup
	lib.end()
