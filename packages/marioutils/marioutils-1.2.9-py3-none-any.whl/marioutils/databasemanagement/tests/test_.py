import pytest
from .. import src
from ..src.databases.baseclass import Database
from ..src.databases.manager import create_db_manager
import os
import pymssql
from sqlalchemy.pool import NullPool
import mariadb

mssql_dict = {
    'server':os.getenv('DB_mssql_SERVER'),
    'user':os.getenv('DB_mssql_USER'),
    'password':os.getenv('DB_mssql_PASSWORD'),
    'database':os.getenv('DB_mssql_DATABASE'),
    'pool_size':NullPool}

maria_dict = {
    'server':os.getenv('DB_mariadb_SERVER'),
    'user':os.getenv('DB_mariadb_USER'),
    'password':os.getenv('DB_mariadb_PASSWORD'),
    'database':os.getenv('DB_mariadb_DATABASE'),
    'pool_size':NullPool}

#manager test
@pytest.mark.parametrize(
    "test_name, init_dict,_class",
    [
        ('MS',mssql_dict, src.MsSQLDatabase),
        ('Maria', maria_dict, src.MariaDatabase)
    ])
def test_correct_manager(test_name, init_dict, _class):

    manager: Database = create_db_manager(test_name, **init_dict)

    assert isinstance(manager, _class)


@pytest.fixture
def mssql_db():
    db = src.MsSQLDatabase(**mssql_dict)
    yield db


@pytest.fixture
def mssql_db_error():
    db_error = src.MsSQLDatabase(
            server=os.getenv('DB_mssql_SERVER'),
            port=os.getenv('DB_mssql_PORT'),
            user=os.getenv('DB_mssql_USER_ERROR'),
            password=os.getenv('DB_mssql_PASSWORD_ERROR'),
            database=os.getenv('DB_mssql_DATABASE'))
    yield db_error


@pytest.fixture
def maria_db():
    db = src.MariaDatabase(**maria_dict)
    yield db


@pytest.fixture
def maria_db_error():
    db_error = src.MariaDatabase(
            server=os.getenv('DB_mariadb_SERVER'),
            user=os.getenv('DB_mariadb_USER_ERROR'),
            password=os.getenv('DB_mariadb_PASSWORD_ERROR'),
            database=os.getenv('DB_mariadb_DATABASE'))
    yield db_error



def test_mssql_db_error(mssql_db_error):
    with pytest.raises(TypeError):
        with mssql_db_error as conn:
            conn.connected


def test_maria_db_error(maria_db_error):
    with pytest.raises(mariadb.Error):
        with maria_db_error as conn:
            conn.connected



def test_mssql_db_success(mssql_db):
    assert mssql_db.connected


def test_maria_db_success(maria_db):
    with maria_db as conn:
        assert conn.connected

@pytest.mark.skip('Not implemented')
def test_maria_db_select(maria_db):
    with maria_db as conn:
        query = "SELECT * FROM tests.test WHERE id = ?"
        vals = (1,)
        res = conn.select(query=query, vals=vals)
        assert res == [{'id': 1, 'test_name': 'test1'}]

@pytest.mark.skip('Not implemented')
def test_maria_db_insert(maria_db):
    with maria_db as conn:
        query = """INSERT INTO tests.test(test_name) VALUES(?)"""
        data = ('test',)
        res = conn.insert(query=query, data=data)
        assert res == 1


# @pytest.mark.skip('Not implemented')
def test_ms_db_insert(mssql_db):
    with mssql_db as conn:
        query = """INSERT INTO tests.test(test_name) VALUES(%s)"""
        data = ('test',)
        res = conn.insert(query=query, data=data)
        assert res == 1

# @pytest.mark.skip('Not implemented')
def test_ms_db_select(mssql_db):
    with mssql_db as conn:
        query = "SELECT * FROM tests.test WHERE id = %d"
        vals = (1,)
        res = conn.select(query=query, vals=vals)
        assert res == [{'id': 1, 'test_name': 'test'}]


