from collections import namedtuple

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import pathlib
from pathlib import Path

class BaseManager:
    def __init__(self, app):
        self.app = app
        self.database_settings = self.app.database_settings
        self.connection = None
    def set_connection(self, database_settings=None):
        if not database_settings:
            database_settings = self.database_settings
        connection = QSqlDatabase.addDatabase(database_settings.driver)
        connection.setDatabaseName(database_settings.file.as_posix()) #PyQT не воспринимает путь к файлу тип Windows, поэтому передаче подлежит путь as_posix() (метод класса Path)
        self.connection = connection
    def _get_cursor(self):
        self.connection.open()
        return QSqlQuery(self.connection)
    def _query(self, query):
        cursor = self._get_cursor()
        cursor.exec(query)
    @property
    def open(self):
        return self.connection.isOpen()
    def __del__(self):
        self.connection.close()

class Query(BaseManager):
    def __init__(self, app):
        super().__init__(app)

        pass




    #@classmethod
    #def _execute_query(cls, query, params=None):
    #    query = QSqlQuery()

    #    cursor = cls._get_cursor()
    #    cursor.execute(query, params)

app = namedtuple('app', ['database_settings'])
app.database_settings = namedtuple('database_settings',
                               ['driver', 'path', 'data_name', 'file'])
app.database_settings.driver= "QSQLITE"
app.database_settings.path = pathlib.Path.cwd()
app.database_settings.data_name= 'my_tsg.db'
app.database_settings.file = Path(app.database_settings.path, app.database_settings.data_name)

a = BaseManager(app)
a.set_connection()
a._query("""CREATE TABLE contacts (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name VARCHAR(40) NOT NULL, job VARCHAR(50), mail VARCHAR(40) NOT NULL)""")

print(a.connection.tables())
