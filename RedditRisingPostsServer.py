import sys
import signal
import socket
import multiprocessing as MP

from bin.LIB import LIB
from bin.SubredditDBPull import SubredditDBPull
from bin.SubmissionPrawPull import SubmissionPrawPull
from bin.SubmissionDBPull import SubmissionDBPull
from bin.SubmissionDBPush import SubmissionDBPush
from bin.SubmissionSnapshotDBPush import SubmissionSnapshotDBPush
from bin.CommentDBPush import CommentDBPush
from bin.CommentSnapshotDBPush import CommentSnapshotDBPush
from bin.DAL import *

# used to listen for ^C to gracefully terminate the program
# input: not sure
# output: None
def sig_handler(sig,frame):
    main_exit()

def db_cleanups():
    """
    Clean up the DB schedules, and release the used logings
    :param my_db_connection: db connection
    :return:
    """
    with Pg.pg_connect("MAIN_REDDIT_RISING_POSTS") as my_db_connection:
        Queue.submission_schedule_release(my_db_connection)
        Queue.subreddit_schedule_release(my_db_connection)
        Praw.praw_login_release(my_db_connection)

# Gracefully exit the program, clean ups to be done here
# input: None
# output: None
def main_exit():
    # Todo: warning: shadows Built-in name exit. Will this be a problem?
    lib.write_log("Exiting..")
    # Close the UDP port
    if in_socket is not None:
        in_socket.close()
    # Kill all processes that were started by the program
    for key in PROCESSLIST:
        lib.write_log("Stopping process: {}".format(key))
        running_process = PROCESSLIST[key]
        print("Killing pid : {}".format(running_process.pid))
        running_process.terminate()
    db_cleanups()
    lib.end()
    sys.exit()

def start_subreddit_db_pull():
    # TODO: Start subreddit db pull processs
    lib.read_config(lib.USING_CONFIG_FILE)
    # Read for the config how many process should be running
    process_start_count = lib.get_config_value("subredditdbpullprocesscount", 1)
    if type(process_start_count) is not int:
        process_start_count = 1

    # Calculate the running and start process difference
    currently_running_process_count = 0
    for process_key in PROCESSLIST:
        if "subreddit_db_pull_" in process_key:
            currently_running_process_count += 1
    # action the results
    if currently_running_process_count != process_start_count:
        process_count_different = currently_running_process_count - process_start_count
        # TODO: Start the difference
        if process_count_different < 0:
            for x in range(0, abs(process_count_different), 1):
                process_name = "subreddit_db_pull_{}_{}".format(x, lib.get_now().replace(" ", "_").replace(":", "_").replace(".", "_"))
                new_process = MP.Process(name=process_name.lower(), target=SubredditDBPull,
                                         args=(process_name, submission_praw_pull_q,))
                new_process.start()
                lib.write_log("Staring process {} {}".format(process_name, new_process.pid))
                PROCESSLIST[process_name] = new_process
        # TODO: shutdown the difference
        elif process_count_different > 0:
            shutdown_count = 0
            stop_list = []
            for x in PROCESSLIST:
                if shutdown_count is not abs(process_count_different):
                    if "subreddit_db_pull_" in x:
                        shutdown_count += 1
                        tmp_process = PROCESSLIST[x]
                        lib.write_log("Stopping {}".format(x))
                        tmp_process.terminate()
                        stop_list.append(x)
            for remove_process_from_list in stop_list:
                del PROCESSLIST[remove_process_from_list]

def start_submission_parw_pull():
    # TODO: Start submission praw pull processs (for the subreddit)
    lib.read_config(lib.USING_CONFIG_FILE)
    # Read for the config how many process should be running
    process_start_count = lib.get_config_value("submissionprawpullprocesscount", 1)
    if type(process_start_count) is not int:
        process_start_count = 1

    # Calculate the running and start process difference
    currently_running_process_count = 0
    for process_key in PROCESSLIST:
        if "submission_praw_pull" in process_key:
            currently_running_process_count += 1
    # action the results
    if currently_running_process_count != process_start_count:
        process_count_different = currently_running_process_count - process_start_count
        # TODO: Start the difference
        if process_count_different < 0:
            for x in range(0, abs(process_count_different), 1):
                process_name = "submission_praw_pull_{}_{}".format(x, lib.get_now().replace(" ", "_").replace(":", "_").replace(".", "_"))
                new_process = MP.Process(name=process_name.lower(), target=SubmissionPrawPull, args=(
                process_name, submission_praw_pull_q, submission_db_push_q, comment_db_push_q,))
                new_process.start()
                lib.write_log("Staring process {} {}".format(process_name, new_process.pid))
                PROCESSLIST[process_name] = new_process
        # TODO: shutdown the difference
        elif process_count_different > 0:
            shutdown_count = 0
            stop_list = []
            for x in PROCESSLIST:
                if shutdown_count is not abs(process_count_different):
                    if "submission_praw_pull" in x:
                        shutdown_count += 1
                        tmp_process = PROCESSLIST[x]
                        lib.write_log("Stopping {}".format(x))
                        tmp_process.terminate()
                        stop_list.append(x)
            for remove_process_from_list in stop_list:
                del PROCESSLIST[remove_process_from_list]

