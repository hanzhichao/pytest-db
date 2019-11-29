import re
import pymysql
import pytest
import logging


PATTEN = r'(?P<db_type>\w+?)://(?P<user>\w+?):(?P<password>\w+?)@(?P<host>.*?):(?P<port>\d+?)/(?P<db>\w+)'


def parse_db_uri(db_uri):
    db_type = user = password = host = port = db = None
    r = re.match(PATTEN, db_uri)
    if r:
        db_type, user, password, host, port, db = [r.group(item)
                                                   for item in ['db_type', 'user', 'password', 'host', 'port', 'db']]
    if not all([db_type, user, password, host, port, db]):
        raise ValueError(f'db_uri should be like mysql://root:password@localhost:3306/test')
    if 'mysql' not in db_type:
        raise TypeError('just support mysql for now')

    db_conf = dict(host=host, port=int(port), db=db, user=user, password=password)
    return db_conf


class DB(object):
    def __init__(self, db_conf,autocommit=True):
        db_conf.setdefault('charset', 'utf8')
        self.conn = pymysql.connect(**db_conf, autocommit=autocommit)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    def query(self, sql):
        logging.debug(f'query sql: {sql}')
        self.cur.execute(sql)
        result = self.cur.fetchall()
        logging.debug(f"query result: {result}")
        return result

    def change_db(self, sql):
        logging.debug(f'execute sql: {sql}')
        self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()


def pytest_addoption(parser):
    parser.addoption('--db-uri', help='DB URI such like mysql://root:password@localhost:3306/test')
    parser.addini('db_uri', help='DB URI such like mysql://root:password@localhost:3306/test')



@pytest.fixture(scope='session')
def db(request):
    db_uri = request.config.getoption('--db-uri') or request.config.getini('db_uri') or os.getenv('DB_URI')
    if not db_uri:
        pytest.skip('Not set db_uri')
    db_conf = parse_db_uri(db_uri)
    try:
        db = DB(db_conf)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        yield db
        db.close()
