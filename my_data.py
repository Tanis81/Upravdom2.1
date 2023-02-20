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

        if not os.path.isfile(self.path_to_file):
            self.made_data_base()
            pass #TODO доделать функцию по созданию полноценной базы данных со всеми необходимым связями. пока база создается вручную

    def made_tabel(self, tabel):
        with self.connection() as connection:
            cursor = connection.cursor()
            tabel_name = tabel.pop(0)
            cursor.execute("CREATE TABLE {}(ID integer PRIMARY KEY)".format(tabel_name))
            while len(tabel) > 0:
                column_name = tabel.pop(0)
                column_type = tabel.pop(0)
                cursor.execute(f'ALTER TABLE {tabel_name} ADD {column_name} {column_type}')
            connection.commit()
            pass

    def return_columns_from_tabel(self, tabel):
        with self.connection() as connection:
            cursor = connection.cursor()
            columns = cursor.execute('select * from {}'.format(tabel))
            return [a[0] for a in columns.description]

    def return_list_of_tabels(self):
        with self.connection() as connection:
            cursor = connection.cursor()
            tabel_list = cursor.execute('''PRAGMA table_list''')
            return [a[1] for a in tabel_list.fetchall()]

    def insert_new_row(self, tabel, row):
        with self.connection() as connection:
            cursor = connection.cursor()
            sqlite_select_query = f"""SELECT ID from {tabel}"""
            cursor.execute(sqlite_select_query)
            ID = [a for a in cursor.fetchall()]
            if not ID:
                new_ID = 1
            else:
                new_ID = max([a[0] for a in ID]) + 1

            if isinstance(row, list):
                row = tuple([new_ID] + row)
            else:
                row = tuple([new_ID] + [row])
            num_values = "?, " * len(row)
            num_values = num_values[:len(row) * 3 - 2]
            sqlite_insert_query = f"""INSERT INTO {tabel} VALUES({num_values})"""
            cursor.execute(sqlite_insert_query, row)
            connection.commit()
        pass

    def update_row_in_tabel(self, tabel, ID, dict_updation):
        with self.connection() as connection:
            cursor = connection.cursor()
            for column, val in dict_updation.items():
                print(column, val)
                sqlite_insert_query = f"""Update {tabel} set {column} = '{val}' where ID = {ID}"""
                print(sqlite_insert_query)
                cursor.execute(sqlite_insert_query)
                connection.commit()
        pass

    def del_row_from_tabel(self, tabel, ID):
        with self.connection() as connection:
            cursor = connection.cursor()
            sqlite_insert_query = f"""DELETE FROM {tabel} WHERE ID = {ID}"""
            cursor.execute(sqlite_insert_query)
            connection.commit()
        pass

    def read_tabel(self, tabel):
        with self.connection() as connection:
            cursor = connection.cursor()
            sqlite_select_query = f"""SELECT * from {tabel}"""
            cursor.execute(sqlite_select_query)
            return cursor.fetchall()

    def connection(self):
        try:
            connection = sqlite3.connect(self.path_to_file)
            return connection
        except Error:
            print("Conection Error") #TODO сделать вывод в основной программе и переход к созданию базы или поиску пути к ранее созданной базе
            pass

    def made_data_base(self, init_file = 'init.csv', init_tabels_connections = 'init_tabels_connections.csv'):
        # TODO сделать функции по созданию полноценной базы данных со всеми необходимым связями.
        #  пока база создается вручную. планируется в создавать два файла csv в первый 'init.scv'
        #  записывать сведения о создаваеемых в базе таблицах и колонках таблиц,
        #  во второй 'init_tabels_connections.csv' - сведения о связях (в четырех столбцах main_tabel,
        #  main tabel column(ключевой столбец), slave_tabel, slave_tabel_column - связанное поле выбирающее
        #  значения из материнской таблицы
        #TODO добавить таблицу с условными связями (например когда выбирается тип подателя жалобы и
        # на этом основании производится сопоставление ID из таблицы зарегистрированных или таблицы собственников


        self.conection = sqlite3.connect(self.path_to_file)
        self.conection.close()

        with open(init_file, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for line in reader:
                if len(line) > 0:
                    self.made_tabel(line)

        with open(init_tabels_connections, "r") as file:
            reader = csv.reader(file, delimiter=",")
            #print(self.return_columns_from_tabel('tabels_connections'))
            for line in reader:
                if len(line) > 0:
                    self.insert_new_row('tables_connections', line)

        self.insert_new_row('holder', 'нет')
        self.insert_new_row('holder', 'да')
        self.insert_new_row('registration', 'нет')
        self.insert_new_row('registration', 'да')
        self.insert_new_row('membertsg', 'нет')
        self.insert_new_row('membertsg', 'да')

        self.insert_new_row('type1_object', 'квартира')
        self.insert_new_row('type1_object', 'машино-место')
        self.insert_new_row('type1_object', 'офис')

        self.insert_new_row('type2_object', 'жилое')
        self.insert_new_row('type2_object', 'нежилое')

        self.insert_new_row('type3_object', 'коммерческое')
        self.insert_new_row('type3_object', 'некоммерческое')

        self.insert_new_row('type_petition', 'почта')
        self.insert_new_row('type_petition', 'личный прием')
        self.insert_new_row('type_petition', 'электронная почта')
        self.insert_new_row('type_petition', 'диспетчер')

        pass

Connected_base()