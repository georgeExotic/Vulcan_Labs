import sqlite3
import datetime

# def init():
#   conn = sqlite3.connect('data.db')
#   createTable(conn)
#   conn.close()

# def create_table(conn):
#   c = conn.cursor()
#   c.execute('''CREATE TABLE IF NOT EXISTS answers (
#       id INTEGER AUTOINCREMENT,
#       questionsId INTEGER,
#       answer INTEGER,
#       createdAt TIMESTAMP
#       )''')
#   conn.commit()

# def add_new_answer(questionId, answer):
#   now = datetime.datetime.now().ctime()
#   c = conn.cursor()
#   c.execute('''INSERT INTO answers (questionId, answer, createdAt) VALUES (?, ?, ?)''',
#       (questionId, answer, now))
#   conn.commit()

class sqlDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        try:
            self.c.execute('''CREATE TABLE data(force FLOAT, position FLOAT)''')
        except:
            pass

    def insert(self):
        force = 3.333
        position = 3434.099
        self.c.execute('''INSERT INTO data VALUES(?,?)''', (force, position))
        self.conn.commit()

    def select(self):
        self.c.execute('''SELECT * FROM data''')
        results = self.c.fetchall()
        print(results)

sdb = sqlDatabase()
sdb.insert()
sdb.select()