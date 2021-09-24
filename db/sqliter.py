import sqlite3

class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def select_all(self):
        result = self.cursor.execute("SELECT * FROM models").fetchall()
        return result


    def tg_id_exists(self, tg_id):
        result = self.cursor.execute(f"SELECT * FROM models WHERE tg_id = ? ",(tg_id,)).fetchall()
        return bool(len(result))

    def user_exists(self, login):
        result = self.cursor.execute(f"SELECT * FROM models WHERE login = ? ",(login,)).fetchall()
        return bool(len(result))

    def update_tg_id(self, tg_id, login):
        result = self.cursor.execute(f"UPDATE models SET tg_id = ? WHERE login = ?",(tg_id, login, ))
        self.commit()

    def get_login(self, tg_id):
        result = self.cursor.execute(f"SELECT login FROM models WHERE tg_id = ? ",(tg_id,)).fetchall()
        try:
            return result[0][0]
        except IndexError:
            return result

    def get_info(self, tg_id):
        result = self.cursor.execute(f"SELECT * FROM models WHERE tg_id = ?",(tg_id, )).fetchall()
        return result[0]

    def check_if_logged(self, tg_id):
        result = self.cursor.execute(f"SELECT is_logged FROM models WHERE tg_id = ?",(tg_id, )).fetchall()
        return result[0][0]




    def password_exists(self, login, password):
        result = self.cursor.execute(f"SELECT * FROM models WHERE password = ? AND login = ? ",(password, login)).fetchall()
        return bool(len(result))

    def add_offer(self, id, tg_id):
        offers_taken_dict = self.cursor.execute(f"SELECT offers_taken FROM models WHERE tg_id = ? ",(tg_id,)).fetchall()
        offers_taken = ""
        for offer in offers_taken_dict[0]:
            offers_taken += str(offer)
        offers_taken = offers_taken.replace("None", "")
        offers_taken += str(id) + ","
        result = self.cursor.execute(f"UPDATE models SET offers_taken = ? WHERE tg_id = ?",(offers_taken, str(tg_id), ))
        self.commit()

    def get_offers_taken(self, tg_id):
        offers_taken_dict = self.cursor.execute(f"SELECT offers_taken FROM models WHERE tg_id = ? ",(tg_id,)).fetchall()
        try:
            offers_list = offers_taken_dict[0][0].split(',')
        except AttributeError:
            offers_list = []

        offers_len = len(offers_list)-1
        offers_list = offers_list[:offers_len]
        return offers_list




    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    db = SQLighter("1.db")
    print(db.password_exists("Koala610", 123456))

if __name__ == '__main__':
    main()
