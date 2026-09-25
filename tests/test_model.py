import pytest

from research.model import (
    EXPECTED_COMMON_CODES,
    EXPECTED_HEADLINE,
    EXPECTED_SOURCE_ROWS,
    EXPECTED_SOURCE_SHA256,
    compare_pair_sets,
    jaccard,
    load_manifest,
    load_primary_results,
    load_robustness,
    load_secondary_results,
    load_summary,
    normalize_technology,
    occupation_distribution,
    quantile,
    validate_bundle,
)


def test_normalization():
    assert normalize_technology("Python 3 / NumPy") == "python 3 numpy"
    assert normalize_technology("Adobe® Acrobat-Pro") == "adobe acrobat pro"


def test_jaccard_and_pair_comparison():
    assert jaccard({"a", "b"}, {"b", "c"}) == pytest.approx(1 / 3)
    result = compare_pair_sets(
        {("1", "a"), ("1", "b")},
        {("1", "b"), ("1", "c")},
    )
    assert result["persisted_pairs"] == 1
    assert result["union_pairs"] == 3
    assert result["global_jaccard"] == pytest.approx(1 / 3)


def test_quantile_interpolation():
    values = [0, 1, 2, 3, 4]
    assert quantile(values, 0.25) == 1
    assert quantile(values, 0.50) == 2
    assert quantile(values, 0.90) == pytest.approx(3.6)


def test_source_manifest_is_exactly_pinned():
    manifest = load_manifest()
    for key, rows in EXPECTED_SOURCE_ROWS.items():
        assert manifest["source_files"][key]["rows"] == rows
        assert manifest["source_files"][key]["sha256"] == EXPECTED_SOURCE_SHA256[key]
    assert manifest["raw_data_redistributed"] is False


def test_headline_release_metrics():
    metrics = load_summary()["headline_metrics"]
    for key, expected in EXPECTED_HEADLINE.items():
        if isinstance(expected, float):
            assert metrics[key] == pytest.approx(expected, abs=5e-5)
        else:
            assert metrics[key] == expected


def test_complete_common_occupation_table():
    rows = load_primary_results()
    assert len(rows) == EXPECTED_COMMON_CODES
    assert len({r["occupation_code"] for r in rows}) == EXPECTED_COMMON_CODES
    assert sum(str(r["title_changed"]).lower() == "true" for r in rows) == 0
    assert all(0 <= float(r["jaccard"]) <= 1 for r in rows)
    assert all(0 <= float(r["category_jaccard"]) <= 1 for r in rows)


def test_low_similarity_subset_is_exact_tail():
    primary = load_primary_results()
    secondary = load_secondary_results()
    expected = sorted(
        primary,
        key=lambda r: (float(r["jaccard"]), r["occupation_code"]),
    )[:10]
    assert len(secondary) == 10
    assert [r["occupation_code"] for r in secondary] == [r["occupation_code"] for r in expected]


def test_common_pair_totals_reconcile():
    rows = load_primary_results()
    metrics = load_summary()["headline_metrics"]
    assert sum(int(r["pairs_2020"]) for r in rows) == metrics["common_pairs_2020"]
    assert sum(int(r["pairs_2026"]) for r in rows) == metrics["common_pairs_2026"]
    assert sum(int(r["persisted_pairs"]) for r in rows) == metrics["common_persisted_pairs"]
    union = sum(int(r["union_pairs"]) for r in rows)
    assert metrics["common_persisted_pairs"] / union == pytest.approx(
        metrics["common_code_global_jaccard"], abs=5e-5
    )


def test_distribution_reconciles_with_full_table():
    summary = load_summary()["occupation_jaccard_distribution"]
    calc = occupation_distribution()
    for key, value in calc.items():
        assert summary[key] == pytest.approx(value, abs=5e-5)


def test_category_sensitivity_is_nonzero_and_reconciled():
    summary = load_summary()
    sensitivity = summary["sensitivity_analysis"]
    rows = load_primary_results()
    category_union = sum(int(r["category_union"]) for r in rows)
    category_persisted = sum(int(r["persisted_categories"]) for r in rows)
    assert sensitivity["common_category_global_jaccard"] > 0
    assert category_persisted / category_union == pytest.approx(
        sensitivity["common_category_global_jaccard"], abs=5e-5
    )


def test_robustness_table_matches_summary():
    summary = load_summary()
    dist = summary["occupation_jaccard_distribution"]
    sensitivity = summary["sensitivity_analysis"]
    robust = load_robustness()
    mapping = {
        "occupation_jaccard_q10": dist["q10"],
        "occupation_jaccard_q25": dist["q25"],
        "occupation_jaccard_q75": dist["q75"],
        "occupation_jaccard_q90": dist["q90"],
        "occupation_jaccard_stddev": dist["stddev"],
        "share_occupations_jaccard_below_025": dist["share_below_025"],
        "share_occupations_jaccard_below_050": dist["share_below_050"],
        "share_occupations_jaccard_at_least_075": dist["share_at_least_075"],
        "common_category_global_jaccard": sensitivity["common_category_global_jaccard"],
        "occupation_category_jaccard_median": sensitivity["occupation_category_jaccard_median"],
    }
    for key, value in mapping.items():
        assert robust[key] == pytest.approx(value, abs=5e-5)


def test_bundle_validation():
    assert validate_bundle()
