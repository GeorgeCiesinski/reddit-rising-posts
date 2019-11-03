import praw
import unittest
from SubmissionFunctions import get_hot
from SubmissionFunctions import get_rising
from SubmissionFunctions import get_top


class Praw:

	@staticmethod
	def login():
		reddit = praw.Reddit(
			client_id='nrE5x4yJ_LUo9Q',
			client_secret='m8ItmlnLRlJ6GVVS1KD5tWsvhsQ',
			user_agent='cussbot by /u/th1nker',
			username='cussbot',
			password='SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS'
		)

		return reddit


# Todo: Write test cases for SubmissionFunctions.py
class SubmissionFunctionUnitTest(unittest.TestCase):
	"""Test for SubmissionFunctions.py"""

	def __init__(self, reddit):
		pass

	def get_hot_test(self, reddit):
		pass

	def get_rising_test(self, reddit):
		pass

	def get_top_test(self, reddit):
		pass


# Todo: Start Unittest
if __name__ == "__init__":

	# Praw Login
	reddit = Praw.login()

	# SubmissionFunctions.py Unit Test
	sf = SubmissionFunctionUnitTest(reddit)
