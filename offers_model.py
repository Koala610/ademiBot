import sqlite3

class Offers_model:
    def __init__(self,database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()


    def get_offers(self, category):
        result = self.cursor.execute(f"SELECT * FROM offers WHERE category = ?",(category,)).fetchall()
        return result


    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    pass

if __name__ == '__main__':
    main()