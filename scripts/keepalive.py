"""Pings Supabase with a trivial query so the free-tier project never auto-pauses.

Run manually with DATABASE_URL set, or via the supabase-keepalive GitHub Actions workflow.
"""
import os
import sys

import psycopg2


def main():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL is not set", file=sys.stderr)
        sys.exit(1)

    try:
        conn = psycopg2.connect(database_url, connect_timeout=10)
        with conn.cursor() as cur:
            cur.execute("select 1")
            cur.fetchone()
        conn.close()
        print("Supabase keep-alive ping OK")
    except Exception as exc:
        print(f"Supabase keep-alive ping FAILED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
