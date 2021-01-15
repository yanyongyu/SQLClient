from typing import Any, Dict, Tuple, Optional

import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT


class SQL:

    def __init__(self):
        self._conn: Optional[pymysql.connections.Connection] = None

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value: pymysql.connections.Connection):
        if self._conn:
            self._conn.close()
        self._conn = value

    def connect(self, host: str, port: int, username: str, password: str):
        self.conn = pymysql.connections.Connection(
            host=host,
            port=port,
            user=username,
            password=password,
            autocommit=True,
            client_flag=CLIENT.MULTI_STATEMENTS,
            cursorclass=pymysql.cursors.DictCursor)
        print("connection established")

    def close(self):
        if self.conn:
            self.conn.close()
            print("connection closed")

    def execute(self, sql) -> Tuple[int, Tuple[Dict[str, Any], ...]]:
        if not self.conn:
            raise RuntimeError("No connection available")

        cursor = self.conn.cursor()
        rows = cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(rows, result)
        return rows, result  # type: ignore
