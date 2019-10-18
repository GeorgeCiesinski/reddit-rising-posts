import sys
import signal
import socket
import multiprocessing as MP
import praw

from bin.LIB import LIB
from bin.DataCollector import DataCollector as DC


# used to listen for ^C to gracefully terminate the program
# input: not sure
# output: None
def sig_handler(sig,frame):
    exit()


# Gracefully exit the program, clean ups to be done here
# input: None
# output: None
def exit():
    # Todo: warning: shadows Built-in name exit. Will this be a problem?
    lib.write_log("Exiting..")
    # Close the UDP port
    if in_socket is not None:
        in_socket.close()
    # Kill all processes that were started by the program
    for process in PROCESSLIST:
        process.terminate()
    sys.exit()


# Main of the program
if __name__ == '__main__':
    # Signal Listener
    signal.signal(signal.SIGINT, sig_handler)

    # Create the lib object
    config_file = "config/RedditRisingPost.cfg"
    lib = LIB(cfg=config_file)

    # Read the config file program specific values, and define other variables
    PROCESSLIST = []
    # making the praw_q
    praw_q = MP.Queue()

    # TODO: Get reddit praw login list from database
    reddit = praw.Reddit(
        client_id="Zfl37rh1asVTjQ",
        client_secret="DX87ZhsDhvJrvxdoud0CXmcbLGA",
        username="top10tracket",
        password="k2T%5VuSJc8k",
        user_agent="reddit-rising-posts"
    )
    praw_q.put(reddit)

    # TODO: Start datacollector for known subreddits
    try:
        subreddits = ['funny', 'science','askreddit'] # get  this list from DB
        for subreddit in subreddits:
            lib.write_log("Starting Data Collection for {}".format(subreddit))
            cfg = "config/DataCollection.cfg"
            process_name = "{}_data_collector".format(subreddit)
            process = MP.Process(name=process_name.lower(), target=DC, args=(subreddit, praw_q))
            process.start()
            PROCESSLIST.append(process)
            lib.write_log("Started Data Collection for {}".format(subreddit))
    except Exception as E:
        pass

    # Start a UDP port listener to allow interaction with this application
    # UPS port and communication variables
    HOST = '127.0.0.1'
    PORT = lib.get_args_value("applicationport", 5000)
    ENCODING = lib.get_args_value("charencoding", "utf-8")
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
        exit()
    # Default message return by the application for invalid commands
    NOT_VALID_MESSAGE = "Not Valid input".encode(ENCODING)
    # For each connection (keep looping to listen for new connections)
    # Each new connection is a one time transaction. A request is made, the result is sent, and the connection is closed
    while True:
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

                # TODO: status of all the process is requested
                if (parts[0] == "status") and (len(parts) == 1):
                    return_string = ""
                    if len(PROCESSLIST) == 0:
                        return_string = "No processes"
                        conn.sendall(return_string.encode(ENCODING))
                        conn.close()
                        break
                    for process in PROCESSLIST:
                        if not process.is_alive():
                            return_string = "{}{}\n".format(return_string,"{} not running".format(process.name))
                        else:
                            return_string = "{}{}\n".format(return_string, "{} running".format(process.name))
                    lib.write_log(return_string)
                    conn.sendall(return_string.encode(ENCODING))
                    conn.close()
                    break

                # TODO: status of one process is requested

                # TODO: request to stop the application
                if (parts[0] == "stop") and (len(parts) == 1):
                    return_string = "Stopping application..."
                    lib.write_log(return_string)
                    conn.sendall(return_string.encode(ENCODING))
                    conn.close()
                    in_socket.close()
                    exit()

                # TODO: request to stop a process (data collector)
                if (parts[0] == "stop") and (len(parts) == 2):
                    stop_name = parts[1].lower()
                    return_string = "Stopping {}: ".format(stop_name)
                    return_status = ""
                    try:
                        for process in PROCESSLIST:
                            if process.name ==  "{}_data_collector".format(stop_name):
                                if process.is_alive():
                                    process.terminate()
                                    return_status = "Stopped"
                                    PROCESSLIST.remove(process)
                                else:
                                    return_status = "Stopped"
                                    PROCESSLIST.remove(process)
                            if return_status == "":
                                return_status = "No such process"

                    except Exception as e:
                        return_status = "Failed"
                        error_string = "Could not stop {}".format(stop_name)
                        lib.write_log(error_string)
                        lib.write_error("{} {}".format(error_string,e))
                    return_string = "{}{}".format(return_string,return_status)
                    lib.write_log(return_string)
                    conn.sendall(return_string.encode(ENCODING))
                    conn.close()
                    break

                # TODO: request to start a process (data collector)
                if (parts[0] == "start") and (len(parts) == 2):
                    start_name = parts[1]
                    return_string = "Starting {}: ".format(start_name)
                    start_status = "Started"
                    try:
                        lib.write_log("Starting Data Collection for {}".format(start_name))
                        cfg = "config/DataCollection.cfg"
                        process_name = "{}_data_collector".format(start_name)
                        process = MP.Process(name=process_name.lower(), target=DC, args=(start_name, praw_q))
                        process.start()
                        PROCESSLIST.append(process)
                        lib.write_log("Started Data Collection for {}".format(start_name))
                    except Exception as e:
                        start_status = "Failed"
                        error_string = "Failed to start data collector"
                        lib.write_log(error_string)
                        lib.write_error("{} {}".format(error_string, e))
                    return_string = "{}{}\n".format(return_string,start_status)
                    conn.sendall(return_string.encode(ENCODING))
                    conn.close()
                    break
    exit()

# Don't import this file, run it directly
if __name__ == "RedditRisingPost":
    print("NO IMPORTS")
    sys.exit()
