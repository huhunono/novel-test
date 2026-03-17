"""Database query helpers for test-layer DB validation.

These are plain functions (not fixtures). Import directly where needed.
"""
from typing import Dict, Optional, Sequence

import pymysql.connections


def db_one(
    conn: pymysql.connections.Connection,
    sql: str,
    params: Optional[Sequence] = None,
) -> Optional[Dict]:
    """Execute a query and return the first row, or None."""
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()


def db_all(
    conn: pymysql.connections.Connection,
    sql: str,
    params: Optional[Sequence] = None,
) -> Sequence[Dict]:
    """Execute a query and return all rows."""
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()
