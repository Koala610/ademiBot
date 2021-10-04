class Sqliter:
	def __init__(self, connection):
	    self.connection = connection
	    self.cursor = self.connection.cursor()


	def check_connection(f):
	    def wrapper(*args):
	        args[0].connection.ping(reconnect = True)
	        return f(*args)
	    return wrapper



	@check_connection
	def commit(self):
		self.connection.commit()


	def close(self):
		self.connection.close()