import collections
import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel
from PyQt6.QtWidgets import QApplication
import pathlib
from pathlib import Path
import os.path


app = collections.namedtuple('app', ['app', 'user'])
app.user = 'Alex'

class Logger:
    def __init__(self):
        self.logs = list()
    def get_log(self, log):
        self.logs.append(log)

class Databasesettings:
    """
    используем в дальнейшем приложении если надо изменить настройки соединения с базой данных
    """
    database_settings = collections.namedtuple('databes_settings',
                                               ['driver', 'path', 'data_name', 'file'])
    database_settings.path = pathlib.Path.cwd()
    def __init__(self, driver = "QSQLITE", data_name = 'my_tsg.db'):
        self.database_settings.driver = driver
        self.database_settings.data_name = data_name
        self.database_settings.file = Path(self.database_settings.path, self.database_settings.data_name)
        pass

class BaseManager():
    connection = None
    app = None
    @classmethod
    def set_connection(cls, database_settings):
        connection = QSqlDatabase.addDatabase(database_settings.driver)
        connection.setDatabaseName(database_settings.file.as_posix()) #PyQT не воспринимает путь к файлу тип Windows, поэтому передаче подлежит путь as_posix() (метод класса Path)
        cls.connection = connection
    @classmethod
    def _get_cursor(cls):
        cls.connection.open()
        return QSqlQuery(cls.connection)
    @classmethod
    def _made_table_model(cls):
        cls.connection.open()
        return QSqlRelationalTableModel(cls.connection)

    def __init__(self, app):
        self.app = app
        self.database_settings = Databasesettings()
        self.set_connection(self.database_settings.database_settings)
    def __del__(self):

        self.connection.close()


class MadeTable(BaseManager):
    def __init__(self, app):
        super().__init__(app)
        self.logs = Logger()
    def made_table(self, table_name, foreign_key = None, child_column = None, **kwargs):
        cursor = self._get_cursor()
        columns = ', '.join(str(key) + ' ' +  str(val) for key, val in kwargs.items())
        if foreign_key:
            query_foreigh = ' FOREIGN KEY ' + child_column + \
                            ' REFERENCES ' + ''.join(str(key) for key in foreign_key.keys()) + '(' + \
                            ''.join(str(val) for val in foreign_key.values()) + ')'
            query = 'CREATE TABLE ' + table_name + ' (' + columns + query_foreigh + ')'
        else:
            query = 'CREATE TABLE ' + table_name + ' (' + columns +')'
        self.execute(cursor, query)
        pass
    def add_column(self, table_name, foreign_key = None, **kwargs):
        cursor = self._get_cursor()
        columns = ', '.join(str(key) + ' ' + str(val) for key, val in kwargs.items())
        if foreign_key:
            query_foreigh = ' REFERENCES ' + ''.join(str(key) for key in foreign_key.keys()) + '(' + \
                            ''.join(str(val) for val in foreign_key.values()) + ')'
            query = 'ALTER TABLE ' + table_name + ' ADD COLUMN ' + columns + query_foreigh
        else:
            query = 'ALTER TABLE ' + table_name + ' ADD COLUMN ' + columns
        self.execute(cursor, query)
        pass
    def execute(self, cursor, query):
        cursor.exec(query)
        new_log = cursor.lastQuery()
        try:
            self.logs.get_log(new_log)
        except:
            pass
        pass


class Select(BaseManager):
    def __init__(self, app):
        super().__init__(app)

class Insert(BaseManager):
    def __init__(self, app):
        super().__init__(app)

class Update(BaseManager):
    def __init__(self, app):
        super().__init__(app)

class Delete(BaseManager):
    def __init__(self, app):
        super().__init__(app)

class Drop(BaseManager):
    def __init__(self, app):
        super().__init__(app)

class Table(BaseManager):
    def __init__(self, app):
        super().__init__(app)
        self.logs = Logger()
        model = self._made_table_model()







if __name__ == '__main__':
#    database_settings = Databasesettings()
    a = MadeTable('app')
#    a.set_connection(database_settings.database_settings)
    a.made_table('contacts', foreign_key =  {'parent': 'parentid'}, child_column = 'child', **{'id': 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
                                'name': 'VARCHAR(40) NOT NULL','job': 'VARCHAR(50)',
                                'email':'VARCHAR(40) NOT NULL'})
    a.add_column('contacts', foreign_key =  {'parent': 'parentid'}, **{'em':'VARCHAR(40) NOT NULL'})





    #@classmethod
    #def _execute_query(cls, query, params=None):
    #    query = QSqlQuery()

    #    cursor = cls._get_cursor()
    #    cursor.execute(query, params)

#database_settings = collections.namedtuple('databes_settings',
#                                           ['driver', 'path', 'data_name', 'file'])
#database_settings.driver= "QSQLITE"
#database_settings.path = pathlib.Path.cwd()
#database_settings.data_name= 'my_tsg.db'
#database_settings.file = Path(database_settings.path, database_settings.data_name)

#a = BaseManager('app')
#a.set_connection(database_settings)
#a.made_tabel()
#print(a.connection.tables())