def start_submission_snapshot_db_push():
    # TODO: Start submission snapshot db push processs (for the subreddit)
    lib.read_config(lib.USING_CONFIG_FILE)
    # Read for the config how many process should be running
    process_start_count = lib.get_config_value("submissionsnapshotdbpushprocesscount", 1)
    if type(process_start_count) is not int:
        process_start_count = 1

    # Calculate the running and start process difference
    currently_running_process_count = 0
    for process_key in PROCESSLIST:
        if "submission_snapshot_db_push" in process_key:
            currently_running_process_count += 1
    # action the results
    if currently_running_process_count != process_start_count:
        process_count_different = currently_running_process_count - process_start_count
        # TODO: Start the difference
        if process_count_different < 0:
            for x in range(0, abs(process_count_different), 1):
                process_name = "submission_snapshot_db_push_{}_{}".format(x, lib.get_now().replace(" ", "_").replace(":", "_").replace(".", "_"))
                new_process = MP.Process(name=process_name.lower(), target=SubmissionSnapshotDBPush, args=(
                    process_name, comment_db_push_q,))
                new_process.start()
                lib.write_log("Staring process {} {}".format(process_name, new_process.pid))
                PROCESSLIST[process_name] = new_process
        # TODO: shutdown the difference
        elif process_count_different > 0:
            shutdown_count = 0
            stop_list = []
            for x in PROCESSLIST:
                if shutdown_count is not abs(process_count_different):
                    if "submission_snapshot_db_push" in x:
                        shutdown_count += 1
                        tmp_process = PROCESSLIST[x]
                        lib.write_log("Stopping {}".format(x))
                        tmp_process.terminate()
                        stop_list.append(x)
            for remove_process_from_list in stop_list:
                del PROCESSLIST[remove_process_from_list]

def start_comment_db_push():
    # TODO: Start comment db push processs (for the subreddit)
    lib.read_config(lib.USING_CONFIG_FILE)
    # Read for the config how many process should be running
    process_start_count = lib.get_config_value("commentdbpushprocesscount", 1)
    if type(process_start_count) is not int:
        process_start_count = 1

    # Calculate the running and start process difference
    currently_running_process_count = 0
    for process_key in PROCESSLIST:
        if "comment_db_push" in process_key:
            currently_running_process_count += 1
    # action the results
    if currently_running_process_count != process_start_count:
        process_count_different = currently_running_process_count - process_start_count
        # TODO: Start the difference
        if process_count_different < 0:
            for x in range(0, abs(process_count_different), 1):
                process_name = "comment_db_push_{}_{}".format(x, lib.get_now().replace(" ", "_").replace(":", "_").replace(".", "_"))
                new_process = MP.Process(name=process_name.lower(), target=CommentDBPush, args=(
                    process_name, comment_db_push_q,))
                new_process.start()
                lib.write_log("Staring process {} {}".format(process_name, new_process.pid))
                PROCESSLIST[process_name] = new_process
        # TODO: shutdown the difference
        elif process_count_different > 0:
            shutdown_count = 0
            stop_list = []
            for x in PROCESSLIST:
                if shutdown_count is not abs(process_count_different):
                    if "comment_db_push" in x:
                        shutdown_count += 1
                        tmp_process = PROCESSLIST[x]
                        lib.write_log("Stopping {}".format(x))
                        tmp_process.terminate()
                        stop_list.append(x)
            for remove_process_from_list in stop_list:
                del PROCESSLIST[remove_process_from_list]


