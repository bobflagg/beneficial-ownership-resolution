# Methods

> **Draft section.** Describes the resolution method the artifact implements (`bor`, building on
> `nlr`). Companion: the [Evaluation](evaluation.md) section and [`../eval-protocol.md`](../eval-protocol.md).

## Data and entities

All inputs are already-public NYC records: HPD registrations and their owner contacts (owner name +
a Geosupport-standardized business address), ACRIS property deeds (grantor, grantee, consideration
amount, document type), and PLUTO (recorded owner, building class). We acquire no private data; the
method surfaces and organizes the public record, it does not collect.

The base entity is a **landlord node** — one distinct `(owner name, standardized business address)`
drawn from the HPD registrations, with its set of buildings (BBLs) attached. Two derived universes
sit above these nodes, and a third axis runs alongside them; keeping them apart is the core design
move.

## A three-layer ownership model

Registration-based tools (notably JustFix's Who Owns What) answer *who is behind a building* by
clustering landlord nodes on shared names and addresses into a single "portfolio." That collapses
three claims of different evidentiary weight into one. We separate them, and attach each a
**reliability type** — *directly-sourced* (Type I) or *inferred* (Type II):

- **Operational network** — *what a building operates through.* The connected components (with
  community splitting) of the shared-name / shared-address / resolved-owner graph — WoW's own notion
  of a portfolio, rebuilt here. Inferred; the fuzziest layer.
- **Beneficial owner group** — *who owns it.* A community built **only from ownership signals**
  (record linkage and deeds) and **never from a shared address**. Inferred.
- **Management** — *who runs it.* The disclosed managing agent (`MANAGED_BY`), taken directly from
  the HPD registration. Directly-sourced.

The governing rule is **"don't ask one signal two questions."** A shared registration office tells
you what a building *operates through*; it never tells you who *owns* it. So ownership is resolved
as its own community, and the two communities — operational network and owner group — are computed
by *the same connected-components algorithm over different edge sets*: the operational network
includes address edges; the owner group excludes them.

## The resolution ladder (the ownership layer)

Ownership is resolved by an auditable ladder of signals, deliberately **recall-biased with
documented precision guards** — because the costly error is a false *merge* (over-attributing
buildings to a party), we let each signal add links, and place the guards where a signal would
otherwise over-reach.

**1. Probabilistic record linkage** (`nlr`, Splink / Fellegi–Sunter) resolves one owner across
differently-named LLCs and typo'd or multi-office addresses — the false-*split* fix. It is tuned to
never fuse two different people, at some cost to recall: **name-anchored blocking** (a surname match
is required to score a pair), a **first-name veto** (JACOB ≠ JOSEF at one office), a **common-name
veto** (two unrelated JIN CHENs never merge), and **aggregator-address masking** (a registered-agent
office shared by many landlords is down-weighted so office-mates are not fused). A corporate-co-owner
**feedback pass** then bridges an owner's offices that share a private corporate parent — the
cross-office link name and address alone cannot reach — guarded by a corp-degree cap and the same
name vetoes. Validated at pairwise precision ≈ 0.996 against a hand-adjudicated gold set. Each
resolved entity emits a `CONNECTED_BY_SPLINK` edge.

**2. Deterministic edges.** Two further sources also emit `CONNECTED_BY_SPLINK`: a **registered-LLC**
edge joining nodes that are the same DOF owner of record, and a small **curated** table of
human-verified same-owner merges for residuals the model cannot reach (e.g. an operator split across
two management shells sharing only a rare exact name).

**3. The deed veil-pierce** (`CONNECTED_BY_DEED`) is the signal no name/address method can produce.
Buildings conveyed on **one ACRIS deed** share a grantee, so they share an owner regardless of what
their individual LLCs are named. Two guards keep it precise:

- a **latest-deed (held-since) rule** — two buildings are joined only when their *most recent*
  conveyance is the same multi-parcel deed, so a bundle re-sold since is not stale-merged;
- a **linked-successor guard** for the shell game's signature move — buy a block together, then
  re-deed each building into its own single-purpose LLC. A superseded joint deed still proves
  co-ownership when the joint grantee is the grantor of each parcel's latest deed *and* that onward
  transfer is a **nominal-consideration** `$0`/token restructuring (`docamount ≤ NOMINAL_MAX`), not
  an arm's-length sale — the check that separates a controlled re-deed from a genuine sale to an
  independent buyer.

**4. The owner group** is then the **connected components** of `CONNECTED_BY_SPLINK ∪
CONNECTED_BY_DEED` — a plain union-find over ownership edges only. No name or address glue enters, so
a shared management office cannot manufacture a phantom owner.

## Precision hygiene (shared across layers)

- **Aggregator masking.** A normalized business address shared by more than 25 distinct landlords is
  a registered-agent / management megaoffice; address edges touching it are dropped before the
  operational network is built, and the same degree threshold masks address evidence inside the
  linkage model. This is what lets the layers separate cleanly — the office is operational
  infrastructure, not ownership.
- **Co-op/condo exclusion.** A building whose owner-role HPD contacts are majority `CO-OP`/`CONDO` is
  owned by shareholders, not a landlord; the managing agent that signs its registration would
  otherwise resolve to a giant phantom "owner" across hundreds of unrelated boards. Such buildings
  are excluded from the ownership layer, and owner groups that are >50% co-op/condo are dropped as
  management artifacts.

## Reliability typing and composition

Every derived link is labeled **sourced or inferred**, and each owner group carries a **composition**
recording how its edges combine: `identity` (a single resolved record-linkage entity), `deed_only`
(the group exists purely via the deed veil-pierce — the intended name-free recovery), or
`deed_bridged` (a deed fuses two or more distinct identity entities — the cross-mechanism case, held
to a higher bar). This makes each claim's epistemic status explicit and lets the consumption layer
present a *typed evidence path* — "possibly connected to N other landlords via these deeds /
registrations" — rather than a named verdict.

## Implementation and reproducibility

The method runs **off-graph**, over Postgres, with no dependence on a graph database: the layers are
in-memory union-find (owner group) and connected-components + community detection (operational
network) over edge sets built from the public records. It is packaged as `bor` and depends on the
standalone record-linkage engine `nlr`; the one derived input table (the landlord graph) is built
in-repo from the public dump. The resolution reproduces the reference graph exactly for the
deterministic layers and to ~0.05% for the linkage-dependent counts (Splink `u`-sampling); see
[`../../docs/parity.md`](../../docs/parity.md).
