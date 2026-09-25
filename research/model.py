from __future__ import annotations

import csv
import json
import math
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COMMON_CODES = 902
EXPECTED_SOURCE_ROWS = {
    "onet_25_1_technology_skills": 29012,
    "onet_31_0_software_skills": 31821,
    "onet_25_1_occupation_data": 1016,
    "onet_31_0_occupation_data": 1016,
}


def normalize_technology(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower())


def normalize_category_id(value: str) -> str:
    value = str(value).strip()
    if value.endswith(".0") and value[:-2].isdigit():
        return value[:-2]
    return value


def jaccard(a, b) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def compare_pair_sets(old_pairs, new_pairs):
    intersection = len(old_pairs & new_pairs)
    union = len(old_pairs | new_pairs)
    return {
        "persisted_pairs": intersection,
        "union_pairs": union,
        "global_jaccard": intersection / union if union else 0.0,
    }


def quantile(values, p: float) -> float:
    ordered = sorted(float(v) for v in values)
    if not ordered:
        raise ValueError("quantile requires at least one value")
    pos = (len(ordered) - 1) * p
    low = math.floor(pos)
    high = math.ceil(pos)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (pos - low)


def load_summary():
    return json.loads((ROOT / "results/empirical_summary.json").read_text())


def load_manifest():
    return json.loads((ROOT / "data/source_manifest.json").read_text())


def load_primary_results():
    with (ROOT / "data/derived/primary_results.csv").open(newline="") as f:
        return list(csv.DictReader(f))


def load_secondary_results():
    with (ROOT / "data/derived/secondary_results.csv").open(newline="") as f:
        return list(csv.DictReader(f))


def load_robustness():
    with (ROOT / "data/derived/robustness_results.csv").open(newline="") as f:
        return {row["metric"]: float(row["value"]) for row in csv.DictReader(f)}


def occupation_distribution(rows=None):
    rows = rows or load_primary_results()
    values = [float(row["jaccard"]) for row in rows]
    return {
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "stddev": statistics.pstdev(values),
        "min": min(values),
        "q10": quantile(values, 0.10),
        "q25": quantile(values, 0.25),
        "q75": quantile(values, 0.75),
        "q90": quantile(values, 0.90),
        "max": max(values),
        "share_below_025": sum(v < 0.25 for v in values) / len(values),
        "share_below_050": sum(v < 0.50 for v in values) / len(values),
        "share_at_least_075": sum(v >= 0.75 for v in values) / len(values),
    }


def validate_bundle():
    manifest = load_manifest()
    summary = load_summary()
    metrics = summary["headline_metrics"]
    sensitivity = summary["sensitivity_analysis"]
    distribution = summary["occupation_jaccard_distribution"]
    primary = load_primary_results()
    secondary = load_secondary_results()
    robustness = load_robustness()

    if len(primary) != EXPECTED_COMMON_CODES or len(secondary) != 10:
        return False
    if int(metrics["common_occupation_codes"]) != EXPECTED_COMMON_CODES:
        return False

    source_files = manifest.get("source_files", {})
    for key, expected_rows in EXPECTED_SOURCE_ROWS.items():
        item = source_files.get(key, {})
        if int(item.get("rows", -1)) != expected_rows:
            return False
        if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", ""))):
            return False

    if manifest.get("raw_data_redistributed") is not False:
        return False

    jaccards = [float(r["jaccard"]) for r in primary]
    if not all(0.0 <= x <= 1.0 for x in jaccards):
        return False
    if [float(r["jaccard"]) for r in secondary] != sorted(float(r["jaccard"]) for r in secondary):
        return False

    calc = occupation_distribution(primary)
    for key in ("mean", "median", "stddev", "min", "q10", "q25", "q75", "q90", "max",
                "share_below_025", "share_below_050", "share_at_least_075"):
        if abs(calc[key] - float(distribution[key])) > 5e-5:
            return False

    common_old = sum(int(r["pairs_2020"]) for r in primary)
    common_new = sum(int(r["pairs_2026"]) for r in primary)
    common_persisted = sum(int(r["persisted_pairs"]) for r in primary)
    common_union = sum(int(r["union_pairs"]) for r in primary)

    if common_old != int(metrics["common_pairs_2020"]):
        return False
    if common_new != int(metrics["common_pairs_2026"]):
        return False
    if common_persisted != int(metrics["common_persisted_pairs"]):
        return False
    if abs(common_persisted / common_union - float(metrics["common_code_global_jaccard"])) > 5e-5:
        return False

    if not (0.0 < float(metrics["all_release_global_jaccard"]) < 1.0):
        return False
    if not (0.0 < float(metrics["common_code_global_jaccard"]) < 1.0):
        return False

    title_changes = sum(str(r["title_changed"]).lower() == "true" for r in primary)
    if title_changes != int(metrics["title_changed_common_codes"]):
        return False

    category_vals = [float(r["category_jaccard"]) for r in primary]
    if abs(statistics.median(category_vals) - float(sensitivity["occupation_category_jaccard_median"])) > 5e-5:
        return False

    required_robustness = {
        "occupation_jaccard_q10": distribution["q10"],
        "occupation_jaccard_q25": distribution["q25"],
        "occupation_jaccard_q75": distribution["q75"],
        "occupation_jaccard_q90": distribution["q90"],
        "occupation_jaccard_stddev": distribution["stddev"],
        "share_occupations_jaccard_below_025": distribution["share_below_025"],
        "share_occupations_jaccard_below_050": distribution["share_below_050"],
        "share_occupations_jaccard_at_least_075": distribution["share_at_least_075"],
        "common_category_global_jaccard": sensitivity["common_category_global_jaccard"],
        "occupation_category_jaccard_median": sensitivity["occupation_category_jaccard_median"],
    }
    for key, value in required_robustness.items():
        if key not in robustness or abs(robustness[key] - float(value)) > 5e-5:
            return False

    return True
