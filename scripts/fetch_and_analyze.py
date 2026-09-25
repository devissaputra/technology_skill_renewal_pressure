#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import statistics
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.model import (
    compare_pair_sets,
    jaccard,
    normalize_category_id,
    normalize_technology,
    normalize_title,
    quantile,
)

MANIFEST_PATH = ROOT / "data/source_manifest.json"
PRIMARY_PATH = ROOT / "data/derived/primary_results.csv"
SECONDARY_PATH = ROOT / "data/derived/secondary_results.csv"
ROBUSTNESS_PATH = ROOT / "data/derived/robustness_results.csv"
SUMMARY_PATH = ROOT / "results/empirical_summary.json"

SOURCE_CONFIG = {
    "onet_25_1_technology_skills": {
        "url": "https://www.onetcenter.org/dl_files/database/db_25_1_text/Technology%20Skills.txt",
        "delimiter": "\t",
        "expected_rows": 29012,
        "release": "25.1",
        "release_date": "2020-11",
    },
    "onet_31_0_software_skills": {
        "url": "https://www.onetcenter.org/dl_files/database/db_31_0_csv/software_skills.csv",
        "delimiter": ",",
        "expected_rows": 31821,
        "release": "31.0",
        "release_date": "2026-08",
        "content_last_updated_release": "30.3",
    },
    "onet_25_1_occupation_data": {
        "url": "https://www.onetcenter.org/dl_files/database/db_25_1_text/Occupation%20Data.txt",
        "delimiter": "\t",
        "expected_rows": 1016,
        "release": "25.1",
        "release_date": "2020-11",
    },
    "onet_31_0_occupation_data": {
        "url": "https://www.onetcenter.org/dl_files/database/db_31_0_csv/occupation_data.csv",
        "delimiter": ",",
        "expected_rows": 1016,
        "release": "31.0",
        "release_date": "2026-08",
        "content_last_updated_release": "25.1",
    },
}


def download(url: str) -> bytes:
    last_error = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "technology-skill-renewal-pressure/2.0"},
            )
            with urllib.request.urlopen(req, timeout=90) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def parse_rows(payload: bytes, delimiter: str):
    text = payload.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text), delimiter=delimiter))


def fetch_sources(manifest, refresh_fingerprints=False):
    rows_by_key = {}
    files_meta = manifest.setdefault("source_files", {})

    for key, config in SOURCE_CONFIG.items():
        payload = download(config["url"])
        sha256 = hashlib.sha256(payload).hexdigest()
        rows = parse_rows(payload, config["delimiter"])
        if len(rows) != config["expected_rows"]:
            raise RuntimeError(
                f"{key}: expected {config['expected_rows']} rows, got {len(rows)}"
            )

        existing = files_meta.get(key, {})
        if not refresh_fingerprints:
            expected_hash = existing.get("sha256")
            expected_rows = existing.get("rows")
            if not expected_hash:
                raise RuntimeError(
                    f"{key}: no pinned SHA-256 in manifest. "
                    "Use --refresh-fingerprints only for an intentional new release."
                )
            if sha256 != expected_hash:
                raise RuntimeError(
                    f"{key}: source fingerprint changed; expected {expected_hash}, got {sha256}"
                )
            if int(expected_rows) != len(rows):
                raise RuntimeError(
                    f"{key}: manifest row count {expected_rows} differs from downloaded {len(rows)}"
                )

        files_meta[key] = {
            "url": config["url"],
            "release": config["release"],
            "release_date": config["release_date"],
            "rows": len(rows),
            "sha256": sha256,
            **(
                {"content_last_updated_release": config["content_last_updated_release"]}
                if "content_last_updated_release" in config
                else {}
            ),
        }
        rows_by_key[key] = rows

    return rows_by_key


