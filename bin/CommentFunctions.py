from bin.Comment import Comment

"""
Comments object: retrieves comments from post
"""


def get_all_comments(lib=None, praw_instance=None, submission=None, replace_more_limit=None):
    """
    Get all comments and replies using PRAW

    :param lib: Anu's Lib
    :param praw_instance: PRAW object
    :param submission: Specified submission
    :param replace_more_limit: Max number of MoreComments to replace
    :return: List of comments
    :rtype: list
    """
    # Ensure lib, praw_instance and post are not none
    if (lib is None) or (praw_instance is None) or (submission is None):
        return None
    lib.write_log("Getting all comments from the post {}".format(submission.id))
    # Get all comments from post (replace more)
    try:
        praw = praw_instance
        comments = submission.comments
        # Replace MoreComments to include them in comments
        comments.replace_more(limit=replace_more_limit)
    except Exception as e:
        lib.write_log("Failed to get all comments from post due to the exception: {}".format(str(e)))
        return None
    # Creates empty comment list
    comment_list = []
    # Make Comment objects
    # .list() lists all levels of comments
    # Adds comments to comment_list
    for comment in comments.list():
        c = Comment(comment)
        comment_list.append(c)
        lib.write_log(c.id)
    lib.write_log("Completed comments from post {}".format(submission.id))
    # Return list of all comments
    return comment_list


def get_root_comments(lib=None, praw_instance=None, submission=None):
    """
    Get all root comments, comments that have the submission as the parent

    :param lib: Anu's lib file
    :param praw_instance: PRAW object
    :param submission: Specified submission file
    :return: List of comments
    :rtype: list
    """
    # Ensure lib, praw_instance and post are not none
    if (lib is None) or (praw_instance is None) or (submission is None):
        return None
    lib.write_log("Getting all top-level comments from the post {}".format(submission.id))
    # Get all top-level comments from post
    try:
        praw = praw_instance
        comments = submission.comments
        # Remove all MoreComments
        comments.replace_more(limit=0)
    except Exception as e:
        lib.write_log("Failed to get top-level comments from post due to the exception: {}".format(str(e)))
        return None
    comment_list = []
    # Make Comment objects
    for comment in comments:
        c = Comment(comment)
        comment_list.append(c)
        lib.write_log(c.id)
    lib.write_log("Completed top-level comments from post {}".format(submission.id))
    # Return list of all comments
    return comment_list


def get_snapshot(lib=None, praw_q=None, comment_id=None):
    pass
