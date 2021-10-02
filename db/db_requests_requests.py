#from db_settings import *
class Request_sqliter:
	def __init__(self, connection):
		self.connection = connection
		self.cursor = self.connection.cursor()

	def add_request(self, tg_id, login, offer_id, story_link, file_id, trans_photo_id):
		self.cursor.execute(f"INSERT INTO requests (tg_id, login, offer_id, story_link, photo_check_id, trans_photo_id) VALUES({tg_id}, '{login}', {offer_id}, '{story_link}', '{file_id}', '{trans_photo_id}')")
		self.commit()

	def get_all_requests(self):
		self.cursor.execute("SELECT * FROM requests")
		result = [list(row.values()) for row in self.cursor.fetchall()]

		return result

	def get_users_requests_by_status(self, id, status):
		self.cursor.execute(f"SELECT * FROM requests WHERE status = {status} AND tg_id = {id}")
		try:
			result = list(self.cursor.fetchall()[0].values())
		except:
			result = []
		return result

	def get_request_tg_id(self, id):
		self.cursor.execute(f"SELECT tg_id FROM requests WHERE id = {id}")
		result = self.cursor.fetchall()
		try:
			return result[0]['tg_id']
		except IndexError:
			return -1

	def get_request_status(self, id):
		self.cursor.execute(f"SELECT status FROM requests WHERE id = {id}")
		result = self.cursor.fetchall()
		try:
			return result[0]['status']
		except IndexError:
			return -1


	def get_photos_by_id(self, id):
		self.cursor.execute(f"SELECT photo_check_id, trans_photo_id FROM requests WHERE id = {id}")
		result = self.cursor.fetchall()
		try:
			return list(result[0].values())
		except IndexError:
			return -1

	def change_status(self, id, status):
		self.cursor.execute(f"UPDATE requests SET status = {status} WHERE id = {id}")
		self.commit()




	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()


def main():
	pass

if __name__ == '__main__':
	main()