def build_pair_maps(rows, *, old=False):
    tech_field = "Example" if old else "Workplace Example"
    category_field = "Commodity Title" if old else "Element Name"
    code_field = "O*NET-SOC Code"

    pairs_by_code = defaultdict(set)
    hot_by_code = defaultdict(set)
    demand_by_code = defaultdict(set)
    categories_by_code = defaultdict(set)

    for row in rows:
        code = row[code_field].strip()
        tech = normalize_technology(row[tech_field])
        if not tech:
            continue
        pair = (code, tech)
        pairs_by_code[code].add(tech)

        if str(row.get("Hot Technology", "")).strip().upper() == "Y":
            hot_by_code[code].add(tech)
        if not old and str(row.get("In Demand", "")).strip().upper() == "Y":
            demand_by_code[code].add(tech)

        category = normalize_technology(row.get(category_field, ""))
        if category:
            categories_by_code[code].add(category)

    all_pairs = {(code, tech) for code, values in pairs_by_code.items() for tech in values}
    all_hot_pairs = {(code, tech) for code, values in hot_by_code.items() for tech in values}
    all_demand_pairs = {(code, tech) for code, values in demand_by_code.items() for tech in values}
    all_categories = {(code, cat) for code, values in categories_by_code.items() for cat in values}

    return {
        "pairs_by_code": pairs_by_code,
        "hot_by_code": hot_by_code,
        "demand_by_code": demand_by_code,
        "categories_by_code": categories_by_code,
        "all_pairs": all_pairs,
        "all_hot_pairs": all_hot_pairs,
        "all_demand_pairs": all_demand_pairs,
        "all_categories": all_categories,
    }


def title_map(rows):
    return {r["O*NET-SOC Code"].strip(): r["Title"].strip() for r in rows}


def distribution(values):
    values = [float(v) for v in values]
    return {
        "mean": round(statistics.fmean(values), 4),
        "median": round(statistics.median(values), 4),
        "stddev": round(statistics.pstdev(values), 4),
        "min": round(min(values), 4),
        "q10": round(quantile(values, 0.10), 4),
        "q25": round(quantile(values, 0.25), 4),
        "q75": round(quantile(values, 0.75), 4),
        "q90": round(quantile(values, 0.90), 4),
        "max": round(max(values), 4),
        "share_below_025": round(sum(v < 0.25 for v in values) / len(values), 4),
        "share_below_050": round(sum(v < 0.50 for v in values) / len(values), 4),
        "share_at_least_075": round(sum(v >= 0.75 for v in values) / len(values), 4),
    }


