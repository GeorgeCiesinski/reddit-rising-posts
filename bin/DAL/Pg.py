import psycopg2
import psycopg2.extras
from bin.LIB import LIB

class Pg:
	# connect to postgres
	@staticmethod
	def pg_connect(process_name=None):
		lib = LIB(cfg="config/Pg.cfg", out_log="{}_pg_out.log".format(process_name), err_log="{}_pg_error.log".format(process_name))
		# TODO: Change this to pooling: http://initd.org/psycopg/docs/pool.html

		dbhost = lib.get_config_value("dbhost","23.233.32.54")
		dbport = lib.get_config_value("dbport","5432")
		db_name = lib.get_config_value("dbname","reddit_rising")
		db_username = lib.get_config_value("dbusername","reddit-rising-posts")
		db_password = lib.decode(lib.get_config_value("dbpassword",'czNjYzJWamNtVjByM3Q='))
		connection = psycopg2.connect(
			# host='23.233.33.158',
			host=dbhost,
			port=dbport,
			dbname=db_name,
			user=db_username,
			password=db_password,
			cursor_factory=psycopg2.extras.DictCursor,  # Return dicts instead of tuples
		)

		# Enable autocommit by default.
		# Some thoughts: Both the database design and the Python code is crafted to not require rollbacks.  Whenever
		# 	multiple statements in a transaction is require, they should be occurring within a database function.  This
		# 	also helps to enforce the practice of keeping the number of DB calls to a minimum by placing multiple
		# 	queries only within DB functions.  Any garbage data should be cleaned up by a cleanup function in the DB.
		connection.autocommit = True
		lib.end()
		return connection

