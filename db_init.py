import settings

from db.requests_sqliter import Request_sqliter as Req_sql
from db.sqliter import SQLighter
from db.offers_model import Offers_model
from db.admins_sqliter import Admin_sqliter



users_db = SQLighter(settings.db_path)
offers_db = Offers_model(settings.db_path)
requests_db = Req_sql(settings.db_path)
admins_db = Admin_sqliter(settings.db_path)