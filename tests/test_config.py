"""config 순수 로직 테스트 (네트워크·비밀값 없음)."""

import pytest

from portoptim.config import MissingDatabaseURL, get_database_url, normalize_url


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("postgres://u:p@h:5432/db", "postgresql+psycopg://u:p@h:5432/db"),
        ("postgresql://u:p@h:5432/db", "postgresql+psycopg://u:p@h:5432/db"),
        ("postgresql+psycopg://u:p@h:5432/db", "postgresql+psycopg://u:p@h:5432/db"),
        ("  postgres://u:p@h/db  ", "postgresql+psycopg://u:p@h/db"),
        # pgbouncer 파라미터는 제거 (Supabase ORM 문자열).
        (
            "postgres://u:p@h:6543/db?pgbouncer=true",
            "postgresql+psycopg://u:p@h:6543/db",
        ),
        # 다른 파라미터(sslmode)는 유지, pgbouncer만 제거.
        (
            "postgres://u:p@h/db?pgbouncer=true&sslmode=require",
            "postgresql+psycopg://u:p@h/db?sslmode=require",
        ),
    ],
)
def test_normalize_url(raw, expected):
    assert normalize_url(raw) == expected


def test_normalize_url_keeps_other_drivers():
    url = "postgresql+asyncpg://u:p@h/db"
    assert normalize_url(url) == url


def test_get_database_url_reads_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://u:p@h:5432/db")
    assert get_database_url() == "postgresql+psycopg://u:p@h:5432/db"


def test_get_database_url_missing_raises(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(MissingDatabaseURL):
        get_database_url()
