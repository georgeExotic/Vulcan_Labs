import tkinter as tk
import pandas as pd
import sqlite3
import datetime
import csv

from tkinter import filedialog

class sqlDatabase():
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        try:
            self.c.execute("CREATE TABLE data (data_set INT, load_kg FLOAT, position_mm FLOAT, timestamp TIMESTAMP, mass_g FLOAT, pressure_kpa FLOAT, density FLOAT)")
        except:
            pass

    def insert_data(self,collection_count,force,position,mass):
        timestamp = datetime.datetime.now()
        self.c.execute('''INSERT INTO data(data_set, load_kg, position_mm, timestamp, mass_g) VALUES(?,?,?,?,?);''', (collection_count, force, position, timestamp, mass))

    def select(self):
        self.c.execute('''SELECT * FROM data''')
        results = self.c.fetchall()
        # print(f'{results} \n')

    def export_data(self):
        self.db_df = pd.read_sql_query("SELECT * FROM data", self.conn)
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.wm_attributes('-topmost', 1)
        self.exportCSV()

    def exportCSV(self):
        self.export_file_path = filedialog.asksaveasfilename(parent=self.root,defaultextension='.csv')
        self.file_path = True

    def exportdb(self):
        self.db_df.to_csv(self.export_file_path, index = False, header=True)


sdb = sqlDatabase()
sdb.select()