import mysql.connector as sql

class MySQL:
    def __init__(self, user, password, ip):
        conn = sql.connect(host=ip, user=user, password=password, database='bookstore')
        self.cursor = conn.cursor()
