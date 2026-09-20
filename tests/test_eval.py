"""Unit tests for the evaluation scoring stats — pure, no DB."""
from bor.eval.score import cohens_kappa, corroboration_class, mcnemar, wilson


def test_wilson():
    assert wilson(0, 0) == (0.0, 0.0, 0.0)
    p, lo, hi = wilson(10, 10)
    assert p == 1.0 and lo < 1.0 and hi <= 1.0  # point 1.0; interval bounded in [lo,1]
    p, lo, hi = wilson(1, 2)
    assert abs(p - 0.5) < 1e-9 and lo < p < hi


def test_cohens_kappa():
    assert cohens_kappa([("SAME", "SAME"), ("DIFFERENT", "DIFFERENT")]) == 1.0   # perfect agreement
    assert cohens_kappa([("SAME", "SAME")]) is None                             # <2 items
    # partial agreement is strictly between 0 and 1
    k = cohens_kappa([("SAME", "SAME"), ("SAME", "DIFFERENT"), ("DIFFERENT", "DIFFERENT")])
    assert -1.0 <= k < 1.0


def test_mcnemar():
    assert mcnemar(0, 0) == 1.0
    assert mcnemar(10, 0) < 0.05                # a strong, one-sided discordance is significant
    assert mcnemar(5, 5) > 0.5                  # symmetric discordance -> not significant (~0.75)


def test_corroboration_class():
    assert corroboration_class("acris-deed", "SAME", ["T1"]) == "C2"        # deed + same-source only
    assert corroboration_class("acris-deed", "SAME", ["T1", "T3"]) == "C1"  # deed + cross-source
    assert corroboration_class("splink-fellegi-sunter", "SAME", ["T1"]) == "C1"
    assert corroboration_class("acris-deed", "DIFFERENT", ["T1"]) is None   # not a SAME
