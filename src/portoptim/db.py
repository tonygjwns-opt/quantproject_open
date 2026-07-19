"""DB 연결: SQLAlchemy 엔진 생성과 연결 검증."""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from portoptim.config import get_database_url, load_env


def get_engine() -> Engine:
    """.env를 로드하고 정규화된 DATABASE_URL로 SQLAlchemy 엔진을 만든다."""
    load_env()
    return create_engine(get_database_url())


def check_connection() -> bool:
    """SELECT 1을 실행해 연결이 살아있는지 확인한다. 성공하면 True."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
    return result == 1


if __name__ == "__main__":
    if check_connection():
        print("DB 연결 OK (SELECT 1)")
    else:
        print("DB 연결 실패")
