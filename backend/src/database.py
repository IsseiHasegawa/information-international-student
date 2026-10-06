import hashlib
import json
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


def connection():
    return psycopg.connect(os.getenv("DATABASE_URL", ""), row_factory=dict_row)


def init_db():
    schema = (Path(__file__).resolve().parents[1] / "schema.sql").read_text(encoding="utf-8")
    with connection() as db:
        db.execute(schema)


def get_page(url):
    with connection() as db:
        return db.execute("SELECT * FROM saved_pages WHERE url = %s", (url,)).fetchone()


def list_pages():
    with connection() as db:
        return db.execute("SELECT * FROM saved_pages ORDER BY id").fetchall()


def content_hash(page):
    content = json.dumps(
        {"title": page["title"], "content": page["content"], "links": page["links"]},
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def save_checked_page(url, page):
    """Save fetched data and return whether the displayed information changed."""
    new_hash = content_hash(page)
    with connection() as db:
        previous = db.execute(
            "SELECT content_hash FROM saved_pages WHERE url = %s", (url,)
        ).fetchone()
        changed = previous is None or previous["content_hash"] != new_hash
        db.execute("""
            INSERT INTO saved_pages (
                url, source_url, title, content_json, links_json, content_hash
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                source_url = EXCLUDED.source_url,
                title = EXCLUDED.title,
                content_json = EXCLUDED.content_json,
                links_json = EXCLUDED.links_json,
                content_hash = EXCLUDED.content_hash,
                last_checked_at = NOW(),
                last_changed_at = CASE
                    WHEN saved_pages.content_hash IS DISTINCT FROM EXCLUDED.content_hash
                    THEN NOW() ELSE saved_pages.last_changed_at
                END,
                last_check_status = 'ok',
                last_error = NULL
        """, (
            url, page["source"], page["title"],
            Jsonb(page["content"]), Jsonb(page["links"]), new_hash,
        ))
    return changed


def record_check_error(url, error):
    with connection() as db:
        db.execute("""
            UPDATE saved_pages SET last_checked_at = NOW(),
                last_check_status = 'error', last_error = %s
            WHERE url = %s
        """, (str(error)[:500], url))


def page_response(row, cached=True):
    return {
        "title": row["title"],
        "content": row["content_json"],
        "links": row["links_json"],
        "source": row["source_url"],
        "cached": cached,
        "last_checked_at": row["last_checked_at"].isoformat(),
        "last_changed_at": row["last_changed_at"].isoformat(),
        "last_check_status": row["last_check_status"],
        "last_error": row["last_error"],
    }
