import psycopg2.extras


def list_topics(conn, active_only=False):
    query = "select * from topics"
    if active_only:
        query += " where active = true"
    query += " order by active desc, created_at desc"
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def get_topic(conn, topic_id):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select * from topics where id = %s", (topic_id,))
        return cur.fetchone()


def create_topic(conn, name, description, style, tone, duration_seconds):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            insert into topics (name, description, style, tone, duration_seconds)
            values (%s, %s, %s, %s, %s)
            returning id
            """,
            (name, description, style, tone, duration_seconds),
        )
        return cur.fetchone()["id"]


def update_topic(conn, topic_id, name, description, style, tone, duration_seconds):
    with conn.cursor() as cur:
        cur.execute(
            """
            update topics
            set name = %s, description = %s, style = %s, tone = %s,
                duration_seconds = %s, updated_at = now()
            where id = %s
            """,
            (name, description, style, tone, duration_seconds, topic_id),
        )


def set_topic_active(conn, topic_id, active):
    with conn.cursor() as cur:
        cur.execute(
            "update topics set active = %s, updated_at = now() where id = %s",
            (active, topic_id),
        )


def get_settings(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select * from settings where id = 1")
        return cur.fetchone()


def update_settings(
    conn,
    language,
    tone,
    default_duration_seconds,
    daily_limit,
    publish_time,
    timezone,
    auto_publish,
):
    with conn.cursor() as cur:
        cur.execute(
            """
            update settings
            set language = %s, tone = %s, default_duration_seconds = %s,
                daily_limit = %s, publish_time = %s, timezone = %s,
                auto_publish = %s
            where id = 1
            """,
            (
                language,
                tone,
                default_duration_seconds,
                daily_limit,
                publish_time,
                timezone,
                auto_publish,
            ),
        )


def list_shorts(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select * from shorts order by created_at desc")
        return cur.fetchall()


def get_short(conn, short_id):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select * from shorts where id = %s", (short_id,))
        return cur.fetchone()


def get_youtube_account(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select * from youtube_accounts limit 1")
        return cur.fetchone()
