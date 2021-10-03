#from db_settings import *
import datetime

class SQLighter:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def check_connection(f):
        def wrapper(*args):
            args[0].connection.ping(reconnect = True)
            return f(*args)
        return wrapper



    @check_connection
    def select_all(self):
        self.cursor.execute("SELECT * FROM models")
        result = [list(row.values()) for row in self.cursor.fetchall()]
        return result

    @check_connection
    def tg_id_exists(self, tg_id):
        self.cursor.execute(f"SELECT * FROM models WHERE tg_id = {tg_id}")
        result = self.cursor.fetchall()
        return bool(len(result))


    @check_connection
    def user_exists(self, login):
        self.cursor.execute(f"SELECT * FROM models WHERE login = '{login}'")
        result = self.cursor.fetchall()
        return bool(len(result))


    @check_connection
    def update_tg_id(self, tg_id, login):
        self.cursor.execute(f"UPDATE models SET tg_id = {tg_id} WHERE login = '{login}'")
        self.commit()



    @check_connection
    def get_login(self, tg_id):
        self.cursor.execute(f"SELECT login FROM models WHERE tg_id = {tg_id}")
        result = self.cursor.fetchall()
        try:
            return result[0]['login']
        except IndexError:
            return []


    @check_connection
    def get_users_ids(self):
        self.cursor.execute("SELECT tg_id FROM models")
        result = self.cursor.fetchall()
        result = [tg_id['tg_id'] for tg_id in result if tg_id['tg_id'] != '']

        return result


    @check_connection
    def get_info(self, tg_id):
        self.cursor.execute(f"SELECT * FROM models WHERE tg_id = {tg_id}")
        result = self.cursor.fetchall()
        try:
            return list(result[0].values())
        except IndexError:
            return []


    @check_connection
    def get_optional_info(self, tg_id):
        return self.get_info(tg_id)[9:]


    @check_connection
    def check_if_new(self, tg_id):
        self.cursor.execute(f"SELECT is_new FROM models WHERE tg_id = {tg_id}")
        result = self.cursor.fetchall()
        try:
            return result[0]['is_new']
        except IndexError:
            return -1


    @check_connection
    def make_old(self, tg_id):
        self.cursor.execute(f"UPDATE models SET is_new = 0 WHERE tg_id = {tg_id}")
        self.commit()


    @check_connection
    def update_name(self, tg_id, name):
        self.cursor.execute(f"UPDATE models SET name = '{name}' WHERE tg_id = {tg_id}")
        self.commit()


    @check_connection
    def update_surname(self, tg_id, surname):
        self.cursor.execute(f"UPDATE models SET surname = {surname} WHERE tg_id = {tg_id}")
        self.commit()


    @check_connection
    def update_date(self, tg_id, date):
        self.cursor.execute(f"UPDATE models SET birth_date = '{date}' WHERE tg_id = {tg_id}")
        self.commit()


    @check_connection
    def update_gender(self, tg_id, gender):
        result = self.cursor.execute(f"UPDATE models SET isMale = {gender} WHERE tg_id = {tg_id}")
        self.commit()



    @check_connection
    def password_exists(self, login, password):
        self.cursor.execute(f"SELECT * FROM models WHERE password = '{password}' AND login = '{login}'")
        result = self.cursor.fetchall()
        return bool(len(result))


    @check_connection
    def add_offer(self, id, tg_id):
        offers_list = self.get_offers_taken(tg_id)
        try:
            offers_list[0] = "" if offers_list[0] == ',' else offers_list[0]
        except:
            pass
        offers_taken = ','.join(offers_list)+',' if len(offers_list) != 0 else ""
        offers_taken = offers_taken.replace("None", "")
        offers_taken += str(id) + ","
        self.replace_offers(tg_id, offers_taken)


    @check_connection
    def get_offers_taken(self, tg_id):
        self.cursor.execute(f"SELECT offers_taken FROM models WHERE tg_id = {tg_id}")
        offers_taken = self.cursor.fetchall()
        try:
            offers_list = offers_taken[0]['offers_taken'].split(',')
        except AttributeError:
            offers_list = []
        except IndexError:
            return "tg_id doesn't exist"

        offers_list = [l for l in offers_list if l != '']
        if len(offers_list) == 1 and offers_list[0] == '':
            return []
        return offers_list


    @check_connection
    def replace_offers(self, tg_id, offers):
        self.cursor.execute(f"UPDATE models SET offers_taken = '{offers}' WHERE tg_id = {tg_id}")
        self.commit()

    @check_connection
    def del_user_offer(self, tg_id, offer_id):
        offers = self.get_offers_taken(tg_id)
        res_offers = [offer for offer in offers if int(offer) != int(offer_id)]
        res_offers = ','.join(res_offers)+ "," if len(res_offers) > 0 else ""
        self.replace_offers(tg_id, res_offers)



    @check_connection
    def commit(self):
        self.connection.commit()



def main():
    pass

if __name__ == '__main__':
    main()