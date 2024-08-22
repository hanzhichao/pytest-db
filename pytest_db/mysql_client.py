import logging
import re
from typing import List
from urllib.parse import urlparse, parse_qs

import pymysql

# PATTEN = r'(?P<db_type>\w+?)://(?P<user>\w+?):(?P<password>\w+?)@(?P<host>.*?):(?P<port>\d+?)/(?P<db>\w+)'
DEFAULT_MYSQL_PORT = 3306
DEFAULT_MYSQL_CHARSET = 'utf8'


def parse_db_uri(db_uri):
    # db_type = user = password = host = port = db = None
    # r = re.match(PATTEN, db_uri)
    # if r:
    #     db_type, user, password, host, port, db = [r.group(item)
    #                                                for item in ['db_type', 'user', 'password', 'host', 'port', 'db']]
    # if not all([db_type, user, password, host, port, db]):
    #     raise ValueError(f'db_uri should be like mysql://root:password@localhost:3306/test')
    # if 'mysql' not in db_type:
    #     raise TypeError('just support mysql for now')
    parsed_uri = urlparse(db_uri)
    assert parsed_uri.scheme == 'mysql'

    user = parsed_uri.username
    password = parsed_uri.password
    host = parsed_uri.hostname
    port = parsed_uri.port or DEFAULT_MYSQL_PORT
    db = parsed_uri.fragment

    assert db != ''

    charset = DEFAULT_MYSQL_CHARSET
    if parsed_uri.query is not None:
        charset = parse_qs(parsed_uri.query).get('charset', [DEFAULT_MYSQL_CHARSET])[0]

    db_conf = dict(host=host, port=int(port), user=user, password=password, db=db, charset=charset)
    return db_conf


class MySQLClient(object):
    def __init__(self, db_uri: str):
        db_conf = parse_db_uri(db_uri)
        db_conf.setdefault('charset', 'utf8')
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def query(self, sql: str) -> dict:
        logging.debug(f'Query sql: {sql}')
        self.cursor.execute(sql)
        result = self.cursor.fetone()
        logging.debug(f"Query result: {result}")
        return result

    def query_all(self, sql: str) -> List[dict]:
        logging.debug(f'Query sql: {sql}')
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        logging.debug(f"Query result num: {len(result)}")
        return result

    def execute(self, sql):
        logging.debug(f'Execute sql: {sql}')
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logging.exception(e)
            self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()
