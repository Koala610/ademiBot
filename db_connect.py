import pymysql
import os

from db import *

def _get_parsed_url(url: list) -> dict:
	if type(url) != list:
		return -1
	data = {}
	data['user'] = s[0]
	data['password'] = s[1].split('@')[0]
	data['host'] = s[1].split('@')[1]
	data['port'] = int(s[2].split('/')[0])
	data['database'] = s[2].split('/')[1]
	data['cursorclass'] = pymysql.cursors.DictCursor
	return data


db_link = os.getenv('JAWSDB_URL')

s = db_link.split("mysql://")[1].split(':')
db_settings = _get_parsed_url(s)

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

users_db = User_sqliter(connection)
offers_db = Offers_sqliter(connection)
requests_db = Req_sql(connection)
admins_db = Admin_sqliter(connection)