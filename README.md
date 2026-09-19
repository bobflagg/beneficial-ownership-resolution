# Beneficial Ownership Resolution

**Reliability-typed beneficial-ownership resolution over NYC public records.** Given the
city's public registration and deed record, it decides *who is behind a building* — and,
unlike registration clustering, it separates three claims of different evidentiary weight
(**operation**, **management**, **ownership**) and types each as **directly-sourced** or
**inferred**. Every derived link reads as an investigative lead, not a legal determination.

This is the software + data + benchmark artifact for the paper *"Leads, Not Verdicts:
Reliability-Typed Beneficial-Ownership Resolution for Housing Accountability."* It builds on
JustFix's [Who Owns What](https://github.com/JustFixNYC/who-owns-what) (WoW) — crediting and
benchmarking against it, not replacing it — and on the standalone record-linkage engine
[`nyc-landlord-resolution`](https://github.com/bobflagg/nyc-landlord-resolution) (`nlr`).

> **Status: v1 in progress.** Ships owner-group + deed + benchmark first; the operational-nexus
> layer (aggregator-masked WCC + Louvain) lands in v1.1. See the roadmap below.

## What it resolves

Registration clustering fails in two opposite, *asymmetrically harmful* directions:

- **False split** — one owner, fragmented across differently-named LLCs and typo'd offices,
  reads as many owners → a real owner evades accountability (harm borne by tenants).
  **Fixed** by probabilistic record linkage (`nlr`) → `CONNECTED_BY_SPLINK`.
- **False merge** — separate owners sharing a registration office read as one → buildings are
  over-attributed to a party (wrongful-targeting / defamation risk). **Fixed** by resolving
  ownership as its own community from ownership signals only, never a shared address.

### The layers (each separately typed)

| Layer | Question | Signals | Status |
|---|---|---|---|
| **Beneficial owner group** | Who *owns* it? | `CONNECTED_BY_SPLINK` ∪ `CONNECTED_BY_DEED` | **v1** |
| **Deed veil-pierce** | co-owned by conveyance? | ACRIS multi-parcel deed + linked-successor guard | **v1** |
| **Operational nexus** | What does it *operate through*? | name / address / splink, aggregator-masked (WCC + Louvain) | **v1.1** |
| **Management** | Who *runs* it? | `MANAGED_BY` (disclosed agent) | (in WatchlineNYC) |

The **deed veil-pierce** is the signature move: a name-free link from a shared ACRIS deed,
with a *linked-successor guard* that reaches owners who bought a block together and re-deeded
each building into its own `$0` single-purpose shell — the case no name/address method can see.
Precision hygiene: **aggregator-address masking** and **co-op/condo exclusion** (co-ops/condos
are owned by shareholders, not a landlord) remove management artifacts a naive inference mints.

## Install

```bash
uv sync                     # installs nlr from its pinned git tag (public; HTTPS, no creds)
cp .env.example .env        # set PG* for the NYC public-record Postgres
```

## Use  *(planned v1 API — see roadmap)*

```python
from bor import resolve_owner_groups
from bor.db import pg_conn

with pg_conn() as conn:
    groups = resolve_owner_groups(conn)   # {landlord_key: owner_group_id}, off-graph
```

## Evaluate — the paired benchmark against Who Owns What

The evaluation protocol is a core contribution: a paired head-to-head against
`wow.wow_portfolios` with an **INDETERMINATE** class, a **circularity control**, and a
**data-vintage control**. It reports where the layers diverge — how many WoW portfolios hide
more than one owner (a false merge), and how many owners cross WoW portfolios (a false split).

```bash
uv run python -m bor.eval.divergence     # the head-to-head divergence report
uv run python -m bor.eval.gate           # the WoW gate (does WoW split/over-lump these members?)
```

Worked case studies (reproducible): Croman, Escobar, Miller, Levitov, AXL, Citadel.

## How it relates to the other repos

```
nlr  (record linkage / false-split resolution)         ── standalone, gold-validated
  └── beneficial-ownership-resolution  (this repo)      ── + deed, owner groups, benchmark  [KG-free]
        └── WatchlineNYC  (the deployed product)        ── materializes the export into Neo4j; UI + agent
```

BOR is **KG-free** — it runs over Postgres (v1) and never requires Neo4j. WatchlineNYC consumes
BOR's export and is where the Neo4j graph, the conversational agent, and the public site live.

## Roadmap

- **v1** — beneficial owner group + deed veil-pierce + the WoW-comparison benchmark, computed
  off-graph from Postgres; the gold set and the six case studies; reproducible divergence report.
- **v1.1** — the operational-nexus layer (aggregator-masked WCC + Louvain), off-graph.
- **v2 (artifact review)** — DuckDB-native over the public HPD / ACRIS / PLUTO CSVs, so the whole
  thing reproduces with no private database (mirrors `nlr`'s public-CSV roadmap).

## Responsible use

Grounded **entirely in already-public record**; it surfaces and organizes, it does not collect.
Every inferred claim is typed as inferred and carries a standardized caveat — *leads, not
verdicts*. The merge-vs-split (precision-vs-recall) tradeoff is documented, not hidden. See the
paper's dual-use reflection; the dataset-release policy for this repo is deliberately scoped to
match it (a Phase-3 decision, tracked below).

## License

MIT.
