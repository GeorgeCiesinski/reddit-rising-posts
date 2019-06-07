#!/usr/bin/python3.4

#imports 
from datetime import datetime as dt
import time
import sys
import subprocess
import os

class LIB:
	PUNCTUATION = ['"','\'','*']
	HOME = None
	LOG = None
	CFG = None
	ARGS = None
	MSGLIST = []
	def __init__(self, home=None, cfg=None):
		self.write_log("Making lib instance: '{}'".format(home))
		if home == None:
			home = os.getcwd()
			parts = home.split("/")
			if parts[len(parts)-1] == "bin":
				home = "/".join(parts[:len(parts)-1])
		
		self.HOME = home
		
		#check and/or create the project structure
		if self.path_exists(self.HOME) == False:
			self.write_log("Creating path: '{}'".format(self.HOME))
			if self.make_path(self.HOME) == False:
				string = "Unable to create path '{}'".format(self.HOME)
				self.write_log(string)
				self.write_error(string)
		
		self.LOG = "{}/logs".format(self.HOME)
		if self.path_exists(self.LOG) == False:
			self.write_log("Creating path: '{}'".format(self.LOG))
			if self.make_path(self.LOG) == False:
				string = "Unable to create path '{}'".format(self.LOG)
				self.write_log(string)
				self.write_error(string)
		
		self.ARGS = sys.argv
		self.write_log("ARGS: {}".format(self.ARGS))
		if cfg == None:
			cfg = self.get_args_value("-cfg","{}/bin/config.cfg".format(self.HOME))
		if self.read_config(cfg) == -1:
			self.CFG = {}
			self.write_log("No such cfg file, no configs being used")
		else:
			self.write_log("Using Config file: '{}'".format(cfg))

############# Config ###########################
	#read the file in config file format, and populate the CFG dictionary
	#input  : config file
	#output : None
	def read_config(self, cfgFile):
		data = self.read_file(cfgFile)
		if data == -1:
			return -1
		self.CFG = {}
		for line in data:
			line = self.clean_string(line)
			if "#" in line:
				line = line[:line.index("#")]
			if len(line) > 3:
				dic = line.split("=")
				key = self.clean_string(dic[0].lower())
				value = self.clean_string(dic[1])
				
				if value[0] == '"':
					value = self.clean_string(value.replace('"',""))
				elif value[0] == '[':
					mList = value.replace("[","").replace("]","").split(",")
					mList = list(map(self.sanitize_string,mList))
					value = mList
				else:
					try:
						value = int(value)
					except:
						value = self.clean_string(value).lower()

				self.CFG[key] = value
		self.write_log("CFG: '{}'".format(self.CFG))
	
	#get a config key value, if no key exists, the given default value is returned
	#input  : key, default value
	#output : value
	def get_config_value(self, key, default=None):
		data = None
		try:
			data = self.CFG[key.lower()]
		except:
			data = default
		return data
		
########## System Arguments ################
	#get the system argumnets
	#input  : None
	#output : list
	def get_args(self):
		return self.ARGS
	
	#get a system key value, if no key exists, the given default value is returned. value is key index + 1
	#input  : None
	#output : list
	def get_args_value(self, key, default=None):
		args = self.ARGS
		try:
			idx = args.index(key)
			value = args[idx+1]
		except Exception as e:
			value = default
		return value
	
	#ket in system arguments
	#input  : key
	#output : boolean
	def in_args(self, key):
		args = self.ARGS
		if key in args:
			return True
		return False
		
