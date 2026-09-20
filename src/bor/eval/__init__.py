"""bor.eval — the evaluation protocol.

A paired, honest comparison of the beneficial-owner-group partition against JustFix's Who Owns
What registration clustering. This is a *divergence* measure — how far apart the two groupings are
and in which direction — not an accuracy claim; there is no ground truth here, and which
divergences are improvements is what blind adjudication (the INDETERMINATE-class eval) decides.

Modules:
    divergence — population-scale partition divergence vs wow.wow_portfolios (the 479 / 157 result).
    gate       — the WoW gate: does WoW genuinely split a group's members, or over-lump them?
"""
