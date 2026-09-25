# Data Dictionary

## Provenance
See `data/source_manifest.json`. Four O*NET source files are pinned by exact row count and SHA-256. Raw source files are not redistributed.

## `data/derived/primary_results.csv`
**Complete 902-occupation longitudinal table.**

Columns:
- `occupation_code`: common O*NET-SOC code;
- `title_2020`, `title_2026`: titles from versioned Occupation Data;
- `title_changed`: normalized title mismatch flag;
- `pairs_2020`, `pairs_2026`: unique normalized software-example counts;
- `persisted_pairs`: exact normalized software examples in both snapshots;
- `added_pairs`, `removed_pairs`;
- `union_pairs`;
- `jaccard`: exact-name occupation-level Jaccard;
- `categories_2020`, `categories_2026`: unique normalized category-name counts;
- `persisted_categories`, `category_union`;
- `category_jaccard`: Commodity Title / Element Name sensitivity Jaccard;
- `hot_pairs_2020`, `hot_pairs_2026`: unique pairs classified Hot Technology;
- `in_demand_pairs_2026`: unique 2026 pairs classified In Demand.

## `data/derived/secondary_results.csv`
The **ten lowest exact-name occupation Jaccards** from the complete primary table. This is a diagnostic tail, not the basis for portfolio-wide mean or median estimates.

## `data/derived/robustness_results.csv`
Distribution and sensitivity diagnostics:
- occupation Jaccard Q10/Q25/Q75/Q90;
- population standard deviation;
- threshold shares;
- common-code category-name Jaccard;
- median occupation category-name Jaccard.

## `results/empirical_summary.json`
Machine-readable release metrics, distribution, sensitivity analysis, and scope-aware finding. Tests reconcile it with the complete derived evidence.

## Pair-versus-row distinction
The raw skill files contain repeated rows after normalization. The analysis collapses them to unique occupation–software pairs before Jaccard and Hot/In Demand pair counts are calculated.

## Construct boundary
The tables measure O*NET portfolio persistence and turnover under explicit normalization. They do not measure worker-level learning, causal obsolescence, proficiency, or performance.
