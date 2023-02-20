import sqlite3
from sqlite3 import Error

import csv
import pathlib
from pathlib import Path
import os.path

class Connected_base():
    def __init__(self, connected_db = "my_tsg.db"):
        self.connected_db = connected_db
        self.local_path = pathlib.Path.cwd()
        self.path_to_file = Path(self.local_path, self.connected_db)

        #if not os.path.isfile(self.path_to_file):
        #    self.made_data_base()
        #    pass #TODO доделать функцию по созданию полноценной базы данных со всеми необходимым связями. пока база создается вручную
    def connection(self):
        try:
            connection = sqlite3.connect(self.path_to_file)
            return connection
        except Error:
            print("Conection Error") #TODO сделать вывод в основной программе и переход к созданию базы или поиску пути к ранее созданной базе
            pass
    @property
    def return_list_of_tables(self):
        with self.connection() as connection:
            cursor = connection.cursor()
            tabel_list = cursor.execute('''PRAGMA table_list''')
            return [a[1] for a in tabel_list.fetchall()]
    def check_table_exists(self, tabel):
        return tabel in self.return_list_of_tables
    def return_columns_from_table(self, table):
        with self.connection() as connection:
            cursor = connection.cursor()
            columns = cursor.execute('select * from {}'.format(table))
            return [a[0] for a in columns.description]
    def check_column_exists(self, table, column):
        return column in self.return_columns_from_table(table)
    def execute_query(self, query):
        with self.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                connection.commit()
                print("Query successful")
            except Error as err:
                print(f"Error: '{err}'")
        pass
    def fetchall_query(self, query):
        with self.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                return cursor.fetchall()
            except Error as err:
                print(f"Error: '{err}'")
                return None
    def fetchall_factory(self, table):
        with self.connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            query = 'SELECT * FROM ' + str(table)
            cursor.execute(query)
            return cursor.fetchall()

    def create_table_query(self, table, columns_dict):
    #    query = "CREATE TABLE " + str(table) + " (ID integer PRIMARY KEY, "
    #    for column, type_column in columns_dict.items():
    #        if column in

#parent, text, parent_column, text, child, text, child_column, text

my_data = Connected_base()

c = my_data.fetchall_factory('tables_connections')

print([a['parent'] for a in c if a['child'] == 'holders' and a['child_column'] == 'object'])