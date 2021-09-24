import sqlite3

class Request_sqliter:
	def __init__(self, database_file):
		self.connection = sqlite3.connect(database_file)
		self.cursor = self.connection.cursor()

	def add_request(self, tg_id, login, offer_id, story_link, file_id):
		result = self.cursor.execute(f"INSERT INTO requests (tg_id, login, offer_id, story_link, photo_check_id) VALUES(?, ?, ?, ?, ?)",(tg_id, login, offer_id, story_link, file_id))
		self.commit()

	def get_all_requests(self):
		result = self.cursor.execute("SELECT * FROM requests").fetchall()
		return result

	def get_users_requests_by_status(self, id, status):
		result = self.cursor.execute(f"SELECT * FROM requests WHERE status = ? AND tg_id = ?",(status ,id,)).fetchall()
		return result




	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()


def main():
	db = Request_sqliter('1.db')
	#print(len(db.get_users_requests_by_status(335271283, -1)))

if __name__ == '__main__':
	main()