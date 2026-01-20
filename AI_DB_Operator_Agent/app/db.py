"""DB 연결 헬퍼."""

from typing import List

import logging
import pymysql
import pymysql.cursors

from app.config import MYSQL_DB, MYSQL_HOST, MYSQL_PASS, MYSQL_PORT, MYSQL_USER

logger = logging.getLogger("db_agent")


def _get_conn():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        database=MYSQL_DB,
        # ?? ?????? ?? ??
        connect_timeout=5,
        read_timeout=5,
        write_timeout=5,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def db_query(sql: str, params: tuple = ()) -> List[dict]:
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description:
                rows = list(cur.fetchall())
                logger.info("DB 조회: rows=%s", len(rows))
                return rows
            logger.info("DB 조회: rows=0")
            return []
    finally:
        conn.close()


def db_execute(sql: str, params: tuple = ()) -> int:
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            affected = cur.execute(sql, params)
            logger.info("DB 조작: affected=%s", affected)
            return int(affected)
    finally:
        conn.close()
