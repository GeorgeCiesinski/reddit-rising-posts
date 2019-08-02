"""
Comments object: retrieves comments from post
"""

"""
Notes for George:
Invokes PRAW session
PRAW is not thread safe - cannot be shared between multiple threads (according to PRAW documentation)
- Must initiate and close the session in the same thread
- This is why we are making the comment object
- It is also because of data separation: Reddit has their own object they populate with info.
...We are retrieving info from it and bringing it into our own database to prevent problems
"""


class Comments:

    # Get all comments and replies, replace more
    # Input: Post post
    # Output: list of Comment comment
    def get_all_comments(self, post=None):
        pass

    # Get all root comments, comments that have the submission as the parent
    # Input: Post post
    # Output: list of Comment comment
    def get_root_comments(self, post=None):
        pass
