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

    def get_optional_info(self, tg_id):
        return self.get_info(tg_id)[9:]

    def check_if_new(self, tg_id):
        result = self.cursor.execute(f"SELECT is_new FROM models WHERE tg_id = ?",(tg_id, )).fetchall()
        return result[0][0]

    def make_old(self, tg_id):
        result = self.cursor.execute(f"UPDATE models SET is_new = 0 WHERE tg_id = ?",(tg_id, ))
        self.commit()

    def update_name(self, tg_id, name):
        result = self.cursor.execute(f"UPDATE models SET name = ? WHERE tg_id = ?",(name, tg_id, ))
        self.commit()

    def update_surname(self, tg_id, surname):
        result = self.cursor.execute(f"UPDATE models SET surname = ? WHERE tg_id = ?",(surname, tg_id, ))
        self.commit()

    def update_date(self, tg_id, date):
        result = self.cursor.execute(f"UPDATE models SET birth_date = ? WHERE tg_id = ?",(date, tg_id, ))
        self.commit()

    def update_gender(self, tg_id, gender):
        result = self.cursor.execute(f"UPDATE models SET isMale = ? WHERE tg_id = ?",(gender, tg_id, ))
        self.commit()


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
        except IndexError:
            return "tg_id doesn't exist"

        offers_len = len(offers_list)-1
        offers_list = offers_list[:offers_len]
        return offers_list

    def replace_offers(self, tg_id, offers):
        result = self.cursor.execute(f"UPDATE models SET offers_taken = ? WHERE tg_id = ?",(offers, tg_id, ))
        self.commit()


    def del_user_offer(self, tg_id, offer_id):
        offers = self.get_offers_taken(tg_id)
        res_offers = [offer for offer in offers if int(offer) != int(offer_id)]
        res_offers = ','.join(res_offers)+ ","
        self.replace_offers(tg_id, res_offers)




    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    db = SQLighter("1.db")
    print(db.user_exists('Koala610'))

if __name__ == '__main__':
    main()