def start_comment_snapshot_db_push():
    # TODO: Start comment snapshot db push processs (for the subreddit)
    lib.read_config(lib.USING_CONFIG_FILE)
    # Read for the config how many process should be running
    process_start_count = lib.get_config_value("commentsnapshotdbpushprocesscount", 1)
    if type(process_start_count) is not int:
        process_start_count = 1

    # Calculate the running and start process difference
    currently_running_process_count = 0
    for process_key in PROCESSLIST:
        if "comment_snapshot_db_push" in process_key:
            currently_running_process_count += 1
    # action the results
    if currently_running_process_count != process_start_count:
        process_count_different = currently_running_process_count - process_start_count
        # TODO: Start the difference
        if process_count_different < 0:
            for x in range(0, abs(process_count_different), 1):
                process_name = "comment_snapshot_db_push_{}_{}".format(x, lib.get_now().replace(" ", "_").replace(":", "_").replace(".", "_"))
                new_process = MP.Process(name=process_name.lower(), target=CommentSnapshotDBPush, args=(
                    process_name, comment_db_push_q,))
                new_process.start()
                lib.write_log("Staring process {} {}".format(process_name, new_process.pid))
                PROCESSLIST[process_name] = new_process
        # TODO: shutdown the difference
        elif process_count_different > 0:
            shutdown_count = 0
            stop_list = []
            for x in PROCESSLIST:
                if shutdown_count is not abs(process_count_different):
                    if "comment_snapshot_db_push" in x:
                        shutdown_count += 1
                        tmp_process = PROCESSLIST[x]
                        lib.write_log("Stopping {}".format(x))
                        tmp_process.terminate()
                        stop_list.append(x)
            for remove_process_from_list in stop_list:
                del PROCESSLIST[remove_process_from_list]


def process_count_update():
    '''
    get the process counts that are running and ensure that is whats configured in the config file;;
    :param my_db_connection: the database connection for this main server process
    :return: None
    '''

    #print("process_count_update")

    #start the subreddit db pull process
    start_subreddit_db_pull()

    #start the submission praw pull process
    start_submission_parw_pull()

    # TODO:  Start submission db push processs

    # TODO: Start submission db pull processs

    # TODO: start submission snapshot praw pull process

    # TODO: start submission snapshot db push process
    start_submission_snapshot_db_push()

    # TODO: start comment db push process
    start_comment_db_push()

    # TODO: start comment db pull process

    # TODO: start comment snapshot praw pull process

    # TODO: start comment snapshot db push process
    start_comment_snapshot_db_push()

    # TODO: Start subreddit scheduler

    # TODO: Start submission scheduler
    


