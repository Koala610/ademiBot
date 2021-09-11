import sqlite3

class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def select_all(self):
        result = self.cursor.execute("SELECT * FROM models").fetchall()
        return result


    def user_exists(self, login):
        result = self.cursor.execute(f"SELECT * FROM models WHERE login = ? ",(login,)).fetchall()
        return bool(len(result))

    def update_tg_id(self, tg_id, login):
        result = self.cursor.execute(f"UPDATE models SET tg_id = ? WHERE login = ?",(tg_id, login, ))
        self.commit()


    def password_exists(self, password):
        result = self.cursor.execute(f"SELECT * FROM models WHERE password = ? ",(password,)).fetchall()
        return bool(len(result))


    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    db = SQLighter("1.db")
    print(db.select_all())
    db.update_tg_id(1, "Koala")

if __name__ == '__main__':
    main()
