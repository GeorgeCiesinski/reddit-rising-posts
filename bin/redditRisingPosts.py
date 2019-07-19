#!/usr/bin/python3.4

import sys
import signal
import multiprocessing as MP

from LIB3 import LIB


def sig_handler(sig,frame):
	exit()


def exit():
	lib.write_log("Exiting..")
	
	for process in PROCESSLIST:
		process.terminate()
	
	sys.exit()


def reload_config(lib, config_file):
	while True:
		lib.write_log("Reloading confing '{}'".format(config_file))
		lib.read_config(config_file)
		lib.write_log("Reloading done")
		lib.sleep(lib.get_config_value("ConfigReloadInterval",60))


if __name__ == '__main__':
	config_file = "RedditRisingPost.cfg"
	lib = LIB(cfg=config_file)
	
	signal.signal(signal.SIGINT, sig_handler)
	
	MaxSearchingThreads = lib.get_config_value("MaxSearchingThreads", 5)
	MaxCollectionThreads = lib.get_config_value("MaxCollectionThreads", 10)
	MaxTrackingThreads = lib.get_config_value("MaxTrackingThreads", 2)
	PROCESSLIST = []

	# All threads are started one by one here#
	
	# TODO: start thread(s) to determin data collection period. periods (minutes) [5,10,30,60,120,320,720,1440,2880, archive]

	# TODO: start thread(s) to collect submission details

	# TODO: start thread(s) to collect submission summary
	
	# TODO: start thread(s) to collect comment details

	# TODO: start thread(s) to collect comment summary
	
	# TODO: start config reloader
	confi_reloader = MP.Process(target=reload_config, args=(lib,config_file,))
	confi_reloader.start()
	PROCESSLIST.append(confi_reloader)
	
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
