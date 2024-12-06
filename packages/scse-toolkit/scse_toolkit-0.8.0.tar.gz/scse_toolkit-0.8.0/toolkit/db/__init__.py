import sqlite3

from . import models as m
from . import query as q
from . import sqla as sa
from . import types as t

models = m
query = q
sqla = sa
types = t


@sqla.event.listens_for(sqla.Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable sqlite `foreign_keys` feature upon connecting."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
