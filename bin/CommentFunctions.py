from bin.Comment import Comment
from bin.DAL.Comment import Comment as DalComment

"""
Comments object: retrieves comments from post
"""


def get_all_comments(lib=None, submission=None, replace_more_limit=None):
    """
    Get all comments and replies using PRAW

    :param lib: Anu's Library
    :param submission: Submission object
    :param replace_more_limit: Max number of MoreComments to replace
    :return comment_list: List of comments
    :rtype list:
    """

    # Ensure lib and submission are not none
    if (lib is None) or (submission is None):
        return None

    lib.write_log("Getting all comments from the post {}".format(submission.id))

    # Get all comments from post (replace more)
    try:
        comments = submission.comments
        comments.replace_more(limit=replace_more_limit)  # Replace MoreComments to include them in comments
    except Exception as e:
        lib.write_log("Failed to get all comments from post due to the exception: {}".format(str(e)))
        return None
    else:
        lib.write_log("Successfully retrieved all comments from the post.")

    comment_list = []  # Creates empty comment list

    # Make Comment objects | .list() lists all levels of comments
    for comment in comments.list():
        c = Comment(comment)
        comment_list.append(c)  # Adds comments to comment_list
        lib.write_log(c.id)

    lib.write_log("Completed comments from post {}".format(submission.id))

    return comment_list  # Return list of all comments


def get_root_comments(lib=None, submission=None):
    """
    Get all root comments, comments that have the submission as the parent

    :param lib: Anu's library
    :param submission: Submission object
    :return comment_list: List of comments
    :rtype list:
    """

    # Ensure lib and submission are not none
    if (lib is None) or (submission is None):
        return None

    lib.write_log("Getting all top-level comments from the post {}".format(submission.id))

    # Get all top-level comments from post
    try:
        comments = submission.comments
        comments.replace_more(limit=0)  # Remove all MoreComments
    except Exception as e:
        lib.write_log("Failed to get top-level comments from post due to the exception: {}".format(str(e)))
        return None
    else:
        lib.write_log("Successfully retrieved top-level comments from the post.")

    comment_list = []

    # Make Comment objects
    for comment in comments:
        c = Comment(comment)
        comment_list.append(c)
        lib.write_log(c.id)

    lib.write_log("Completed top-level comments from post {}".format(submission.id))

    return comment_list  # Return list of all comments


def comment_db_push(lib=None, pg=None, submission=None):
    """
    Sends a snapshot of submission comments to comment_detail_upsert to collect detailed data.

    :param lib: Anu's library
    :param pg: Postgress Object
    :param submission: Submission object
    :return upsert_result: Returns true if upsert is completely successful
    :rtype bool:
    """

    # Ensure lib, pg, and submission are not none
    if (lib is None) or (pg is None) or (submission is None):
        return None

    upsert_result = True  # Remains true as long as no comment upsert fails

    # Get comment list // Gets root comments. Can get all comments, but must provide replace_more variable.
    # comment_list = get_root_comments(lib, submission)
    comment_list = get_all_comments(lib, submission, 32)

    # Loop through comments in comment list
    for comment in comment_list:

        successful_upsert = DalComment.comment_detail_upsert(pg, comment)  # Upsert comment

        if not successful_upsert:

            lib.write_log(f"Failed to upsert comment: {comment.id}")  # Log if unsuccessful

            upsert_result = False  # Upsert has failed one or more comments

    return upsert_result


def comment_snapshot_db_push(lib=None, pg=None, submission=None):
    """
    Sends a snapshot of submission comments to comment_snapshot_insert to collect snapshot.

    :param lib: Anu's library
    :param pg: Postgress object
    :param submission: Submission object
    :return insert_result: Returns true if upsert is completely successful
    :rtype bool:
    """

    # Ensure lib, pg, and submission are not none
    if (lib is None) or (pg is None) or (submission is None):
        return None

    insert_result = True  # Remains true as long as no comment upsert fails

    # Get comment list // Gets root comments. Can get all comments, but must provide replace_more variable.
    # comment_list = get_root_comments(lib, submission)
    comment_list = get_all_comments(lib, submission, 32)

    # Loop through comments in comment list
    for comment in comment_list:

        successful_upsert = DalComment.comment_snapshot_insert(pg, comment)  # Insert Comment

        if not successful_upsert:

            lib.write_log(f"Failed to upsert comment: {comment.id}")  # Log if unsuccessful

            insert_result = False  # Upsert has failed one or more comments

    return insert_result
