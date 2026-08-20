from unittest.mock import MagicMock

from app import repo


def make_conn(fetchone_result=None, fetchall_result=None):
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = False
    cursor.fetchone.return_value = fetchone_result
    cursor.fetchall.return_value = fetchall_result or []

    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


def test_create_topic_inserts_and_returns_id():
    conn, cursor = make_conn(fetchone_result={"id": "topic-1"})

    topic_id = repo.create_topic(
        conn,
        name="Space Facts",
        description="Short facts about space",
        style="listicle",
        tone="engaging",
        duration_seconds=40,
    )

    assert topic_id == "topic-1"
    query, params = cursor.execute.call_args[0]
    assert "insert into topics" in query.lower()
    assert params == ("Space Facts", "Short facts about space", "listicle", "engaging", 40)


def test_update_topic_sets_all_fields():
    conn, cursor = make_conn()

    repo.update_topic(
        conn,
        topic_id="topic-1",
        name="Updated Name",
        description="Updated description",
        style="documentary",
        tone="calm",
        duration_seconds=60,
    )

    query, params = cursor.execute.call_args[0]
    assert "update topics" in query.lower()
    assert params == ("Updated Name", "Updated description", "documentary", "calm", 60, "topic-1")


def test_set_topic_active_disables_topic():
    conn, cursor = make_conn()

    repo.set_topic_active(conn, "topic-1", False)

    query, params = cursor.execute.call_args[0]
    assert "update topics" in query.lower()
    assert params == (False, "topic-1")


def test_set_topic_active_enables_topic():
    conn, cursor = make_conn()

    repo.set_topic_active(conn, "topic-1", True)

    query, params = cursor.execute.call_args[0]
    assert params == (True, "topic-1")


def test_list_topics_returns_all_by_default():
    rows = [{"id": "topic-1", "active": True}, {"id": "topic-2", "active": False}]
    conn, cursor = make_conn(fetchall_result=rows)

    topics = repo.list_topics(conn)

    assert topics == rows
    query = cursor.execute.call_args[0][0]
    assert "where active" not in query.lower()


def test_list_topics_active_only_filters_in_query():
    conn, cursor = make_conn(fetchall_result=[])

    repo.list_topics(conn, active_only=True)

    query = cursor.execute.call_args[0][0]
    assert "where active = true" in query.lower()


def test_get_topic_returns_none_when_missing():
    conn, cursor = make_conn(fetchone_result=None)

    topic = repo.get_topic(conn, "missing-id")

    assert topic is None
