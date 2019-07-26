#!/usr/bin/python3.4

import sys
import signal
import multiprocessing as MP

from LIB3 import LIB

# used to listen for ^C to gracefully terminate the program
# input: not sure
# output: None
def sig_handler(sig,frame):
	exit()

# Gracefully exit the program, clean ups to be done here
# input: None
# output: None
def exit():
	lib.write_log("Exiting..")
	#kill all processes that were started by the program
	for process in PROCESSLIST:
		process.terminate()
	sys.exit()

# Main of the program
if __name__ == '__main__':
	# Signal Listener
	signal.signal(signal.SIGINT, sig_handler)

	# Create the lib object
	config_file = "RedditRisingPost.cfg"
	lib = LIB(cfg=config_file)

	# Read the config file program specific values, and define other variables
	MaxSearchingThreads = lib.get_config_value("MaxSearchingThreads", 5)
	MaxCollectionThreads = lib.get_config_value("MaxCollectionThreads", 10)
	MaxTrackingThreads = lib.get_config_value("MaxTrackingThreads", 2)
	PROCESSLIST = []


	# TODO: makesure all the threads started are still running
	while True:
		print(lib.get_config_value("MaxSearchingThreads", 5))
		try:
			print(confi_reloader.is_alive())
		except:
			print("no process")
		lib.sleep(5)

	
# Don't import this file, run it directly
if __name__ == "RedditRisingPost":
	print("NO IMPORTS")
	sys.exit()