############# IO #####################################
	#read the given file name, retuns a list of lines 
	#input  : filename
	#output : list
	def read_file(self, fileName):
		data = None
		try:
			inFile = open(fileName, "r+")
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return -1
		try:
			data = []
			for line in inFile:
				data.append(line)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return -1
		return data
	
	#Write out put to the log file
	#input  : string
	#output : None
	def write_log(self, string):
		try:
			out = open("{}/output.log".format(self.LOG), 'a+')
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return -1
		
		msg = "{} ~ {}\n".format(self.get_now(), string)
		
		try:
			con = self.get_config_value("console", 0)
			if (con == 1) or (con == 4):
				print(msg)
			out.write(msg)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return -1	

		return 0

	#Write out put to the error file
	#input  : string
	#output : None
	def write_error(self, string):
		try:
			out = open("{}/error.log".format(self.LOG), "a+")
		except:
			return -1
		msg = "{} ~ {}\n".format(self.get_now(), string)
		try:
			con = self.get_config_value("console", 0) 
			if (con == 2) or (con == 4):
				print(msg)
			out.write(msg)
		except:
			return -1
		return 0

	#Write output to a specified file
	#input: filename, string
	#output: None
	def write_file(self, fileName, string):
		try:
			out = open(fileName, "a+")
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return -1
		msg = "{} ~ {}\n".format(self.get_now(), string)
		try:
			out.write(msg)
			con = self.get_config_value("console", 0) 
			if (con == 3) or (con == 4):
				print(msg)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return -1
		return 0

	#Check if the given path already exists
	#input: absolute path TODO: Make relative safe
	#output: boolean
	def path_exists(self, path):
		self.write_log("Check path: {}".format(path))
		try:
			value = os.path.exists(path)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			value = False
		self.write_log("Result: {}".format(value))
		return value
	
	#Create the given path. This is a recursive operation.
	#input: absolute path TODO: Make relative safe
	#output: boolean
	def make_path(self, path):
		self.write_log("Creating path: {}".format(path))
		value = False
		try:
			if not self.path_exists(path):
				os.makedirs(path)
				value = True
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			value = False
		self.write_log("Result: {}".format(value))
		return value
	
	#Run the given os command
	#input: string (system command)
	#ouptput: [command.output, command.error, command.returncode]
	def run_os_cmd(self, cmd):
		tout = self.get_config_value("cmdtimeout", 60)
		if tout != 0:
			cmd = "timeout {} {}".format(tout,cmd)
		self.write_log("Running cmd: '{}'".format(cmd))
		try:
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
			p.wait()
			out, error = p.communicate()
			returnCode = p.poll() 
			self.write_log("Code:{}\n==OUT==\n{}\n==OUT==\n==ERR==\n{}\n==ERR==".format(returnCode,out,error))
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return None
		return [out, error, returnCode]
		
	#Start the given os command as it's on process
	#input: string (system command)
	#output: subprocess.Popen obejct
	def start_process(self, cmd):
		self.write_log("Starting process cmd: '{}'".format(cmd))
		try:
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return None
		return p
		
########## Time Base ################
	#Get the time now
	#input: None
	#ouptput: string
	def get_now(self):
		return str(dt.now()).split(".")[0]
	
	#Convert time stamp to human readable date
	#input: string (timestamp)
	#output: string (human redable format)
	def timestamp_to_date(self, stamp):
		if stamp!=None:
			return str(dt.utcfromtimestamp(stamp)).split(".")[0]
		return None
		
	#Sleep for a given duration
	#input: int (duration)
	#output: none
	def sleep(self, duration):
		self.write_log("Sleeping for {}".format(duration))
		try:
			time.sleep(duration)
		except Exception as e:
			string = "Sleep error: '{}'".format(e)
			lib.write_log("Sleep error")
			lib.write_error(string)
		return
		
########## General Funtions ################
	#clean the given list of strings. Errors result in the same list being returned
	#input: list (of strings)
	#oputput: list (of string)
	def clean_string_list(self, list):
		try:
			mlist = []
			for m in list:
				if (m != "") or (len(m) >= 1):
					mlist.append(self.clean_string(m))
			return mlist
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return list
	
	#clean the given string. Remove newline characters, and strip whitespaces. Errors result in the same string being returned
	#input: string
	#output: string
	def clean_string(self, string):
		try:
			mstring = string.replace("\n","").replace("\r","").strip()
			return mstring
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return string
	
	#sanitize string, remove all punctuations (defined at the top), newlines, and whitespaces
	#input: string
	#output: string
	def sanitize_string(self, instring, black_list=None):
		words = instring.split()
		
		if black_list != None:
			tmp = []
			for word in words:
				if word not in black_list:
					tmp.append(word)
			words = tmp
		
		mstring = []
		for word in words:
			mword = []
			for char in word:
				if char not in self.PUNCTUATION:
					mword.append(char)
			mstring.append("".join(mword))
		string = self.clean_string(" ".join(mstring))
		self.write_log("Sanitized string: {}".format(string))
		return string