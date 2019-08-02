# !/usr/bin/python3.4

# imports
from datetime import datetime as DT
from datetime import timedelta as TD
import time
import sys
import subprocess
import os
import inspect
import multiprocessing as MP
import base64
import re

#file object, stores information about a given file... no need to import this.
class file:
    #set the file properties
    def __init__(self,name=None, permissions=None, size=None, modified_time=None, path=None):
        self.name = name
        self.permissions = permissions
        self.size = size
        self.modified_time = modified_time
        self.path = path

    # Determin if this file is a directory
    # input: None
    # Ouput: Boolean
    def is_directory(self):
        if self.permissions is not None:
            parts = self.permissions
            #print(parts)
            if parts[0] == 'd':
                return True
        return False

class LIB:
    PUNCTUATION = ['"', '\'', '*']
    HOME = None
    LOG = None
    CFG = None
    ARGS = None
    MSGLIST = []
    PROCESSLIST = []
    OS = None

    def __init__(self, home=None, cfg=None):
        #find out home if none is given. lib location is used.
        self.PROCESSLIST = []
        if home is None:
            home = os.getcwd()
            parts = home.split("/")
            if parts[len(parts) - 1] == "bin":
                home = "/".join(parts[:len(parts) - 1])

        self.HOME = home
        # check and/or create the project structure
        if not self.path_exists(self.HOME):
            if not self.make_path(self.HOME):
                return

        #set the logs directory
        self.LOG = "{}/logs".format(self.HOME)
        self.write_log("Making lib instance: '{}'".format(home))
        if not self.path_exists(self.LOG):
            self.write_log("Creating path: '{}'".format(self.LOG))
            if not self.make_path(self.LOG):
                string = "Unable to create path '{}'".format(self.LOG)
                self.write_log(string)
                self.write_error(string)

        #get and store the sys arguments
        self.ARGS = sys.argv
        self.write_log("ARGS: {}".format(self.ARGS))

        #load the config file
        if cfg is None:
            cfg = self.get_args_value("-cfg", "{}/config/config.cfg".format(self.HOME))
        if self.read_config(cfg) == -1:
            self.CFG = {}
            self.write_log("No such cfg file, no configs being used")
        else:
            self.write_log("Using Config file: '{}'".format(cfg))

        #set the current running OS
        self.OS = self.clean_string(str(sys.platform).lower())
        self.write_log("Using OS: {}".format(self.OS))

        # Start the config file reload thread
        confi_reloader = MP.Process(name = "Config_Reloader", target=self.reload_config, args=(cfg,))
        confi_reloader.start()
        self.PROCESSLIST.append(confi_reloader)


    """
    CONFIG
    """

    # Read the file in config file format, and populate the CFG dictionary
    # Input  : config file
    # Output : None
    def read_config(self, cfgFile):
        data = self.read_file(cfgFile)
        if (data == -1) or (data is None):
            return None
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
                    value = self.clean_string(value.replace('"', ""))
                elif value[0] == '[':
                    mList = value.replace("[", "").replace("]", "").split(",")
                    mList = list(map(self.sanitize_string, mList))
                    value = mList
                else:
                    try:
                        value = int(value)
                    except:
                        value = self.clean_string(value).lower()

                self.CFG[key] = value
        self.write_log("CFG: '{}'".format(self.CFG))

    # Get a config key value, if no key exists, the given default value is returned
    # Input  : key, default value
    # Output : value
    def get_config_value(self, key, default=None):
        try:
            data = self.CFG[key.lower()]
        except:
            data = default
        return data

    # Reload the given lib with the given config file
    # input: String config file
    # output: None
    def reload_config(self, config_file):
        if self.get_config_value("ConfigReloadInterval", 60) == 0:
            return None
        self.write_log("Starting config reload process")
        while True:
            if os.getppid() == 1:
                return None
            self.write_log("Reloading confing '{}'".format(config_file))
            self.read_config(config_file)
            self.write_log("Reloading done")
            self.sleep(self.get_config_value("ConfigReloadInterval", 60))

    # Destroy this lib instance... it will become unusable if this is called
    # Input: None
    # Output: None
    def end(self):
        self.write_log("Terminating LIB instance")
        for process in self.PROCESSLIST:
                if process.is_alive():
                        self.write_log("Stopping process: {}".format(process.name))
                        process.terminate()
        del self

    # Get the name of the parent script that called lib
    # Input: None
    # Output: String
    def get_script(self):
        # Index definition for stack object
        FILENAME_INDEX = 1
        FUNCTIONAME_INDEX = 3

        # Get python stack
        try:
            stack = inspect.stack()
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None

        # Remove all python imports. (this in theory will only show usr writen scripts)
        m_stack = []
        for entry in stack:
            try:
                if ("python" not in entry[FILENAME_INDEX]) and ("__" not in entry[FUNCTIONAME_INDEX]):
                    m_stack.append(entry)
            except Exception as e:
                self.write_error("Error:\n####\n{}\n####\n".format(e))
                return None

        # reverse the stack (starting of the script is at the bottom, must bring it top)
        m_stack.reverse()
        try:
            for entry in m_stack:
                name = entry[FILENAME_INDEX]
                function = entry[FUNCTIONAME_INDEX]
                idx = m_stack.index(entry)
                # if this is the last entry in the last return script and function name
                if idx is len(m_stack) - 1:
                    if self.HOME in name:
                        name = name.split("/")[-1]
                    return "{}/{}".format(name, function)
                # get the next entry
                next_entry = m_stack[idx + 1]
                # if this is the first entry, and the next entry does not have the same name return script (this is pobably the main script)
                if (idx == 0) and (next_entry[FILENAME_INDEX] is not name):
                    if self.HOME in name:
                        name = name.split("/")[-1]
                    return "{}".format(name)
                # if the next entry is not the same return script and function name
                if (next_entry[FILENAME_INDEX] is not name):
                    if self.HOME in name:
                        name = name.split("/")[-1]
                    return "{}/{}".format(name, function)
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None

    """
    SYSTEM ARGUMENTS
    """

    # Get the system argumnets
    # Input  : None
    # Output : list
    def get_args(self):
        return self.ARGS

    # Get a system key value, if no key exists, the given default value is returned. value is key index + 1
    # Input  : None
    # Output : list
    def get_args_value(self, key, default=None):
        args = self.ARGS
        try:
            idx = args.index(key)
            value = args[idx + 1]
        except Exception as e:
            value = default
        return value

    # Ket in system arguments
    # Input  : key
    # Output : boolean
    def in_args(self, key):
        args = self.ARGS
        if key in args:
            return True
        return False

    """
    IO
    """

    # Read string from user
    # Input: String message
    # Output: String user_input
    def read_string(self,message = "Enter a string: "):
        try:
            input_string = input(message)
            self.write_log("{} {}".format(message, input_string))
            return input_string
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None

    # Read int from user
    # Input: String message
    # Output: int user_input
    def read_int(self, message="Enter an integer: "):
        try:
            value = self.read_string(message)
            self.write_log("{} {}".format(message,value))
            if value is -1:
                raise
            intput_int = int(value)
            return intput_int
        except Exception as e:
            self.write_log("Invalid int")
            return None

    # Read int from user
    # Input: String message
    # Output: String user_input
    def read_char(self, message="Enter a character: "):
        try:
            input_string = self.read_string(message)
            self.write_log("{} {}".format(message, input_string))
            if len(input_string) != 1:
                raise
            return input_string
        except Exception as e:
            self.write_log("Invalid char")
            return None

    # Read the given file name, retuns a list of lines
    # Input  : filename
    # Output : list
    def read_file(self, fileName):
        try:
            inFile = open(fileName, "r+")
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        try:
            data = []
            for line in inFile:
                data.append(line)
            return data
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None

    # Write out put to the log file
    # Input  : string
    # Output : None
    def write_log(self, string, mode="a+"):
        try:
            out = open("{}/output.log".format(self.LOG), mode)
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        msg = "{} ~ {} ~ {}\n".format(self.get_now(), self.get_script(), string)
        try:
            con = self.get_config_value("console", 0)
            if (con == 1) or (con == 4):
                print(msg)
            out.write(msg)
            out.close()
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None

        return 0

    # Write out put to the error file
    # Input  : string
    # Output : None
    def write_error(self, string, mode="a+"):
        try:
            out = open("{}/error.log".format(self.LOG), mode)
        except:
            return None
        msg = "{} ~ {} ~ {}\n".format(self.get_now(), self.get_script(), string)
        try:
            con = self.get_config_value("console", 0)
            if (con == 2) or (con == 4):
                print(msg)
            out.write(msg)
            out.close()
        except:
            return None
        return 0

    # Write output to a specified file
    # Input: filename, string
    # Output: None
    def write_file(self, fileName, string, mode="a+"):
        try:
            out = open(fileName, mode)
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        msg = "{} ~ {}\n".format(self.get_now(), string)
        try:
            out.write(msg)
            con = self.get_config_value("console", 0)
            if (con == 3) or (con == 4):
                print(msg)
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        return 0

    # List directory content
    # Input: String path
    # Ouput: List of dict of files
    def directory_listing(self, directory=None, recursive=None):
        if self.OS != "linux":
            self.write_log("directory_listing is only linux compatible")
            return None
        files = []
        if not self.path_exists(directory):
            self.write_log("No such path {}".format(directory))
            return None
        data, error, code = self.run_os_cmd("ls -lh {}".format(directory))
        if code !=0 :
            self.write_log("Error getting directory listing {}".format(error))
            return None
        data = data.decode(self.get_config_value("CharEncoding", "utf-8"))
        lines = data.split("\n")
        for line in lines:
            line=self.clean_string(line)
            line_parts = line.split(" ")
            if len(line_parts) >=8:
                mfile = file()
                mfile.name = line_parts[8:]
                mfile.permissions = line_parts[0]
                mfile.size = line_parts[4]
                mfile.modified_time = line_parts[5:7]
                files.append(mfile)
        return files


    # Check if the given path already exists
    # Input: absolute path TODO: Make relative safe
    # Output: boolean
    def path_exists(self, path):
        self.write_log("Check path: {}".format(path))
        try:
            value = os.path.exists(path)
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            value = False
        self.write_log("Result: {}".format(value))
        return value

    # Create the given path. This is a recursive operation.
    # Input: absolute path TODO: Make relative safe
    # Output: boolean
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

    # Run the given os command
    # Input: string (system command)
    # Output: [command.output, command.error, command.returncode]
    def run_os_cmd(self, cmd):
        tout = self.get_config_value("cmdtimeout", 60)
        if tout != 0:
            cmd = "timeout {} {}".format(tout, cmd)
        self.write_log("Running cmd: '{}'".format(cmd))
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            p.wait()
            out, error = p.communicate()
            returnCode = p.poll()
            self.write_log("Code:{}\n==OUT==\n{}\n==OUT==\n==ERR==\n{}\n==ERR==".format(returnCode, out, error))
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        return [out, error, returnCode]

    # Start the given os command as it's on process
    # Input: string (system command)
    # Output: subprocess.Popen obejct
    def start_process(self, cmd):
        self.write_log("Starting process cmd: '{}'".format(cmd))
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        return p

    """
    TIME BASE
    """

    # Get the time now
    # Input: None
    # Output: string
    def get_now(self):
        return str(DT.now()).split(".")[0]

    # Convert time stamp to human readable date
    # Input: string (timestamp)
    # Output: string (human readable format)
    def timestamp_to_date(self, stamp):
        if stamp is not None:
            return str(DT.utcfromtimestamp(stamp)).split(".")[0]
        return None

    # Sleep for a given duration
    # Input: int (duration)
    # Output: none
    def sleep(self, duration):
        self.write_log("Sleeping for {}".format(duration))
        try:
            time.sleep(duration)
        except Exception as e:
            string = "Sleep error: '{}'".format(e)
            self.write_log("Sleep error")
            self.write_error(string)
        return

    # Delta time +/-
    # Input: Integer delta, String measure
    def time_delta(self, delta=None, measure=None):
        if (delta is None) or (measure is None):
            self.write_error("Invalid delta or measure")
            return None
        MEASURE = ['days','weeks','hours','minutes','seconds']
        if measure not in MEASURE:
            self.write_error("Invalid measure {}".format(measure))
            self.write_error("OPTIONS: {}".format(MEASURE))
            return None
        if type(delta) is not int:
            self.write_error("Delta must be an integer")
            return None
        self.write_log("Time delta {} {}".format(delta, measure))
        now = DT.now()
        future = False
        if delta >0:
            future = True
        delta = abs(delta)
        measure = measure.lower()
        return_value = None
        if future:
                if measure == "seconds":
                    return_value = str(now + TD(seconds=delta)).split(".")[0]
                if measure == "minutes":
                    return_value = str(now + TD(minutes=delta)).split(".")[0]
                if measure == "hours":
                    return_value = str(now + TD(hours=delta)).split(".")[0]
                if measure == "days":
                    return_value = str(now + TD(days=delta)).split(".")[0]
                if measure == "weeks":
                    return_value = str(now + TD(weeks=delta)).split(".")[0]
        if not future:
                if measure == "seconds":
                    return_value = str(now - TD(seconds=delta)).split(".")[0]
                if measure == "minutes":
                    return_value = str(now - TD(minutes=delta)).split(".")[0]
                if measure == "hours":
                    return_value = str(now - TD(hours=delta)).split(".")[0]
                if measure == "days":
                    return_value = str(now - TD(days=delta)).split(".")[0]
                if measure == "weeks":
                    return_value = str(now - TD(weeks=delta)).split(".")[0]
        return return_value
    """
    GENERAL FUNCTIONS
    """

    # Clean the given list of strings. Errors result in the same list being returned
    # Input: list (of strings)
    # Output: list (of string)
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

    # Clean the given string. Remove newline characters, and strip whitespaces. Errors result in the same string being returned
    # Input: string
    # Output: string
    def clean_string(self, string):
        try:
            mstring = string.replace("\n", "").replace("\r", "").strip()
            mstring = re.sub('\s+', ' ', mstring).strip()
            return mstring
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return string

    # Sanitize string, remove all punctuations (defined at the top), newlines, and whitespaces
    # Input: string
    # Output: string
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

    # Encode a given value using base64. A key can be given to further secure the encoding
    #  NOTE: THIS IS NOT SECURE ENCRIPTION... BUT ALTEAST ITS NOT PLAIN TEXT
    # Input: String value, String key
    # Output: String encoded_value
    def encode(self, value = None, key="secret"):
        self.write_log("Encoding: {}".format(value))
        encoded_value = None
        if value is None:
                return encoded_value
        try:
            encoded_key = base64.b64encode(key.encode(self.get_config_value('CharEncoding','utf-8'))).decode(self.get_config_value('CharEncoding','utf-8'))
            value_lenght = len(value)
            m_value = "{}{}{}".format(value[:int(value_lenght/2)],encoded_key,value[int(value_lenght/2):])
            encoded_value = base64.b64encode(m_value.encode(self.get_config_value('CharEncoding', 'utf-8'))).decode(self.get_config_value('CharEncoding', 'utf-8'))
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        return encoded_value

    # Decode a given value using base64. A key has to be given if it was encoded using one
    #  NOTE: THIS IS NOT SECURE ENCRIPTION... BUT ALTEAST ITS NOT PLAIN TEXT
    # Input: String value, String key
    # Output: String decoded_value
    def decode(self, value = None, key="secret"):
        self.write_log("Decoding: {}".format(value))
        m_value = None
        if value is None:
            return m_value
        try:
            encoded_key = base64.b64encode(key.encode(self.get_config_value('CharEncoding', 'utf-8'))).decode(self.get_config_value('CharEncoding', 'utf-8'))
            decoded_value = base64.b64decode(value.encode(self.get_config_value('CharEncoding', 'utf-8'))).decode(self.get_config_value('CharEncoding', 'utf-8'))
            m_value = decoded_value.replace(encoded_key,"")
        except Exception as e:
            self.write_error("Error:\n####\n{}\n####\n".format(e))
            return None
        return m_value
