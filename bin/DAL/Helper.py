#!/user/bin/python3


class Helper:
	# Format a postgres result row so that the values can be accessed via column name
	# https://mail.python.org/pipermail/tutor/2010-April/075587.html
	# Utilizes the psycopg2.cursor.description attribute to get the list of column names
	# Example usage: pg_fres(cur.description, cur.fetchone())
	# Returns: A dictionary for one row. Eg {'id': 1, 'name': 'Foo', 'address': 'Bar'}
	@staticmethod
	def pg_col_map(cur_description, results):
		row = {}
		# Loop through the cursor's description of each column name
		for (key, val) in zip((d[0] for d in cur_description), results):
			row[key] = val
		return row
