from dataclasses import dataclass

import pytest

from mimedb import MimeDB


@dataclass
class DataHelper:
    key: str
    body: bytes
    content_type: str | None = None


@pytest.fixture()
def mime_db():
    md = MimeDB(":memory:")
    yield md
    md.close()


def test_set_get(mime_db):
    data = DataHelper(
        key="key1",
        body=b"{}",
        content_type="application/json",
    )
    mime_db.set(data.key, data.body, data.content_type)
    assert mime_db.get(data.key) == (data.body, data.content_type)

    data.content_type = "text/html"
    mime_db.set(data.key, data.body, data.content_type)
    assert mime_db.get(data.key) == (data.body, data.content_type)

    data.content_type = None
    mime_db.set(data.key, data.body, data.content_type)
    assert mime_db.get(data.key) == (data.body, None)


def test_exists(mime_db):
    data = DataHelper(
        key="key1",
        body=b"",
        content_type="text/plain",
    )

    assert mime_db.exists(data.key) is False

    mime_db.set(data.key, data.body, data.content_type)
    assert mime_db.exists(data.key) is True


def test_scan(mime_db):
    data = DataHelper(
        key="key1",
        body=b"",
        content_type="text/plain",
    )
    mime_db.set(data.key, data.body, data.content_type)
    data.key = "key2"
    mime_db.set(data.key, data.body, data.content_type)
    result_list = list(mime_db.scan())
    assert len(result_list) == 2


def test_transaction(mime_db):
    mime_db.begin()
    mime_db.set("1", b"1")
    mime_db.set("2", b"2")
    mime_db.commit()
    assert mime_db.get("1") == (b"1", None)
    assert mime_db.get("2") == (b"2", None)


def test_commit_or_rollback(mime_db):
    try:
        with mime_db.commit_or_rollback():
            mime_db.set("1", b"1")
            raise ValueError("test")
    except Exception:
        pass
    assert mime_db.get("1") == (None, None)

    with mime_db.commit_or_rollback():
        mime_db.set("1", b"1")
    assert mime_db.get("1") == (b"1", None)


def test_always_commit(mime_db):
    try:
        with mime_db.always_commit():
            mime_db.set("1", b"1")
            raise ValueError("test")
    except Exception:
        pass
    assert mime_db.get("1") == (b"1", None)
