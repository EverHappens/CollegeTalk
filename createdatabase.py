import sqlite3

def create_connection(fb_file):
	conn = None
	try:
		conn = sqlite3.connect(fb_file)
		print(sqlite3.version)
	except sqlite3.Error as e:
		print(e)

	return conn

def create_table(conn, sql_create):
	try:
		c = conn.cursor()
		c.execute(sql_create)
	except sqlite3.Error as e:
		print(e)

def testonething(conn, sql_create):
	try:
		c = conn.cursor()
		c.execute(sql_create)
	except sqlite3.Error as e:
		print(e)

if __name__ == '__main__':
	
	connection = sqlite3.connect('sql.db', check_same_thread = False)
	cursor = connection.cursor()
	result = cursor.execute("SELECT testhour FROM testla WHERE idd = 321321").fetchall()
	print(result)
	for number in result:
		if 1 in number:
			print("success")
		print(number)
	print(result[1]+result[2])

