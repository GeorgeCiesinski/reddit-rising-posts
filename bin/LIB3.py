#!/usr/bin/python3.4

#imports 
from datetime import datetime as dt
import sys
import subprocess
import os

#my imports
class MSG:
        #variables
        NAME = None
        MESSAGE = None
        CODE = None
        DATA = None

        def __init__(self, name=None, message=None, code=None, data=None):
                self.NAME = name
                self.MESSAGE = message
                self.CODE = code
                self.DATA = data

        def toString(self):
                if self.DATA is not None:
                        try:
                                data = str(self.DATA)
                        except:
                                data = ""
                return "'%s' | '%s' | '%s' | '%s'" % (self.NAME, self.MESSAGE, self.CODE, self.DATA)

class LIB:
	PUNCTUATION = ['"','\'','*']
	HOME = None
	LOG = None
	CFG = None
	ARGS = None
	MSGLIST = []
	def __init__(self, home, cfgFile=None):
		self.writeLog("Making lib instance: '%s'" % (home))
		self.HOME = home
		self.LOG = "%s/logs" % (self.HOME)
		self.ARGS = sys.argv
		self.writeLog("ARGS: %s" % (self.ARGS))
		if cfgFile == None:
			cfgFile = self.getArgsValue("-cfg","%s/bin/config.cfg" % (self.HOME))
		self.writeLog("Using Config file: '%s'" % (cfgFile))
		if self.readConfig(cfgFile) == MSG.ERROR:
			print("Error reading config file '%s'" % (cfgFile))
			return

############# Config ###########################
	#read the file in config file format, and populate the CFG dictionary
	#input  : config file
	#output : None
	def readConfig(self, cfgFile):
		data = self.readFile(cfgFile)
		if data == MSG.ERROR:
			return MSG.ERROR
		self.CFG = {}
		for line in data:
			line = self.cleanString(line)
			if "#" in line:
				line = line[:line.index("#")]
			if len(line) > 3:
				dic = line.split("=")
				key = self.cleanString(dic[0].lower())
				value = self.cleanString(dic[1])
				
				if value[0] == '"':
					value = self.cleanString(value.replace('"',""))
				elif value[0] == '[':
					mList = value.replace("[","").replace("]","").split(",")
					mList = list(map(self.stanatizeString,mList))
					value = mList
				else:
					try:
						value = int(value)
					except:
						value = self.cleanString(value).lower()

				self.CFG[key] = value
		self.writeLog("CFG: %s" % self.CFG)
	
	#get a config key value, if no key exists, the given default value is returned
	#input  : key, default value
	#output : value
	def getConfigValue(self, key, default):
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
	def getArgs(self):
		return self.ARGS
	
	#get a system key value, if no key exists, the given default value is returned. value is key index + 1
	#input  : None
	#output : list
	def getArgsValue(self, key, default):
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
	def inArgs(self, key):
		args = self.ARGS
		if key in args:
			return True
		return False
		
############# IO #####################################
	#read the given file name, retuns a list of lines 
	#input  : filename
	#output : list
	def readFile(self, fileName):
		data = None
		try:
			inFile = open(fileName, "r+")
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR
		try:
			data = []
			for line in inFile:
				data.append(line)
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR
		return data

	def writeLog(self, string):
		try:
			out = open("%s/output.log" % (self.LOG), 'a+')
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR
		
		msg = "%s ~ %s\n" % (self.getNow(), string)
		
		try:
			out.write(msg)
			con = self.getConfigValue("console", 0) 
			if (con == 1) or (con == 4):
				print(msg)
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR	

		return MSG.NORMAL

	def writeError(self, string):
		try:
			out = open("%s/error.log" % (self.LOG), "a+")
		except:
			return MSG.ERROR
		msg = "%s ~ %s\n" % (self.getNow(), string)
		try:
			out.write(msg)
			con = self.getConfigValue("console", 0) 
			if (con == 2) or (con == 4):
				print(msg)
		except:
			return MSG.ERROR
		return MSG.NORMAL

	def writeFile(self, fileName, string):
		try:
			out = open(fileName, "a+")
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR
		msg = "%s ~ %s\n" % (self.getNow(), string)
		try:
			out.write(msg)
			con = self.getConfigValue("console", 0) 
			if (con == 3) or (con == 4):
				print(msg)
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR
		return MSG.NORMAL

	def pathExists(self, path):
		try:
			value = os.path.exists(path)
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			value = MSG.ERROR
		return value
	
	def makePath(self, path):
		try:
			if not self.pathExists(path):
				os.makedirs(path)
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return MSG.ERROR
		return MSG.NORMAL
	
	def runOScmd(self, cmd):
		self.writeLog("Running cmd: '%s'" % (cmd))
		tOut = self.getConfigValue("cmdtimeout", 60)
		if tout != 0:
			cmd = "timeout %s %s" % (tout,cmd)
		try:
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
			p.wait()
			out, error = p.communicate()
			returnCode = p.poll() 
			self.writeLog("Code:%s\n==OUT==\n%s\n==OUT==\n==ERR==\n%s\n==ERR==" % (returnCode,out,error))
		except Exception as e:
			self.writeLog("Error:\n####\n%s\n####\n" % (e))
			return None
		return [out, error, returnCode]
		
	def startProcess(self, cmd):
		self.writeLog("Starting process cmd: '%s'" % (cmd))
		try:
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
		except Exception as e:
			self.writeLog("Error:\n####\n%s\n####\n" % (e))
			return None
		return p
		
########## Time Base ################
	def getNow(self):
		return str(dt.now()).split(".")[0]
	
	def timestampToDate(self, stamp):
		if stamp!=None:
			return str(dt.utcfromtimestamp(stamp)).split(".")[0]
		return None
		
########## General Funtions ################
	def cleanStringList(self, list):
		try:
			mlist = []
			for m in list:
				if (m != "") or (len(m) >= 1):
					mlist.append(self.cleanString(m))
			return mlist
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return list
			
	def cleanString(self, string):
		try:
			return string.replace("\n","").replace("\r","").strip()
		except Exception as e:
			self.writeError("Error:\n####\n%s\n####\n" % (e))
			return string
	
	def stanatizeString(self, instring):
		words = instring.split()
		mstring = []
		for word in words:
			mword = []
			for char in word:
				if char not in self.PUNCTUATION:
					mword.append(char)
			mstring.append("".join(mword))
		return self.cleanString(" ".join(mstring))
		
