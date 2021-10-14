from .sqliter import Sqliter

class Admin_sqliter(Sqliter):
    def __init__(self, connection):
        super().__init__(connection)


    @Sqliter.check_connection
    def check_if_exists(self, tg_id):
        self.cursor.execute(f"SELECT * FROM admins WHERE tg_id = {tg_id}")
        res = self.cursor.fetchall()
        return bool(len(res))

def main():
    pass

if __name__ == '__main__':
    main()