def analyze(sources):
    old_rows = sources["onet_25_1_technology_skills"]
    new_rows = sources["onet_31_0_software_skills"]
    old_occ = sources["onet_25_1_occupation_data"]
    new_occ = sources["onet_31_0_occupation_data"]

    old = build_pair_maps(old_rows, old=True)
    new = build_pair_maps(new_rows, old=False)
    old_titles = title_map(old_occ)
    new_titles = title_map(new_occ)

    common_codes = sorted(set(old["pairs_by_code"]) & set(new["pairs_by_code"]))
    if len(common_codes) != 902:
        raise RuntimeError(f"Expected 902 common occupation codes, got {len(common_codes)}")

    all_pair_comp = compare_pair_sets(old["all_pairs"], new["all_pairs"])

    common_old_pairs = {
        (code, tech)
        for code in common_codes
        for tech in old["pairs_by_code"][code]
    }
    common_new_pairs = {
        (code, tech)
        for code in common_codes
        for tech in new["pairs_by_code"][code]
    }
    common_pair_comp = compare_pair_sets(common_old_pairs, common_new_pairs)

    common_old_categories = {
        (code, cat)
        for code in common_codes
        for cat in old["categories_by_code"][code]
    }
    common_new_categories = {
        (code, cat)
        for code in common_codes
        for cat in new["categories_by_code"][code]
    }
    common_category_comp = compare_pair_sets(common_old_categories, common_new_categories)

    occupation_rows = []
    for code in common_codes:
        a = old["pairs_by_code"][code]
        b = new["pairs_by_code"][code]
        inter = a & b
        union = a | b

        ca = old["categories_by_code"][code]
        cb = new["categories_by_code"][code]
        cinter = ca & cb
        cunion = ca | cb

        title_2020 = old_titles.get(code, "")
        title_2026 = new_titles.get(code, "")
        title_changed = normalize_title(title_2020) != normalize_title(title_2026)

        occupation_rows.append(
            {
                "occupation_code": code,
                "title_2020": title_2020,
                "title_2026": title_2026,
                "title_changed": title_changed,
                "pairs_2020": len(a),
                "pairs_2026": len(b),
                "persisted_pairs": len(inter),
                "added_pairs": len(b - a),
                "removed_pairs": len(a - b),
                "union_pairs": len(union),
                "jaccard": round(jaccard(a, b), 6),
                "categories_2020": len(ca),
                "categories_2026": len(cb),
                "persisted_categories": len(cinter),
                "category_union": len(cunion),
                "category_jaccard": round(jaccard(ca, cb), 6),
                "hot_pairs_2020": len(old["hot_by_code"][code]),
                "hot_pairs_2026": len(new["hot_by_code"][code]),
                "in_demand_pairs_2026": len(new["demand_by_code"][code]),
            }
        )

    occ_dist = distribution([r["jaccard"] for r in occupation_rows])
    cat_dist = distribution([r["category_jaccard"] for r in occupation_rows])

    title_changes = sum(r["title_changed"] for r in occupation_rows)

    summary = {
        "study": "Technology Skill Renewal Pressure: O*NET 2020–2026",
        "headline_metrics": {
            "rows_2020": len(old_rows),
            "rows_2026": len(new_rows),
            "common_occupation_codes": len(common_codes),
            "all_pairs_2020": len(old["all_pairs"]),
            "all_pairs_2026": len(new["all_pairs"]),
            "all_persisted_pairs": all_pair_comp["persisted_pairs"],
            "all_release_global_jaccard": round(all_pair_comp["global_jaccard"], 4),
            "common_pairs_2020": len(common_old_pairs),
            "common_pairs_2026": len(common_new_pairs),
            "common_persisted_pairs": common_pair_comp["persisted_pairs"],
            "common_code_global_jaccard": round(common_pair_comp["global_jaccard"], 4),
            "occupation_jaccard_mean": occ_dist["mean"],
            "occupation_jaccard_median": occ_dist["median"],
            "hot_unique_pairs_2020": len(old["all_hot_pairs"]),
            "hot_unique_pairs_2026": len(new["all_hot_pairs"]),
            "in_demand_unique_pairs_2026": len(new["all_demand_pairs"]),
            "duplicate_pair_rows_2020": len(old_rows) - len(old["all_pairs"]),
            "duplicate_pair_rows_2026": len(new_rows) - len(new["all_pairs"]),
            "title_changed_common_codes": title_changes,
        },
        "occupation_jaccard_distribution": occ_dist,
        "sensitivity_analysis": {
            "measure": "Normalized O*NET category-name overlap: Commodity Title (25.1) versus Element Name (31.0) within the same 902 occupations",
            "common_category_pairs_2020": len(common_old_categories),
            "common_category_pairs_2026": len(common_new_categories),
            "common_category_persisted": common_category_comp["persisted_pairs"],
            "common_category_global_jaccard": round(common_category_comp["global_jaccard"], 4),
            "occupation_category_jaccard_mean": cat_dist["mean"],
            "occupation_category_jaccard_median": cat_dist["median"],
        },
        "finding": (
            "The release reports two distinct pair-set comparisons: an all-release Jaccard across "
            "every occupation-software pair present in each snapshot, and a common-code Jaccard "
            "restricted to the 902 occupations represented in both files. Occupation-level "
            "heterogeneity is evaluated only within those 902 common codes. A category-level "
            "sensitivity analysis tests whether the renewal signal persists when software names "
            "are collapsed to normalized O*NET category names."
        ),
        "source": "O*NET Database 25.1 and 31.0, Technology Skills / Software Skills",
        "retrieved": "2026-09-25",
    }

    low_rows = sorted(
        occupation_rows,
        key=lambda r: (r["jaccard"], r["occupation_code"]),
    )[:10]

    robustness = {
        "occupation_jaccard_q10": occ_dist["q10"],
        "occupation_jaccard_q25": occ_dist["q25"],
        "occupation_jaccard_q75": occ_dist["q75"],
        "occupation_jaccard_q90": occ_dist["q90"],
        "occupation_jaccard_stddev": occ_dist["stddev"],
        "share_occupations_jaccard_below_025": occ_dist["share_below_025"],
        "share_occupations_jaccard_below_050": occ_dist["share_below_050"],
        "share_occupations_jaccard_at_least_075": occ_dist["share_at_least_075"],
        "common_category_global_jaccard": summary["sensitivity_analysis"]["common_category_global_jaccard"],
        "occupation_category_jaccard_median": summary["sensitivity_analysis"]["occupation_category_jaccard_median"],
    }

    return occupation_rows, low_rows, robustness, summary


