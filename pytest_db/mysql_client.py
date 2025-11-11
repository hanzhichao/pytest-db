import logging
from typing import List
from urllib.parse import urlparse, parse_qs

import pymysql

DEFAULT_MYSQL_PORT = 3306
DEFAULT_MYSQL_CHARSET = 'utf8'

LOGGER = logging.getLogger('pytest-db')

def parse_db_uri(db_uri):
    parsed_uri = urlparse(db_uri)
    assert parsed_uri.scheme == 'mysql', 'Only support mysql'

    user = parsed_uri.username
    password = parsed_uri.password
    host = parsed_uri.hostname
    port = parsed_uri.port or DEFAULT_MYSQL_PORT
    db = parsed_uri.path.lstrip('/')
    # db = parsed_uri.fragment

    charset = DEFAULT_MYSQL_CHARSET
    if parsed_uri.query is not None:
        charset = parse_qs(parsed_uri.query).get('charset', [DEFAULT_MYSQL_CHARSET])[0]

    db_conf = dict(host=host, port=int(port), user=user, password=password, db=db, charset=charset)
    return db_conf


class MySQLClient(object):
    def __init__(self, db_uri: str):
        db_conf = parse_db_uri(db_uri)
        db_conf.setdefault('charset', 'utf8')
        LOGGER.debug(f'Connect db: {db_conf["host"]}:{db_conf["port"]}')
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def query(self, sql: str) -> dict:
        LOGGER.debug(f'Query sql: {sql}')
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        LOGGER.debug(f"Query result: {result}")
        return result

    def query_all(self, sql: str) -> List[dict]:
        LOGGER.debug(f'Query sql: {sql}')
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        LOGGER.debug(f"Query result num: {len(result)}")
        return result

    def execute(self, sql):
        LOGGER.debug(f'Execute sql: {sql}')
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            LOGGER.exception(e)
            self.conn.rollback()

    def close(self):
        LOGGER.debug(f'Close db cursor and connection')
        self.cursor.close()
        self.conn.close()
