import os

import psycopg2
from flask import g


def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")
    conn = psycopg2.connect(database_url, connect_timeout=5)
    conn.autocommit = True
    return conn


def get_db():
    """Returns a connection scoped to the current request, opened lazily."""
    if "db" not in g:
        g.db = get_connection()
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def check_connection():
    """Returns (status, error) where status is 'connected' | 'not configured' | 'error'."""
    if not os.environ.get("DATABASE_URL"):
        return "not configured", None
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("select 1")
                cur.fetchone()
            return "connected", None
        finally:
            conn.close()
    except Exception as exc:
        return "error", str(exc)
