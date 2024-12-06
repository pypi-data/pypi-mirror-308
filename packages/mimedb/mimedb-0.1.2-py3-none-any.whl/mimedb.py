import sqlite3
import zlib
from datetime import UTC, datetime
from typing import Iterable


class MimeDB:
    def __init__(self, path, compress_level: int = 9):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.execute(
            """
            create table if not exists content(
              id integer primary key,
              key text unique not null,
              url text,
              body blob,
              content_type text,
              last_update_utc text
            )
            """
        )
        self.compress_level = compress_level

    def close(self):
        self.db.close()

    def set(
        self,
        key: str,
        body: bytes,
        content_type: str | None = None,
        url: str | None = None,
    ):
        compressed = zlib.compress(body, level=self.compress_level)
        last_update_utc = str(datetime.now(UTC))
        self.db.execute(
            """
            insert or replace into content
            (key, url, body, content_type, last_update_utc)
            values (?, ?, ?, ?, ?)
            """,
            (key, url, compressed, content_type, last_update_utc),
        )

    def get(self, key: str):
        row = self.db.execute(
            """
            select body, content_type from content
            where key = ?
            """,
            (key,),
        ).fetchone()
        if row is None:
            return None, None
        body, content_type = row
        return zlib.decompress(body), content_type

    def scan(self) -> Iterable:
        cursor = self.db.execute(
            """
            select key, body, content_type from content
            """
        )
        for key, body, content_type in cursor:
            body = zlib.decompress(body)
            yield key, body, content_type

    def exists(self, key: str):
        row = self.db.execute(
            """
            select 1 from content
            where key = ?
            """,
            (key,),
        ).fetchone()
        return row is not None

    # experimental feature
    def begin(self):
        self.db.execute("begin immediate")

    # experimental feature
    def commit(self):
        self.db.execute("commit")