def svg_escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write_figures(summary):
    metrics = summary["headline_metrics"]
    dist = summary["occupation_jaccard_distribution"]
    sens = summary["sensitivity_analysis"]
    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    architecture = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430">
<rect width="1200" height="430" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Technology Skill Renewal Pressure</text>
<text x="50" y="88" font-family="Arial" font-size="16">Versioned O*NET research pipeline with source fingerprinting</text>
<g font-family="Arial" text-anchor="middle">
<rect x="40" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="135" y="185" font-size="16" font-weight="700">Pinned sources</text><text x="135" y="215" font-size="14">25.1 + 31.0</text>
<rect x="280" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="375" y="185" font-size="16" font-weight="700">Normalize</text><text x="375" y="215" font-size="14">names + IDs</text>
<rect x="520" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="615" y="185" font-size="16" font-weight="700">Compare</text><text x="615" y="215" font-size="14">all + common codes</text>
<rect x="760" y="145" width="190" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="855" y="185" font-size="16" font-weight="700">Sensitivity</text><text x="855" y="215" font-size="14">category Jaccard</text>
<rect x="1000" y="145" width="160" height="135" rx="15" fill="#f5f5f5" stroke="#222"/><text x="1080" y="185" font-size="16" font-weight="700">Interpret</text><text x="1080" y="215" font-size="14">bounded L&amp;D claim</text>
</g>
<g stroke="#222" stroke-width="2.5"><line x1="230" y1="212" x2="280" y2="212"/><line x1="470" y1="212" x2="520" y2="212"/><line x1="710" y1="212" x2="760" y2="212"/><line x1="950" y1="212" x2="1000" y2="212"/></g>
</svg>'''

    method = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="550" viewBox="0 0 1200 550">
<rect width="1200" height="550" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Technology Skill Renewal Pressure — Method</text>
<g font-family="Arial">
<text x="70" y="125" font-size="20" font-weight="700">1. All-release pair comparison</text>
<text x="90" y="155" font-size="16">All unique occupation–software pairs in each snapshot; not restricted to common occupation codes.</text>
<text x="70" y="215" font-size="20" font-weight="700">2. Common-code longitudinal comparison</text>
<text x="90" y="245" font-size="16">{metrics["common_occupation_codes"]} occupations present in both skill files; full occupation-level distributions are reported.</text>
<text x="70" y="305" font-size="20" font-weight="700">3. Category sensitivity</text>
<text x="90" y="335" font-size="16">Repeat overlap analysis on normalized O*NET Commodity Title / Element Name categories to reduce vendor-name sensitivity.</text>
<text x="70" y="395" font-size="20" font-weight="700">4. Interpretation</text>
<text x="90" y="425" font-size="16">Treat observed change as database-based renewal pressure, not a causal rate of human skill depreciation.</text>
<text x="90" y="465" font-size="14">O*NET renamed Technology Skills to Software Skills in release 30.3; the longitudinal relation is documented by O*NET.</text>
</g>
</svg>'''

    evaluation = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="570" viewBox="0 0 1200 570">
