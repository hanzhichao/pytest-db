import pytest

from pytest_db.mysql_client import parse_db_uri

@pytest.fixture(scope='session')
def db_uri():
    return 'mysql://root:passw0rd@localhost:3306/test?charset=utf8'

def test_parse_db_uri(db_uri):
    db_conf = parse_db_uri(db_uri)
    assert db_conf == {'host': 'localhost',
                       'port': 3306,
                       'user': 'root',
                       'password': 'passw0rd',
                       'db': 'test',
                       'charset': 'utf8'}

