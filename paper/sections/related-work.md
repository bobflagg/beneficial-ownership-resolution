# Related Work

> **Draft section.** References are named in prose; **citation keys / bib entries are to be
> finalized and verified** (see the checklist at the end). Companion sections: [Methods](methods.md),
> [Evaluation](evaluation.md).

Our work sits at the intersection of four literatures: housing-accountability tooling, beneficial-
ownership transparency, entity resolution over public registries, and the algorithmic-accountability
study of identification systems. We take from each and depart from each in a specific way.

## Landlord and housing accountability tools

The closest system is JustFix's **Who Owns What** (WoW), which clusters HPD-registered buildings
into landlord "portfolios" from shared registration names and addresses and is widely used by
tenants, organizers, and reporters; the Housing Data Coalition and allied civic-tech efforts have
built related tooling over the same NYC open data (HPD registrations, ACRIS, PLUTO). Investigative
journalism has long assembled landlord portfolios by hand — "worst landlord" lists and property-
empire exposés — and public agencies publish enforcement and violation records. These establish both
the demand (tenants and reporters need to reach the party behind a shell) and the de-facto method
(registration clustering). **We build directly on WoW and benchmark against it**, but rather than
treat its portfolio as the answer we (i) show its single "portfolio" conflates operation,
management, and ownership, and (ii) resolve ownership as its own, separately-typed layer.

## Beneficial-ownership transparency

A policy and investigative literature treats beneficial-ownership disclosure as a public good — the
premise of the U.S. **Corporate Transparency Act**, the **FATF** anti-money-laundering
recommendations, and open-register efforts such as **Open Ownership** and the UK **People with
Significant Control** register — and cross-border investigations (ICIJ's Panama/Paradise Papers)
have shown the accountability value of linking entities across filings. Most of this work assumes
*disclosed* beneficial ownership (a register someone must file into) or reconstructs ownership
through leaked/bulk corporate data. **We instead infer beneficial-owner grouping from routinely-
published municipal records** — HPD registrations and ACRIS deeds — in a jurisdiction with no
beneficial-ownership register for rental LLCs, and we are explicit that the result is an inference,
not a disclosure.

## Entity resolution and portfolio construction

The technical core is probabilistic **record linkage** in the Fellegi–Sunter tradition, realized
here with **Splink**; the broader deduplication/entity-resolution literature (e.g. Christen's
data-matching work, and blocking/canopy methods) supplies the precision techniques we lean on —
name-anchored blocking and value-frequency vetoes. Portfolio/community construction uses standard
graph methods — connected components and the **Louvain** community-detection method (Blondel et al.).
Our contribution here is not a new matcher but a **name-free linkage signal** — a co-conveyance
**deed veil-pierce** with a linked-successor guard — that reaches same-owner links no name/address
matcher can (an owner who re-deeds a jointly-bought block into per-building `$0` shells), plus the
"same algorithm over different edge sets" separation of an *operational* community (address-
inclusive) from an *ownership* community (ownership-signals-only).

## Algorithmic accountability, identification harms, and contestability

FAccT-adjacent work studies the harms of systems that identify or score people. Two threads matter
here. First, **misidentification and aggregation harms**: risk-assessment and predictive-policing
critiques (e.g. the COMPAS debate) show the danger of presenting an *inference* with the authority
of a *fact*, and the "mosaic theory" of privacy (the *Jones* concurrence; Solove's work on
aggregation) shows that assembling individually-public records into one profile creates exposure the
sources do not individually carry — directly relevant to a system that links names, LLCs, addresses,
and deeds. Second, **transparency, provenance, and contestability**: documentation practices such as
datasheets and model cards, and the "contestable AI" literature, argue that responsible systems make
their claims' status legible and challengeable. **Our reliability typing operationalizes this**:
every derived link is labeled sourced or inferred and carries a standardized caveat ("leads, not
verdicts"), and the design keeps a human adjudicator in the loop rather than emitting a determination.

Unusually for this literature, our system's valence largely runs *toward* accountability — it exposes
actors who deliberately obscure ownership to the tenants and regulators with a legitimate interest in
reaching them — but we treat "already public" as a necessary, not sufficient, defense and analyze the
residual harms (misidentification of a namesake or a low-level signatory, home-address exposure, the
mosaic effect) in the dual-use reflection.

## Positioning — what is new

Against this backdrop, the paper's distinct contributions are: (1) **decomposing** the conflated
portfolio into three separately-verifiable, reliability-typed layers; (2) treating resolution as an
**accountability inference with asymmetric, oppositely-distributed harms** (false merge →
over-attribution; false split → evasion) rather than a pure accuracy problem; (3) the **name-free
deed veil-pierce** with its precision guards; and (4) an **evaluation methodology built for
accountability inference** — a paired, blind, public-record adjudication with an `INDETERMINATE`
class, a circularity control, and a data-vintage control (see [Evaluation](evaluation.md)) — that
refuses to claim ownership the public record cannot support.

---

### References to finalize

Verify and add bib entries for: JustFix *Who Owns What* / Housing Data Coalition; the Corporate
Transparency Act; FATF beneficial-ownership recommendations; Open Ownership; UK PSC register; ICIJ
(Panama Papers); Fellegi & Sunter (1969); Splink (UK Ministry of Justice); Christen, *Data Matching*;
Blondel et al. (2008), Louvain; the COMPAS/risk-assessment accountability debate; *United States v.
Jones* (2012) and Solove on aggregation/mosaic; datasheets (Gebru et al.) and model cards (Mitchell
et al.); the contestable-AI literature. Keep only sources actually cited in the final text.
