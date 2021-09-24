import sqlite3

class Admin_sqliter:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def check_if_exists(self, tg_id):
        result = self.cursor.execute(f"SELECT * FROM admins WHERE tg_id = ? ",(tg_id,)).fetchall()
        return bool(len(result))




    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    db = Admin_sqliter('1.db')

if __name__ == '__main__':
    main()