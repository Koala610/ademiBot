import sqlite3

class SQLighter:
    def __init__(self,database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()


    def user_exists(self,login):
        result = self.cursor.execute(f"SELECT * FROM models WHERE login = ? ",(login,)).fetchall()
        return bool(len(result))


    def password_exists(self,password):
        result = self.cursor.execute(f"SELECT * FROM models WHERE password = ? ",(password,)).fetchall()
        return bool(len(result))


    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    pass

if __name__ == '__main__':
    main()
