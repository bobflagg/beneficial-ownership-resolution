"""bor.build_lwc — materialize `landlords_with_connections` (lwc) from `wow_landlords`.

lwc is the node/edge substrate every layer keys off (one node per distinct (name, standardized
business address), with the precomputed name/address connections). The JustFix `justfixwow` dump
ships the *input* (`wow_landlords`) but not this derived table, so BOR builds it here with WoW's
own SQL (vendored verbatim in ``sql/landlords_with_connections.sql``). This is what lets BOR run
against the data alone — no WatchlineNYC pipeline. See docs/data.md.

    uv run python -m bor.build_lwc                # build (drops + rebuilds; idempotent)
    uv run python -m bor.build_lwc --verify-only  # just report the existing table

NOTE: nodeid = row_number(), so a rebuild renumbers the nodes. That is fine within one build
(all layers read the same lwc), but ids are not stable across builds — see docs/parity.md.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from bor.db import pg_conn

SQL_PATH = Path(__file__).parent / "sql" / "landlords_with_connections.sql"

# WoW's lwc over the reference wow_landlords dump has ~this many nodes; a warn-only sanity signal
# (the dump changes over time).
EXPECTED_ROWS_HINT = 118_493


def _counts(cur) -> tuple[int, int]:
    cur.execute("SELECT count(*) FROM wow_landlords")
    src = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM landlords_with_connections")
    return src, cur.fetchone()[0]


def build(conn) -> int:
    """Run the vendored SQL, materializing landlords_with_connections. Returns the row count."""
    sql = SQL_PATH.read_text()
    with conn.cursor() as cur:
        print("Building landlords_with_connections from wow_landlords (pg_trgm self-join) ...")
        t0 = time.perf_counter()
        cur.execute(sql)
        conn.commit()
        src, rows = _counts(cur)
        cur.execute("SELECT n.nspname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
                    "WHERE c.oid = to_regclass('landlords_with_connections')")
        schema = cur.fetchone()[0]
    dt = time.perf_counter() - t0
    print(f"  wrote {schema}.landlords_with_connections: {rows:,} nodes "
          f"from {src:,} wow_landlords rows  ({dt:.1f}s)")
    if abs(rows - EXPECTED_ROWS_HINT) > EXPECTED_ROWS_HINT * 0.1:
        print(f"  NOTE: expected ~{EXPECTED_ROWS_HINT:,} nodes for the reference dump; "
              f"got {rows:,} — verify the wow_landlords source if this is unexpected.")
    return rows


def verify(conn) -> None:
    """Read-only check that lwc exists, is non-empty, and carries edge info."""
    with conn.cursor() as cur:
        cur.execute("SELECT to_regclass('landlords_with_connections')")
        if cur.fetchone()[0] is None:
            raise SystemExit("landlords_with_connections not found — run `python -m bor.build_lwc` first.")
        src, rows = _counts(cur)
        cur.execute("SELECT count(*) FROM landlords_with_connections "
                    "WHERE name_match_info IS NOT NULL OR bizaddr_match_info IS NOT NULL")
        with_edges = cur.fetchone()[0]
    print(f"landlords_with_connections: {rows:,} nodes ({with_edges:,} with connections) "
          f"from {src:,} wow_landlords rows")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build or verify landlords_with_connections.")
    ap.add_argument("--verify-only", action="store_true",
                    help="only report the existing table, don't rebuild")
    args = ap.parse_args()
    conn = pg_conn()
    try:
        (verify if args.verify_only else build)(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
