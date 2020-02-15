import praw
from bin.DAL.Praw import Praw
from bin.DAL.Pg import Pg
from bin.Submission import Submission
import bin.SubmissionFunctions as SubmissionFunctions
import bin.CommentFunctions as CommentFunctions
from bin.LIB import LIB


class zPraw:

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


class SubmissionFunctionUnitTest():
    """Test for SubmissionFunctions.py"""

    def __init__(self, lib, reddit, sr, submission, limit):

        # Prints test name
        print('\nTesting results for SubmissionFunctions.py : ')

        # Tests get_hot
        self.test_get_hot(lib, reddit, sr, limit)

        # Tests get_rising
        self.test_get_rising(lib, reddit, sr, limit)

        # Tests get_top
        self.test_get_top(lib, reddit, sr, limit)

        # Tests submission_snapshot_praw_pull
        self.test_submission_snapshot_praw_pull(lib, reddit, submission)

        # Tests submission_snapshot_db_push
        self.test_submission_snapshot_db_push(lib, submission)

        pass

    @staticmethod
    def test_get_hot(lib, reddit, subreddit, limit):

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
    def test_get_rising(lib, reddit, subreddit, limit):

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
    def test_get_top(lib, reddit, subreddit, limit):

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
    def test_submission_snapshot_praw_pull(lib, reddit, submission):

        # Gets snapshot of submission
        snapshot = SubmissionFunctions.submission_snapshot_praw_pull(lib, reddit, submission)

        # Testing
        assert snapshot.id == submission.id
        assert isinstance(snapshot.title, str)

        # Print Results
        print('\nResults of submission_snapshot_praw_pull: ')
        print(snapshot.id)
        print(snapshot.title)

    @staticmethod
    def test_submission_snapshot_db_push(lib, submission):

        with Pg.pg_connect() as db:
            test_result = SubmissionFunctions.submission_snapshot_db_push(lib, db, submission)

        print('\nResults of submission_snapshot_db_push: ')
        print(f"Insert successful: {test_result}")


class CommentFunctionsUnitTest():
    """Test for CommentFunctions.py"""

    def __init__(self, lib, submission, replace_more):

        # Prints test name
        print('\nTesting results for CommentFunctions.py : ')

        # Tests get_all_comments
        self.test_get_all_comments(lib, submission, replace_more)

        # Tests get_root_comments
        self.test_get_root_comments(lib, submission)

        # tests comment_db_push
        #self.test_comment_db_push(lib, submission)

        # tests comment_snapshot_db_push
        #self.test_comment_snapshot_db_push(lib, submission)

    @staticmethod
    def test_get_all_comments(lib, submission, replace_more):

        # Gets Comment List
        comment_list = CommentFunctions.get_all_comments(lib, submission, replace_more)

        # Testing
        assert isinstance(comment_list, list)

        # Print a few comments

        print('\nResults of get_all_comments')
        for x in range(4):
            print(comment_list[x].id)

        print(f'The total number of comments is: {len(comment_list)}')

    @staticmethod
    def test_get_root_comments(lib, submission):

        # Gets Comment List
        comment_list = CommentFunctions.get_root_comments(lib, submission)

        # Testing
        assert isinstance(comment_list, list)

        # Print a few comments
        print('\nResults of get_root_comments')
        for x in range(4):
            print(comment_list[x].id)

        print(f'The total number of root comments is: {len(comment_list)}')

    @staticmethod
    def test_comment_db_push(lib, submission):

        with Pg.pg_connect() as db:

            test_result = CommentFunctions.comment_db_push(lib, db, submission)

        print('\nResults of comment_db_push: ')
        print(f"Upsert successful: {test_result}")

    @staticmethod
    def test_comment_snapshot_db_push(lib, submission):

        with Pg.pg_connect() as db:
            test_result = CommentFunctions.comment_snapshot_db_push(lib, db, submission)

        print('\nResults of comment_snapshot_db_push: ')
        print(f"Upsert successful: {test_result}")

if __name__ == "__main__":
    """
    Universal settings
    """

    # LIB
    lib = LIB()

    # praw = zPraw.login()

    # Todo: Make this work consistently. Sometimes works, sometimes doesn't. Unreliable for testing at this time.
    # Praw Login
    # Opens connection to db, gets praw login, and closes connection
    with Pg.pg_connect() as db:
        praw = Praw.praw_login_get(lib,db)

    # Submission ID
    sub_id = 'ezgp2e'

    # Submission object
    submission_praw = praw.submission(sub_id)  # Returns praw submission object
    submission = Submission(lib, submission_praw)  # Creates our own submission object

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

    replace_more = 32

    """
    Testing Classes
    """

    # SubmissionFunctions.py Unit Test
    sf = SubmissionFunctionUnitTest(lib, praw, sr, submission, limit)
    cf = CommentFunctionsUnitTest(lib, submission, replace_more)

    # Cleanup
    lib.end()

    # Release login
    Praw.praw_login_release(db)