import settings

from db.db_requests_requests import Request_sqliter as Req_sql
from db.db_users_requests import SQLighter
from db.db_offer_requests import Offers_model
from db.db_admin_request import Admin_sqliter



users_db = SQLighter(settings.connection)
offers_db = Offers_model(settings.connection)
requests_db = Req_sql(settings.connection)
admins_db = Admin_sqliter(settings.connection)