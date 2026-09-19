"""Database connections for BOR.

BOR resolves ownership over the same NYC public-record Postgres as its record-linkage
dependency, ``nlr``, so it reuses ``nlr``'s connection shim — one ``PG*`` configuration and
one connection path for both layers (see ``.env.example``). ``nlr.db.pg_conn`` calls
``load_dotenv()`` and reads ``PGHOST``/``PGPORT``/``PGDATABASE``/``PGUSER``/``PGPASSWORD``.

The DuckDB-over-public-CSVs path (``nlr.db.duckdb_conn``) is re-exported for the v2
no-database reproduction milestone; v1 uses ``pg_conn``.
"""
from nlr.db import pg_conn

try:  # duckdb path is a v2 concern; tolerate older nlr without it
    from nlr.db import duckdb_conn
except ImportError:  # pragma: no cover
    duckdb_conn = None

__all__ = ["pg_conn", "duckdb_conn"]
