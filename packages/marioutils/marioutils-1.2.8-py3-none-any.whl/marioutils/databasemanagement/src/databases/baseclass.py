from marioutils.databasemanagement.src import exceptions
import sqlalchemy
from sqlalchemy.pool import PoolProxiedConnection
from sqlalchemy.engine.interfaces import DBAPICursor
from abc import ABC, abstractmethod

class DatabaseNew(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.__create_pool()

    def __enter__(self):
        self.temp_conn, self.temp_cursor = self.__prepare()
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.temp_conn.close()
        self.temp_conn = self.temp_cursor = None

    @property
    def connected(self):
        try:
            conn, cursor = self.__prepare()
            cursor.execute("SELECT 1 as TEST")
        except Exception:
            return False
        else:
            return True
        finally:
            conn.close()

    @abstractmethod
    def __getconn(self):
        raise NotImplementedError
    
    def __create_pool(self):
        self.pool = sqlalchemy.pool.QueuePool(self.__getconn, max_overflow=10, pool_size=5)

    def __prepare(self):
        #get connection from pool
        conn = self.pool.connect()
        cursor = conn.cursor()
        return conn, cursor


    def execute(self, query: str, vals: list[tuple] | tuple = ()):
        if isinstance(vals, list):
            self.temp_cursor.executemany(query, vals)
        else:
            self.temp_cursor.execute(query,vals)
        self.temp_conn.commit()
        if isinstance(vals, list):
            res = self._fetchall()
        else:
            res = self._fetchone()
        return res

    def _fetchall(self):
        try:
            res = list(self.temp_cursor.fetchall())
        except Exception as e:
            raise Exception("Error while fetching data") from e
        else:
            return res

    def _fetchone(self):
        try:
            res = self.temp_cursor.fetchone()
        except Exception as e:
            raise Exception("Error while fetching data") from e
        else:
            return res
        
    def __format_conditions(data: dict):
        conditions = []
        for key, value in data.items():
            if isinstance(value, (int, float)):
                condition = f"{key} = {value}"
            elif isinstance(value, str):
                condition = f"{key} = '{value}'"
            elif isinstance(value, bool):
                condition = f"{key} = {int(value)}"
            else:
                raise TypeError(f"Cannot cast SQL where clause for data type {type(value)}")
            conditions.append(condition)
            return " AND ".join(conditions)

    def select(self, query: str, vals: tuple = ()):
        return self.execute(query, vals)

    def insert(self, query: str, vals: list[tuple] | tuple = ()):
        return self.execute(query, vals)
    
    def exec_stored_procedure(self, procedure_name: str, vals: list[tuple] | tuple = ()):
        return self.temp_cursor.callproc(procedure_name, vals)

    

    



class Database():

    def __init__(
            self,
            server: str,
            user: str,
            password: str,
            database: str = None,
            as_dict: bool = True,
            port: int = 1333,
            pool_size: int | sqlalchemy.pool.NullPool = 5,
            max_overflow: int = 10):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.as_dict = as_dict
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self._connection = None
        self._cursor = None
        self._pool = None
        if self.pool_size == sqlalchemy.pool.NullPool:
            pass
        else:
            if self.pool_size < 1:
                raise exceptions.PoolSizeMinException
            if self.max_overflow < self.pool_size:
                raise exceptions.MaxOverflowSizeException
            self.create_pool()

    def __enter__(self):
        self.connect()
        self.get_cursor()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close_connection()

    def get_connection(self):
        raise NotImplementedError

    def connect(self):
        self._connection = self._pool.connect()

    @property
    def connection(self):
        return self._connection

    @property
    def connected(self) -> bool:
        try:
            conn = self._pool.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT 1 AS test')
            return True
        except Exception:
            return False

    @property
    def cursor(self):
        return self._cursor

    def get_cursor(self):
        if self._connection is None:
            raise exceptions.ConnectionException
        if self._cursor is None:
            self._cursor = self.connection.cursor()

    def create_pool(self):
        if self._pool is None:
            self._pool = sqlalchemy.pool.QueuePool(
                self.get_connection,
                max_overflow=self.max_overflow,
                pool_size=self.pool_size)

    @property
    def pool(self):
        return self._pool

    def select(self, query: str, vals: tuple = ()):
        if self._cursor is None:
            raise exceptions.CursorException
        try:
            self._cursor.execute(query, vals)
        except Exception as e:
            raise Exception("Error selecting data") from e
        else:
            res = self.fetchall()
            return res
        finally:
            self.close_connection()

    def insert(self, query: str, data: tuple | list[tuple] = ()) -> int:
        if self._cursor is None:
            raise exceptions.CursorException
        try:
            if isinstance(data, tuple):
                self._cursor.execute(query, data)
            else:
                self._cursor.executemany(query, data)
            self._connection.commit()
        except Exception as e:
            raise Exception("Error when inserting data") from e
        else:
            return self._cursor.rowcount
        finally:
            self.close_connection()

    def fetchall(self):
        try:
            res = list(self._cursor.fetchall())
        except Exception as e:
            raise Exception("Error while fetching results") from e
        else:
            return res

    def close_connection(self):
        self._connection.close()
