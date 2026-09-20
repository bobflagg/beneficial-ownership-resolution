# Paper

Drafts and supporting material for *"Leads, Not Verdicts: Reliability-Typed Beneficial-Ownership
Resolution for Housing Accountability."* This is the paper's canonical home; the code + data
artifact it describes is this repository (`bor`), and its empirical claims are reproducible from
it directly (`python -m bor.eval.divergence`, `docs/parity.md`).

## Contents

- **`facct-abstract.md`** — the FAccT variant (fairness/accountability framing; harms-asymmetry,
  typed provenance, dual-use reflection). Primary target.
- **`paper-abstract.md`** — the base variant (systems + evaluation emphasis; COMPASS-leaning).
- **`eval-protocol.md`** — the evaluation methodology (paired vs Who Owns What, the INDETERMINATE
  class, circularity + data-vintage controls) — itself contribution #5.
- **`cases/`** — worked, WoW-verified case studies:
  - `case-escobar.md` — false *split* reunited (record linkage).
  - `case-miller.md`, `case-levitov.md` — false *merges* kept apart (shared office / shared manager).
  - `case-axl.md` — the name-free deed veil-pierce (two $0 shells reunited by one deed).

## Provenance & status

Copied from the WatchlineNYC `specs/` tree, which is where this work originated; BOR is now the
canonical home for the *paper* (WatchlineNYC keeps its product docs — the deck, pitches, roadmap).
The divergence figures here are the current rebuild (**616 portfolios hide >1 owner; 760 owners
cross portfolios**), confirmed two ways (on-graph `compare_kg --divergence` and off-graph
`bor.eval.divergence`); see `../docs/paper-mapping.md` for the contribution→module map.

Two caveats while these are freshly lifted:
- Some **internal cross-references** in these drafts still point at the original WatchlineNYC
  `specs/…` paths (not everything was copied). They'll be reconciled as the paper develops here.
- The manager-layer figure **1,461** (in `paper-abstract.md`) was **not** re-measured against the
  current rebuild — it predates the refresh and should be recomputed before it's cited.
- Supporting design/analysis notes (`ownership-model-spec.md`, `deed-gate-review.md`) were left in
  WatchlineNYC; bring them under `paper/notes/` if you want them here too.
