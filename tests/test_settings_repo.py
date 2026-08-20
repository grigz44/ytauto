from unittest.mock import MagicMock

from app import repo


def make_conn(fetchone_result=None):
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = False
    cursor.fetchone.return_value = fetchone_result

    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


def test_update_settings_writes_all_fields():
    conn, cursor = make_conn()

    repo.update_settings(
        conn,
        language="en",
        tone="engaging",
        default_duration_seconds=45,
        daily_limit=2,
        publish_time="20:00",
        timezone="Asia/Kolkata",
        auto_publish=True,
    )

    query, params = cursor.execute.call_args[0]
    assert "update settings" in query.lower()
    assert params == ("en", "engaging", 45, 2, "20:00", "Asia/Kolkata", True)


def test_get_settings_returns_row():
    conn, cursor = make_conn(fetchone_result={"id": 1, "language": "en"})

    settings = repo.get_settings(conn)

    assert settings == {"id": 1, "language": "en"}