# Main of the program
if __name__ == '__main__':
    # Signal Listener
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    # Create the lib object
    config_file = "config/RedditRisingPostsServer.cfg"
    lib = LIB(cfg=config_file)

    PROCESSLIST = {}

    #make all nessary queues for processs
    submission_praw_pull_q = MP.Queue()
    submission_db_push_q = MP.Queue()

    submission_snapshot_praw_pull_q = MP.Queue()
    submission_snapshot_db_push_q = MP.Queue()

    comment_praw_pull_q = MP.Queue()

    comment_db_push_q = MP.Queue()

    comment_snapshot_praw_pull_q = MP.Queue()
    comment_snapshot_db_push_q = MP.Queue()


    #Make my db connection

    #TODO: Clear in DB -- subreddit_schedule, submission_schedule, comment_schedule, praw_logs
    db_cleanups()

    #TODO: start all processes by count defined in the config file
    process_count_update()

    # Start a UDP port listener to allow interaction with this application
    # UPS port and communication variables
    HOST = ''
    PORT = lib.get_args_value("applicationport", 5000)
    ENCODING = lib.get_args_value("charencoding", "utf-8")
    in_socket = None
    try:
        # Make the UPD port
        in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        in_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        in_socket.bind((HOST, PORT))
        in_socket.listen()
    except Exception as e:
        error_string = "Could not start UDP port listener"
        lib.write_log(error_string)
        lib.write_error("{} {}".format(error_string,e))
        main_exit()
    # Default message return by the application for invalid commands
    NOT_VALID_MESSAGE = "Not Valid input".encode(ENCODING)
    # For each connection (keep looping to listen for new connections)

   #TODO: Break out below to functions ###############
    ###############

    ## def process_list (print process_object)
        ## get each process status and print to screen
    ## def process_restart (print process_object)
        ## send and wait for process to stop
        ## update the import for that file
        ## start the process

    # Each new connection is a one time transaction. A request is made, the result is sent, and the connection is closed
    while True:
        if in_socket is None:
            main_exit()
        conn, addr = in_socket.accept()
        lib.write_log("Connected with: {}".format(addr))
        with conn:
            while True:
                # Get data from connection
                data = conn.recv(1024)
                if not data:
                    break
                # Decode the message from bytes to string
                m_data = data.decode(ENCODING).lower()
                parts = m_data.split(" ")
                lib.write_log("Request: {}".format(parts))

                # TODO: ensure there is some data to action
                if len(parts) < 1:
                    conn.sendall(NOT_VALID_MESSAGE)
                    conn.close()
                    break

                if len(parts) == 1:
                    # TODO: request to server commands
                    if parts[0] == "help":
                        return_string = "Commands..\n"
                        return_string = "{} help -- list this outputr\n".format(return_string)
                        return_string = "{} stop -- stop the server\n".format(return_string)
                        return_string = "{} stop (process name) -- not available\n".format(return_string)
                        return_string = "{} start (sub reddit name) -- not available\n".format(return_string)
                        return_string = "{} status -- return the status of all the process\n".format(return_string)
                        return_string = "{} update_processes -- Update the process count\n".format(return_string)
                        return_string = "{} queue_size -- List the size of all the queues\n".format(return_string)
                        lib.write_log(return_string)
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        break

                    # TODO: status of all the process is requested
                    if parts[0] == "status":
                        return_string = ""
                        if len(PROCESSLIST) == 0:
                            return_string = "No processes"
                            conn.sendall(return_string.encode(ENCODING))
                            conn.close()
                            break
                        for key in PROCESSLIST:
                            process = PROCESSLIST[key]
                            if not process.is_alive():
                                return_string = "{}{}\n".format(return_string,"{} not running".format(process.name))
                            else:
                                return_string = "{}{}\n".format(return_string, "{} running".format(process.name))
                        lib.write_log(return_string)
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        break

                    #TODO: update process count
                    if parts[0] == "update_processes":
                        return_string = ""
                        process_count_update()
                        if len(PROCESSLIST) == 0:
                            return_string = "No processes"
                            conn.sendall(return_string.encode(ENCODING))
                            conn.close()
                            break
                        for key in PROCESSLIST:
                            process = PROCESSLIST[key]
                            if not process.is_alive():
                                return_string = "{}{}\n".format(return_string, "{} not running".format(process.name))
                            else:
                                return_string = "{}{}\n".format(return_string, "{} running".format(process.name))
                        lib.write_log(return_string)
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        break

                    # TODO: request to stop the application
                    if parts[0] == "stop":
                        return_string = "Stopping application..."
                        lib.write_log(return_string)
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        in_socket.close()
                        main_exit()

                    if parts[0] == "queue_size":
                        return_string = ""

                        try:
                            return_string = "{}submission_praw_pull_q = {}\n".format(return_string, submission_praw_pull_q.qsize())
                        except:
                            return_string = "{}submission_praw_pull_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}submission_db_push_q = {}\n".format(return_string, submission_db_push_q.qsize())
                        except:
                            return_string = "{}submission_db_push_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}submission_snapshot_praw_pull_q = {}\n".format(return_string, submission_snapshot_praw_pull_q.qsize())
                        except:
                            return_string = "{}submission_snapshot_praw_pull_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}submission_snapshot_db_push_q = {}\n".format(return_string, submission_snapshot_db_push_q.qsize())
                        except:
                            return_string = "{}submission_snapshot_db_push_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}comment_praw_pull_q = {}\n".format(return_string, comment_praw_pull_q.qsize())
                        except:
                            return_string = "{}comment_praw_pull_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}comment_db_push_q = {}\n".format(return_string, comment_db_push_q.qsize())
                        except:
                            return_string = "{}comment_db_push_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}comment_snapshot_praw_pull_q = {}\n".format(return_string, comment_snapshot_praw_pull_q.qsize())
                        except:
                            return_string = "{}comment_snapshot_praw_pull_q = {}\n".format(return_string, "Unknown")

                        try:
                            return_string = "{}comment_snapshot_db_push_q = {}\n".format(return_string, comment_snapshot_db_push_q.qsize())
                        except:
                            return_string = "{}comment_snapshot_db_push_q = {}\n".format(return_string, "Unknown")

                        lib.write_log(return_string)
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        break

                if len(parts) == 2:
                    # TODO: request to stop a process (data collector)
                    if parts[0] == "stop":
                        return_string = "No avalible"
                        lib.write_log(return_string)
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        break

# Don't import this file, run it directly
if __name__ == "RedditRisingPost":
    print("NO IMPORTS")
    sys.exit()
