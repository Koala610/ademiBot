import os
import pymysql

API_TOKEN = os.getenv('API_TOKEN')
db_link = os.getenv('JAWSDB_URL')


s = db_link.split("mysql://")[1].split(':')
db_settings = {}

db_settings['user'] = s[0]
db_settings['password'] = s[1].split('@')[0]
db_settings['host'] = s[1].split('@')[1]
db_settings['port'] = int(s[2].split('/')[0])
db_settings['database'] = s[2].split('/')[1]
db_settings['cursorclass'] = pymysql.cursors.DictCursor

try:
    connection = pymysql.connect(
		host = db_settings['host'],
		port = db_settings['port'],
		user = db_settings['user'],
		password = db_settings['password'],
		database = db_settings['database'],
		cursorclass = db_settings['cursorclass'],
        )

except Exception as ex:
	print(ex)

