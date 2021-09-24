import sqlite3

class Offers_model:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def get_offers(self, category):
        result = self.cursor.execute(f"SELECT offers.id, b.name, offers.start_date, offers.finish_date  FROM offers INNER JOIN businesses b on offers.bus_id = b.id WHERE offers.category = ?",(category,)).fetchall()
        return result

    def check_views_limit(self, id):
        views = self.cursor.execute(f"SELECT views_count FROM offers WHERE id = ?",(id, )).fetchall()
        views_limit = self.cursor.execute(f"SELECT views_limit FROM offers WHERE id = ?",(id, )).fetchall()
        return views[0][0] < views_limit[0][0]

    def get_business_name(self, id):
        result = self.cursor.execute(f"SELECT name FROM businesses WHERE id = ? ",(id,)).fetchall()
        try:
            return result[0][0]
        except IndexError:
            return result

    def get_business_id(self, id):
        result = self.cursor.execute(f"SELECT bus_id FROM offers WHERE id = ?",(id, )).fetchall()
        try:
            return result[0][0]
        except IndexError:
            return result


    def increment_views(self, id):
        result = self.cursor.execute(f"UPDATE offers SET views_count = views_count + 1 WHERE id = ?",(id, )).fetchall()
        self.commit()


    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()


def main():
    db = Offers_model('1.db')
    print(db.get_offers(1000))

if __name__ == '__main__':
    main()