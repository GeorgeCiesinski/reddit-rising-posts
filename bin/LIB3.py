#!/usr/bin/python3.4

#imports 
from datetime import datetime as dt
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
	def __init__(self, home=None, cfgFile=None):
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
		if cfgFile == None:
			cfgFile = self.get_args_value("-cfg","{}/bin/config.cfg".format(self.HOME))
		if self.read_config(cfgFile) == -1:
			self.CFG = {}
			self.write_log("No such cfg file, no configs being used")
		else:
			self.write_log("Using Config file: '{}'".format(cfgFile))

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
	def get_config_value(self, key, default):
		data = None
		try:
			data = self.CFG[key]
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
	def get_args_value(self, key, default):
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

	def path_exists(self, path):
		try:
			value = os.path.exists(path)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			value = Flase
		return value
	
	def make_path(self, path):
		try:
			if not self.path_exists(path):
				os.makedirs(path)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return False
		return True
	
	def run_os_cmd(self, cmd):
		self.write_log("Running cmd: '{}'".format(cmd))
		tOut = self.get_config_value("cmdtimeout", 60)
		if tout != 0:
			cmd = "timeout {} {}".format(tout,cmd)
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
		
	def start_process(self, cmd):
		self.write_log("Starting process cmd: '{}'".format(cmd))
		try:
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return None
		return p
		
########## Time Base ################
	def get_now(self):
		return str(dt.now()).split(".")[0]
	
	def timestamp_to_date(self, stamp):
		if stamp!=None:
			return str(dt.utcfromtimestamp(stamp)).split(".")[0]
		return None
		
########## General Funtions ################
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
			
	def clean_string(self, string):
		try:
			return string.replace("\n","").replace("\r","").strip()
		except Exception as e:
			self.write_error("Error:\n####\n{}\n####\n".format(e))
			return string
	
	def sanitize_string(self, instring):
		words = instring.split()
		mstring = []
		for word in words:
			mword = []
			for char in word:
				if char not in self.PUNCTUATION:
					mword.append(char)
			mstring.append("".join(mword))
		return self.clean_string(" ".join(mstring))
		
