import collections
import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication
import pathlib
from pathlib import Path
import os.path

class BaseManager():
    connection = None
    app = None
    @classmethod
    def set_connection(cls, database_settings):
        connection = QSqlDatabase.addDatabase(database_settings.driver)
        connection.setDatabaseName(database_settings.file.as_posix())
        cls.connection = connection
    @classmethod
    def _get_cursor(cls):
        cls.connection.open()
        return QSqlQuery(cls.connection)

    def __init__(self, app):
        self.app = app

    def made_tabel(self):
        cursor = self._get_cursor()
        cursor.exec(
            """
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                job VARCHAR(50),
                email VARCHAR(40) NOT NULL
            )
            """
        )
    #@classmethod
    #def _execute_query(cls, query, params=None):
    #    query = QSqlQuery()

    #    cursor = cls._get_cursor()
    #    cursor.execute(query, params)

database_settings = collections.namedtuple('databes_settings',
                                           ['driver', 'path', 'data_name', 'file'])
database_settings.driver= "QSQLITE"
database_settings.path = pathlib.Path.cwd()
database_settings.data_name= 'my_tsg.db'
database_settings.file = Path(database_settings.path, database_settings.data_name)

a = BaseManager('app')
a.set_connection(database_settings)
a.made_tabel()
print(a.connection.tables())



