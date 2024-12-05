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
