import sqlite3

class Offers_model:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def get_offers(self, category):
        result = self.cursor.execute("SELECT offers.id, b.name, offers.start_date, offers.finish_date  FROM offers INNER JOIN businesses b on offers.bus_id = b.id").fetchall()
        return result


    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    pass

if __name__ == '__main__':
    main()