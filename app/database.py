import mariadb


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        self.conn = mariadb.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.conn

    def get_cursor(self):
        if self.conn:
            return self.conn.cursor()
        else: raise ConnectionError("Database is not connected")
