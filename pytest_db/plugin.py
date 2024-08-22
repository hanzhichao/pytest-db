import os
import re
import pytest

from pytest_db.mysql_client import MySQLClient


def pytest_addoption(parser):
    parser.addoption('--db-uri', help='DB URI such like mysql://root:password@localhost:3306/test')
    parser.addini('db_uri', help='DB URI such like mysql://root:password@localhost:3306/test')


@pytest.fixture
def db_uri(request):
    return request.config.getoption('--db-uri') or request.config.getini('db_uri') or os.getenv('DB_URI')


@pytest.fixture
def db(db_uri):
    if not db_uri:
        pytest.skip('Not set db_uri')

    try:
        db = MySQLClient(db_uri)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        yield db
        db.close()