<rect width="1200" height="570" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Technology Skill Renewal Pressure — Evidence Boundary</text>
<g font-family="Arial">
<rect x="55" y="95" width="1090" height="215" rx="18" fill="#f6f6f6" stroke="#333"/>
<text x="85" y="135" font-size="20" font-weight="700">Empirical evidence</text>
<text x="85" y="170" font-size="16">All-release pair Jaccard: {metrics["all_release_global_jaccard"]:.4f}.</text>
<text x="85" y="198" font-size="16">Common-code pair Jaccard across {metrics["common_occupation_codes"]} occupations: {metrics["common_code_global_jaccard"]:.4f}.</text>
<text x="85" y="226" font-size="16">Median occupation Jaccard: {metrics["occupation_jaccard_median"]:.4f}; Q10–Q90: {dist["q10"]:.4f}–{dist["q90"]:.4f}.</text>
<text x="85" y="254" font-size="16">Category-level common-code Jaccard sensitivity: {sens["common_category_global_jaccard"]:.4f}.</text>
<rect x="55" y="345" width="1090" height="150" rx="18" fill="#f6f6f6" stroke="#333"/>
<text x="85" y="385" font-size="20" font-weight="700">Claim boundary</text>
<text x="85" y="420" font-size="16">Observed turnover mixes real labor-market change with taxonomy maintenance, source updates, and naming changes.</text>
<text x="85" y="450" font-size="16">It is a renewal-pressure indicator for workforce planning, not a pure measure of human skill depreciation.</text>
</g>
</svg>'''

    values = [dist["q10"], dist["q25"], dist["median"], dist["q75"], dist["q90"]]
    labels = ["Q10", "Q25", "Median", "Q75", "Q90"]
    bars = []
    for i, (label, value) in enumerate(zip(labels, values)):
        x = 105 + i * 205
        h = value * 250
        y = 380 - h
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="105" height="{h:.1f}" fill="#d9d9d9" stroke="#333"/>')
        bars.append(f'<text x="{x+52.5}" y="410" text-anchor="middle" font-family="Arial" font-size="15">{label}</text>')
        bars.append(f'<text x="{x+52.5}" y="{y-10:.1f}" text-anchor="middle" font-family="Arial" font-size="14">{value:.3f}</text>')

    research_design = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500">
<rect width="1200" height="500" fill="white"/>
<text x="50" y="55" font-family="Arial" font-size="29" font-weight="700">Occupation-Level Jaccard Distribution</text>
<text x="50" y="85" font-family="Arial" font-size="16">Complete distribution across {metrics["common_occupation_codes"]} common O*NET-SOC codes</text>
<line x1="70" y1="380" x2="1130" y2="380" stroke="#222"/>
{''.join(bars)}
</svg>'''

    (assets / "architecture.svg").write_text(architecture)
    (assets / "method.svg").write_text(method)
    (assets / "evaluation.svg").write_text(evaluation)
    (assets / "research_design.svg").write_text(research_design)


def write_outputs(occupation_rows, low_rows, robustness, summary, manifest):
    PRIMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "occupation_code", "title_2020", "title_2026", "title_changed",
        "pairs_2020", "pairs_2026", "persisted_pairs", "added_pairs",
        "removed_pairs", "union_pairs", "jaccard", "categories_2020",
        "categories_2026", "persisted_categories", "category_union",
        "category_jaccard", "hot_pairs_2020", "hot_pairs_2026",
        "in_demand_pairs_2026",
    ]
    for path, rows in ((PRIMARY_PATH, occupation_rows), (SECONDARY_PATH, low_rows)):
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    with ROBUSTNESS_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in robustness.items():
            writer.writerow({"metric": key, "value": value})

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    write_figures(summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--refresh-fingerprints",
        action="store_true",
        help="Intentionally accept current upstream bytes and update pinned SHA-256 values.",
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text())
    sources = fetch_sources(manifest, refresh_fingerprints=args.refresh_fingerprints)
    occupation_rows, low_rows, robustness, summary = analyze(sources)

    if args.write:
        write_outputs(occupation_rows, low_rows, robustness, summary, manifest)

    print(
        json.dumps(
            {
                "source_files": manifest["source_files"],
                "summary": summary,
                "primary_rows": len(occupation_rows),
                "secondary_rows": len(low_rows),
                "robustness": robustness,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
