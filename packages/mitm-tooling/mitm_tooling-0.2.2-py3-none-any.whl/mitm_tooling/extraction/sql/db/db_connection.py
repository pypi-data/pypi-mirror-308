import sqlite3
import typing
from pathlib import Path

import sqlalchemy as sa
from pydantic import AnyUrl
from sqlalchemy import Engine


def create_sa_engine(db_url: AnyUrl, sqlite_extensions: list[str] | None = None, test_engine: bool = False,
                     **engine_kwargs) -> Engine:
    engine = sa.create_engine(str(db_url), **engine_kwargs)

    return engine
