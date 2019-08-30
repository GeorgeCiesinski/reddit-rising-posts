from bin.Comment import Comment
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
def get_all_comments(lib=None, praw_instance=None, submission_id=None, replace_more_limit=None):
    # TODO: Ensure lib, praw_instance and post are not none
    if (lib is None) or (praw_instance is None) or (submission_id is None):
        return None
    lib.write_log("Getting all comments from the post {}".format(submission_id))
    praw = praw_instance
    # TODO: Get all comments from post (replace more)
    submission = praw.submission(id=submission_id)
    comments = submission.comments
    # Replace MoreComments to include them in comments
    comments.replace_more(limit=replace_more_limit)
    comment_list = []
    # TODO: Make Comment objects
    # .list() lists all levels of comments
    for comment in comments.list():
        c = Comment(comment)
        comment_list.append(c)
        lib.write_log(c.id)
    lib.write_log("Completed comments from post {}".format(submission_id))
    # TODO: Return list of all comments
    return comment_list


# Get all root comments, comments that have the submission as the parent
# Input: LIB lib, MP Queue, Post post
# Output: list of Comment comment
def get_root_comments(lib=None, praw_instance=None, submission_id=None):
    # TODO: Ensure lib, praw_instance and post are not none
    if (lib is None) or (praw_instance is None) or (submission_id is None):
        return None
    lib.write_log("Getting all top-level comments from the post {}".format(submission_id))
    praw = praw_instance
    # TODO: Get all top-level comments from post
    submission = praw.submission(id=submission_id)
    comments = submission.comments
    # Remove all MoreComments
    comments.replace_more(limit=0)
    comment_list = []
    # TODO: Make Comment objects
    for comment in comments:
        c = Comment(comment)
        comment_list.append(c)
        lib.write_log(c.id)
    lib.write_log("Completed top-level comments from post {}".format(submission_id))
    # TODO: Return list of all comments
    return comment_list
