"""접속 설정: 환경변수 DATABASE_URL을 읽고 SQLAlchemy+psycopg3용으로 정규화한다."""

from __future__ import annotations

import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv

# psycopg3 드라이버를 명시한 SQLAlchemy 스킴.
_PSYCOPG_SCHEME = "postgresql+psycopg"

# psycopg3(libpq)가 이해하지 못해 걸러내야 하는 쿼리 파라미터.
# 예: Supabase의 ORM/Prisma용 문자열에 붙는 pgbouncer=true.
_DROP_QUERY_KEYS = {"pgbouncer"}


class MissingDatabaseURL(RuntimeError):
    """DATABASE_URL 환경변수가 없을 때 발생."""


def load_env() -> None:
    """.env 파일이 있으면 환경변수로 로드한다. 이미 설정된 값은 덮지 않는다."""
    load_dotenv(override=False)


def normalize_url(url: str) -> str:
    """Postgres URL을 SQLAlchemy+psycopg3 스킴으로 통일하고 미지원 파라미터를 제거한다.

    스킴:
    - ``postgres://...``        -> ``postgresql+psycopg://...``
    - ``postgresql://...``      -> ``postgresql+psycopg://...``
    - ``postgresql+psycopg://`` -> 그대로
    이미 다른 드라이버(``+asyncpg`` 등)가 명시돼 있으면 스킴은 건드리지 않는다.

    쿼리: psycopg3가 모르는 파라미터(``pgbouncer`` 등)는 걸러낸다.
    나머지 파라미터(``sslmode`` 등)는 유지한다.
    """
    url = url.strip()
    # 1) 드라이버 스킴 통일
    if not url.startswith("postgresql+"):
        for prefix in ("postgresql://", "postgres://"):
            if url.startswith(prefix):
                url = f"{_PSYCOPG_SCHEME}://{url[len(prefix):]}"
                break
    # 2) psycopg가 이해하지 못하는 쿼리 파라미터 제거
    parts = urlsplit(url)
    if parts.query:
        kept = [
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k not in _DROP_QUERY_KEYS
        ]
        url = urlunsplit(parts._replace(query=urlencode(kept)))
    return url


def get_database_url() -> str:
    """환경변수 DATABASE_URL을 정규화해 반환한다. 없으면 MissingDatabaseURL.

    .env 파일 로드는 하지 않는다(순수하게 환경변수만 본다). 필요하면
    호출 전에 :func:`load_env` 를 부른다.
    """
    raw = os.environ.get("DATABASE_URL")
    if not raw:
        raise MissingDatabaseURL(
            "DATABASE_URL이 설정되지 않았습니다. .env.example을 참고해 .env에 채우세요."
        )
    return normalize_url(raw)
