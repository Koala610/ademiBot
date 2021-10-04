from .sqliter import Sqliter

class Offers_sqliter(Sqliter):
    def __init__(self, connection):
        super().__init__(connection)

    @Sqliter.check_connection
    def get_offers(self, category):
        self.cursor.execute(f"SELECT offers.id, b.name, offers.start_date, offers.finish_date  FROM offers INNER JOIN businesses b on offers.bus_id = b.id WHERE offers.category = {category}")
        result = [list(row.values()) for row in self.cursor.fetchall()]
        return result
    @Sqliter.check_connection
    def get_info(self, id):
        self.cursor.execute(f"SELECT * FROM offers WHERE id = {id} ")
        result = self.cursor.fetchall()[0]
        return result

    @Sqliter.check_connection
    def get_all_ids(self):
        self.cursor.execute("SELECT id FROM offers")
        ids = self.cursor.fetchall()
        result = [id['id'] for id in ids]
        return result

    @Sqliter.check_connection
    def check_views_limit(self, id):
        self.cursor.execute(f"SELECT views_count FROM offers WHERE id = {id}")
        views = self.cursor.fetchall()
        self.cursor.execute(f"SELECT views_limit FROM offers WHERE id = {id}")
        views_limit = self.cursor.fetchall()

        try:
            return views[0]['views_count'] < views_limit[0]['views_limit']
        except IndexError:
            return False

    @Sqliter.check_connection
    def get_business_name(self, id):
        self.cursor.execute(f"SELECT name FROM businesses WHERE id = {id} ")
        result = self.cursor.fetchall()
        try:
            return result[0]['name']
        except IndexError:
            return []


    @Sqliter.check_connection
    def get_business_id(self, id):
        self.cursor.execute(f"SELECT bus_id FROM offers WHERE id = {id}")
        result = self.cursor.fetchall()
        try:
            return result[0]['bus_id']
        except IndexError:
            return []

    @Sqliter.check_connection     
    def increment_views(self, id):
        self.cursor.execute(f"UPDATE offers SET views_count = views_count + 1 WHERE id = {id}")
        self.commit()

def main():
    pass

if __name__ == '__main__':
    main()
