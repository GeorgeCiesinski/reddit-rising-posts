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


# Get all comments and replies, replace more
# Input: LIB lib, MP Queue, Post post
# Output: list of Comment comment
def get_all_comments(lib=None, praw_instance=None, post=None):
    # TODO: Ensure lib, praw_instance and post are not none
    if (lib is None) or (praw_instance is None) or (post is None):
        return None
    # TODO: Get all comments from post (replace more)

    # TODO: Make Comment objects

    # TODO: Put praw instance back into queue

    # TODO: Return list of all comments

    pass


# Get all root comments, comments that have the submission as the parent
# Input: LIB lib, MP Queue, Post post
# Output: list of Comment comment
def get_root_comments(lib=None, praw_instance=None, post=None):
    # TODO: Ensure lib, praw_instance and post are not none
    if (lib is None) or (praw_instance is None) or (post is None):
        return None
    # TODO: Get all root comments from post (if parent id is the post id)

    # TODO: Make Comment objects

    # TODO: Put praw instance back into queue

    # TODO: Return list of all comments

    pass
