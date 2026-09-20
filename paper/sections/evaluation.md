# Evaluation

> **Draft section.** The design, sampling frame, and metrics below are frozen; the **results tables
> are pending the blind adjudication** (see §Results). Full methodology: [`../eval-protocol.md`](../eval-protocol.md);
> harness: `bor.eval.sample` / `bor.eval.score`.

## What we measure, and why this way

Beneficial-ownership resolution is a claim about identifiable parties, and its errors are
asymmetric: a **false merge** over-attributes buildings to someone (a wrongful-targeting and
defamation risk), while a **false split** lets a real owner evade accountability. We therefore
evaluate the *correctness of the system's decisions* — when it asserts that two landlord records
are the same owner (a merge), or deliberately keeps them apart (a split), is that call right? — and
we lead with **precision**, the merge-side (costly-error) property.

Two design commitments follow from treating this as an *accountability inference*, not a lookup:

1. **Ground truth is the public record, adjudicated by humans — not the system's own output.** The
   unit is a *pair* of landlord records; two annotators, **blind** to which system produced the pair
   and to the signal that linked it, label each pair `SAME` / `DIFFERENT` / `INDETERMINATE` from
   primary sources (ACRIS deeds, NYS DOS filings, HPD registrations, court/enforcement records). A
   *golden rule* forbids counting the system's own edge as evidence: the annotator must corroborate
   the call from records the heuristic did not use.
2. **`INDETERMINATE` is a first-class outcome.** The public record often cannot settle ownership;
   such pairs are **excluded from the precision denominator**, and we report **coverage**
   (`1 − INDETERMINATE/n`) separately — how often the record can decide at all. This keeps precision
   honest about what public data can and cannot establish, consistent with "leads, not verdicts."

## Stratified sampling

Uniform sampling is useless — almost all random pairs are trivial non-matches. We sample where the
system exercises judgment, drawing each stratum by simple random sample from its frame and recording
the frame size for preregistration. The frozen frame (seed 42, snapshot date `D`):

| Stratum | Decision it probes | Frame | n |
|---|---|---:|---:|
| **S1a** deed-held | merge via a held multi-parcel deed | 885 | 70 |
| **S1b** deed-linked-successor | merge via the `$0` re-deed-into-shells recovery | 52 | 52 |
| **S2** model | merge via probabilistic record linkage (Splink) | 11,742 | 150 |
| **S3** aggregator-split | *keeping apart* landlords who share a masked aggregator office | 438 | 120 |
| **S4** hard-negative | *not merging* a shared surname / shared address | 7,083 | 120 |
| **Total** | | | **512** |

The merge strata (S1, S2) measure **merge precision**; the split strata (S3, S4) measure **split
precision** — that the operational-nexus masking and the "shared office ≠ shared owner" rule keep
apart parties that public record confirms are distinct. (S1b's frame is small because the
linked-successor shell game is genuinely rare — we take the whole frame.)

Recall is not estimable from a pair-precision sample; we gauge it separately against **recall
anchors** — operators whose complete portfolios are externally documented (e.g. Steven Croman via
the Attorney General settlement) — checking whether the resolved group recovers the known set.

## Metrics

Per stratum, over the adjudicable pairs (`INDETERMINATE`/`UNRESOLVED` excluded), with **Wilson 95%
confidence intervals** on every proportion:

- **Strict precision (C1 only)** vs **inclusive precision (C1 + C2).** Each correct `SAME` is typed
  **C1** — corroborated by evidence *independent* of the signal the system used — or **C2** —
  verifiable only through the same record the system keyed on (e.g. a deed-only `SAME` whose sole
  support is that deed). Strict precision credits only C1; the **C2 share** quantifies how much
  correctness rests on the system's own input. This is the circularity control, made numeric.
- **Coverage** = `1 − INDETERMINATE/n`.
- **Inter-annotator agreement** (Cohen's κ), target κ ≥ 0.70; a stratum below it is diagnosed.
- **Paired head-to-head vs. Who Owns What** (McNemar): on pairs where the two systems disagree,
  adjudication decides who is right, testing whether the divergence favors this system.

## Controls

- **Circularity:** blinding to system and signal, plus the golden rule (no self-evidence); residual
  same-source reliance is surfaced by the C1/C2 split rather than hidden.
- **Data vintage:** decisions and evidence are evaluated as of a fixed snapshot `D`; disagreements
  are bucketed for "record changed after `D`" vs. a genuine error before results are read.
- **Preregistration:** strata, frame, codebook, and metrics are frozen before adjudication
  (`bor.eval.sample` writes a `frame_manifest.json` with the seed, git commit, and per-stratum
  frame/n).

## Reproducibility

The comparison this evaluation adjudicates is the population-scale **divergence** from Who Owns What:
760 owner groups cross WoW portfolios and 616 WoW portfolios hide more than one owner
(`bor.eval.divergence`; cross-validated on-graph and off-graph, `../../docs/parity.md`). Divergence
says *how much* the two systems differ; this evaluation says *which is right where they differ* and
*how precise* the merge/split decisions are. The sample is deterministic given the seed; the
resolution is reproducible to ~0.05% (Splink u-sampling; `../../docs/parity.md`).

## Results

**Pending blind adjudication.** With `annotations.jsonl` in hand, `bor.eval.score` emits
per-stratum precision (strict/inclusive) with Wilson CIs, coverage, C2 share, κ, and the McNemar
head-to-head. The tables below are the shells to populate:

| Stratum | n | coverage | strict precision [95% CI] | inclusive [95% CI] | C2 share |
|---|---|---|---|---|---|
| S1a · S1b · S2 (merges) | | | *TBD* | *TBD* | |
| S3 · S4 (splits) | n | coverage | split precision [95% CI] | | |

_Inter-annotator κ: TBD. Head-to-head vs. WoW (discordant pairs): TBD._
