# Paper → artifact map

Where each contribution of *"Leads, Not Verdicts: Reliability-Typed Beneficial-Ownership Resolution
for Housing Accountability"* is realized in this repository.

| # | Paper contribution | In this artifact |
|---|---|---|
| 1 | Reframing beneficial-ownership resolution as an accountability problem with *asymmetric* harms (false merge → over-attribution; false split → evasion) | `README.md` ("What it resolves"); the two directions are measured separately by `bor.eval.divergence`. |
| 2 | Reliability-typed provenance — inference vs. directly-sourced ("leads, not verdicts") | `OwnerGroup.composition` (`identity` / `deed_only` / `deed_bridged`) types each group's evidentiary basis; the `split` field on `OperationalNetwork` marks exact (WCC) vs. inferred-tail (Louvain). |
| 3 | Three-layer decomposition (operation / management / ownership) held to distinct standards | `bor.operational_network` (operation), `bor.owner_groups` (ownership), management (`MANAGED_BY`) lives in WatchlineNYC. |
| 4 | Auditable, recall-biased resolution ladder + precision guards — the name-free deed veil-pierce with the linked-successor guard, aggregator masking, co-op/condo exclusion | `bor.deed_edges` (the veil-pierce + guards), `nlr` (record linkage), aggregator masking in `bor.operational_network` and `nlr.splink_source`, co-op/condo drop in `bor.owner_groups`. |
| 5 | An evaluation methodology — paired head-to-head vs. registration clustering; INDETERMINATE class; circularity + data-vintage controls | `bor.eval.divergence` (the paired divergence: 760 crossing / 616 hiding) and `bor.eval.gate` (the WoW gate) are built. The stratified adjudication frame (INDETERMINATE class + controls) is the remaining v1 item — see the roadmap. |
| 6 | Dual-use reflection; contestability | Reflected in the release design: `bor.export` is person-free by default (BBL-keyed, opaque ids); `README.md` "Responsible use". |

## Reproducibility

`docs/parity.md` records how each layer was validated against the live WatchlineNYC knowledge
graph, and the reproducibility ceiling of each (owner groups: 100% of nodes, deterministic;
operational network: 99.9% of portfolios, WCC-exact with an approximate Louvain tail). The
headline divergence figures (760 / 616) are confirmed two independent ways — on-graph
(`compare_kg --divergence`) and off-graph (`bor.eval.divergence`).

## Layers ↔ modules

- Record linkage (false-split fix) → dependency [`nlr`](https://github.com/bobflagg/nyc-landlord-resolution)
- Deed veil-pierce → `bor.deed_edges`
- Beneficial owner group → `bor.owner_groups` (`resolve_owner_groups`)
- Operational network → `bor.operational_network` (`resolve_operational_networks`)
- Benchmark → `bor.eval.divergence`, `bor.eval.gate`
- Dataset export → `bor.export`
