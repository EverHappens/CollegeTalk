import sqlite3
import threading

class SQLighter:
  
	def __init__(self, database_file):
		self.connection = sqlite3.connect(database_file, check_same_thread = False)
		self.lock = threading.Lock()
		self.cursor = self.connection.cursor()

	def add_user(self, userid, fn, ln, status = 'register'):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO 'userinfo' ('userid', 'fn', 'ln', 'status') VALUES (?, ?, ?, ?)", (userid, fn, ln, status))

	def clear_userlist(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE * FROM col_searchlist WHERE userid = ?; DELETE * FROM col_univlist WHERE userid = ?; DELETE * FROM hsc_searchlist WHERE userid = ?; DELETE * FROM hsc_univlist WHERE userid = ?", (userid, userid, userid, userid))

	def clear_userinfo(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET utc = NULL, about = NULL, status = 'register' WHERE userid = ?", (userid,))

	def check_user(self, userid):
		with self.connection:
			with self.lock:
				result = self.cursor.execute("SELECT * FROM userinfo WHERE userid = ?", (userid,)).fetchall()
				return bool(len(result))

	def get_single_value(self, userid, table_name, column):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT ? FROM ? WHERE userid = ?", (column, tablename, userid,)).fetchall()

	def change_single_value(self, userid, table_name, column, value):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE ? SET ? = ? WHERE userid = ?", (table_name, column, value, userid))

	def change_status(self, userid, status):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET status = ? WHERE userid = ?", (status, userid))

	def get_status(self, userid,):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT status FROM userinfo WHERE userid = ?", (userid,)).fetchall()

	def get_role(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT user_role FROM userinfo WHERE userid = ?", (userid,)).fetchall()

	def change_role(self, userid, user_role):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET user_role = ? WHERE userid = ?", (user_role, userid))

	def add_utc(self, userid, utc):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET utc = ? WHERE userid = ?", (utc, userid))

	def delete_utc(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET utc = NULL WHERE userid = ?", (userid,))

	def add_about(self, userid, about):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET about = ? WHERE userid = ?", (about, userid))

	def del_about(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET about = NULL WHERE userid = ?", (userid,))

	def output_checked_univ(self, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name FROM univlist WHERE univ_name LIKE ?", ('%' + univ_name + '%',)).fetchall()	


	def get_col_univ_for_major(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name FROM col_univlist WHERE userid = ? ORDER BY id DESC LIMIT 1", (userid,)).fetchall()

	def add_col_searchlist(self, userid, messageid, univ_name, major):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO col_searchlist(userid, messageid, univ_name, major) VALUES (?, ?, ?, ?)", (userid, messageid, univ_name, major))

	def get_col_id(self, userid, univ_name, major):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT id FROM col_searchlist WHERE userid = ? AND univ_name = ? AND major = ?",  (userid, univ_name, major, )).fetchall()

	def get_col_messageids(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT messageid FROM col_searchlist WHERE userid = ? AND univ_name LIKE ?", (userid, univ_name,)).fetchall()

	def get_col_last_univ(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name FROM col_univlist WHERE userid = ? ORDER BY id DESC LIMIT 1", (userid,)).fetchall()

	def check_col_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return bool(len(self.cursor.execute("SELECT * FROM col_univlist WHERE userid = ? AND univ_name = ?", (userid, univ_name,)).fetchall()))

	def check_col_major(self, userid, univ_name, major):
		with self.connection:
			with self.lock:
				return bool(len(self.cursor.execute("SELECT * FROM col_searchlist WHERE userid = ? AND univ_name = ? AND major = ?",  (userid, univ_name, major,)).fetchall()))

	def add_col_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO col_univlist(userid, univ_name) VALUES (?, ?)", (userid, univ_name))

	def del_col_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM col_univlist WHERE userid = ? AND univ_name LIKE ?", (userid, '%' + univ_name + '%'))

	def del_col_searchlist(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM col_searchlist WHERE userid = ? AND univ_name = ?", (userid, univ_name))

	def del_col_major_searchlist(self, myid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM col_searchlist WHERE id = ?", (myid,))



	def get_hsc_univ_for_major(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name FROM hsc_univlist WHERE userid = ? ORDER BY id DESC LIMIT 1", (userid,)).fetchall()

	def add_hsc_searchlist(self, userid, messageid, univ_name, major):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO hsc_searchlist(userid, messageid, univ_name, major) VALUES (?, ?, ?, ?)", (userid, messageid, univ_name, major))

	def get_hsc_id(self, userid, univ_name, major):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT id FROM hsc_searchlist WHERE userid = ? AND univ_name = ? AND major = ?",  (userid, univ_name, major, )).fetchall()

	def get_hsc_messageids(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT messageid FROM hsc_searchlist WHERE userid = ? AND univ_name LIKE ?", (userid, univ_name,)).fetchall()

	def get_hsc_last_univ(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name FROM hsc_univlist WHERE userid = ? ORDER BY id DESC LIMIT 1", (userid,)).fetchall()

	def check_hsc_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return bool(len(self.cursor.execute("SELECT * FROM hsc_univlist WHERE userid = ? AND univ_name = ?", (userid, univ_name,)).fetchall()))

	def check_hsc_major(self, userid, univ_name, major):
		with self.connection:
			with self.lock:
				return bool(len(self.cursor.execute("SELECT * FROM hsc_searchlist WHERE userid = ? AND univ_name = ? AND major = ?",  (userid, univ_name, major,)).fetchall()))

	def add_hsc_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO hsc_univlist(userid, univ_name) VALUES (?, ?)", (userid, univ_name))

	def del_hsc_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM hsc_univlist WHERE userid = ? AND univ_name LIKE ?", (userid, '%' + univ_name + '%'))

	def del_hsc_searchlist(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM hsc_searchlist WHERE userid = ? AND univ_name = ?", (userid, univ_name))

	def del_hsc_major_searchlist(self, myid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM hsc_searchlist WHERE id = ?", (myid,))

	def add_hsc_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO hsc_univlist(userid, univ_name) VALUES (?, ?)", (userid, univ_name))

	def del_hsc_univ(self, userid, univ_name):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM hsc_univlist WHERE userid = ? AND univ_name LIKE ?", (userid, '%' + univ_name + '%'))	


	def add_request(self, hsc_userid, col_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO requests(hsc_userid, col_userid) VALUES (?, ?)", (hsc_userid, col_userid))

	def del_request(self, hsc_userid, col_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM requests WHERE hsc_userid = ? AND col_userid = ?", (hsc_userid, col_userid))

	def get_hsc_requests(self, hsc_userid):
		with self.connection:	
			with self.lock:
				return self.cursor.execute("SELECT col_userid FROM requests WHERE hsc_userid = ?", (hsc_userid,)).fetchall()

	def get_col_requests(self, col_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT hsc_userid FROM requests WHERE col_userid = ?", (col_userid,)).fetchall()

	def add_comrade(self, hsc_userid, col_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("INSERT INTO comrade(hsc_userid, col_userid) VALUES (?, ?)", (hsc_userid, col_userid))

	def del_comrade(self, hsc_userid, col_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("DELETE FROM comrade WHERE hsc_userid = ? and col_userid = ?", (hsc_userid, col_userid))

	def get_hsc_comrade(self, hsc_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT col_userid FROM comrade WHERE hsc_userid = ?", (hsc_userid,)).fetchall()

	def get_col_comrade(self, col_userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT hsc_userid FROM comrade WHERE col_userid = ?", (col_userid,)).fetchall()

	def change_role(self, userid, user_role):
		with self.connection:
			with self.lock:
				return self.cursor.execute("UPDATE userinfo SET user_role = ? WHERE userid = ?", (user_role, userid))
		
# VITIN BRED		
	def get_std (self, userid) :
		with self.connection:
			with self.lock:
				pairs = self.cursor.execute("SELECT univ_name, major FROM hsc_searchlist WHERE userid = ?", (userid,)).fetchall()
				out = []
				for pair in pairs:
					results = self.cursor.execute("SELECT userinfo.userid, userinfo.fn, userinfo.ln, userinfo.about, col_searchlist.univ_name as univ, col_searchlist.major as major FROM userinfo INNER JOIN col_searchlist ON col_searchlist.userid = userinfo.userid WHERE univ LIKE ? AND major LIKE ?", (pair[0], pair[1])).fetchall()
					if results:
						for result in results:
							out.append(result)
				return out

	def get_test(self, userid):
		with self.connection:
			with self.lock:
				hsc_searchlist = self.cursor.execute("SELECT univ_name, major FROM hsc_searchlist WHERE userid = ?", (userid,)).fetchall()
				print(hsc_searchlist)
				out = set()
				for pair in hsc_searchlist:
					print(pair)
					results = self.cursor.execute("SELECT userid FROM col_searchlist WHERE univ_name = ? AND major LIKE ?", (pair[0], pair[1])).fetchall()
					if results:
						for result in results:
							out.add(result)
				return out

	def get_userinfo(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT fn, ln, about FROM userinfo WHERE userid = ?", (userid,)).fetchall()

	def get_col_acad(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name, major FROM col_searchlist WHERE userid = ?", (userid,)).fetchall()

	def get_hsc_acad(self, userid):
		with self.connection:
			with self.lock:
				return self.cursor.execute("SELECT univ_name, major FROM hsc_searchlist WHERE userid = ?", (userid,)).fetchall()