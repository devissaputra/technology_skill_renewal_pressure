# Final QA Report

**Release status: PASS.**

## Source integrity
- O*NET 25.1 Technology Skills verified at 29,012 rows;
- O*NET 31.0 Software Skills verified at 31,821 rows;
- matching 25.1 and 31.0 Occupation Data verified at 1,016 rows each;
- all four source files pinned by exact SHA-256 in `data/source_manifest.json`;
- normal rebuilds reject changed source bytes or row counts;
- raw O*NET files are not redistributed.

## Longitudinal comparability
- O*NET's official schema history documents the Technology Skills → Software Skills rename in release 30.3;
- Example → Workplace Example and Commodity Title → Element Name field renames are documented;
- the 31.0 Software Skills file records 30.3 as its most recent content update;
- matching Occupation Data snapshots verify zero title changes among the 902 common skill-file occupation codes.

## Corrected scope definitions
The release now separates:
1. all-release occupation–software pair overlap;
2. pair overlap restricted to the 902 occupation codes represented in both skill files;
3. the complete occupation-level Jaccard distribution for those 902 codes.

The global all-release Jaccard is no longer incorrectly described as a statistic across the 902 common codes.

## Corrected release metrics
- unique pairs 2020: 28,929;
- unique pairs 2026: 31,706;
- all-release persisted pairs: 24,736;
- all-release global Jaccard: 0.6890;
- common-code pairs 2020: 28,929;
- common-code pairs 2026: 31,065;
- common-code persisted pairs: 24,736;
- common-code global Jaccard: 0.7016;
- occupation Jaccard mean: 0.6685;
- occupation Jaccard median: 0.6923.

These values replace the earlier stale 0.685 / 0.6875 release claims.

## Heterogeneity
The complete 902-occupation distribution is packaged and tested:
- standard deviation: 0.1665;
- Q10: 0.4286;
- Q25: 0.5769;
- Q75: 0.7826;
- Q90: 0.8517;
- 1.33% below 0.25;
- 13.97% below 0.50;
- 36.03% at or above 0.75.

The ten lowest-Jaccard occupations are retained only as a diagnostic subset.

## Sensitivity analysis
Raw Commodity Code and Element ID values were not assumed to be longitudinally identical. The released sensitivity analysis instead uses normalized semantic category names:
- 25.1 Commodity Title;
- 31.0 Element Name.

Results:
- common-code category-name Jaccard: 0.8169;
- median occupation category-name Jaccard: 0.8481.

The higher category-level persistence shows that part of exact software-name turnover occurs inside broader categories that remain more stable.

## Pair-versus-row correction
The analysis now distinguishes source rows from unique occupation–software pairs:
- 83 duplicate normalized pair rows in 2020;
- 115 duplicate normalized pair rows in 2026;
- Hot Technology unique pairs: 12,636 in 2020 and 11,456 in 2026;
- In Demand unique pairs: 2,404 in 2026.

The release no longer labels raw row counts as pair counts.

## Evidence completeness
- `primary_results.csv`: all 902 common occupations;
- `secondary_results.csv`: exact ten-row low-similarity tail;
- `robustness_results.csv`: distribution and sensitivity diagnostics;
- `empirical_summary.json`: synchronized machine-readable release;
- four regenerated SVG figures use corrected scope and metrics.

## Software and reproducibility QA
- study-specific analysis logic consolidated in `research/model.py`;
- tests expanded to cover normalization, pair comparison, quantiles, exact fingerprints, release metrics, complete-table size, low-tail extraction, pair reconciliation, distribution statistics, category sensitivity, robustness tables, and full bundle validation;
- CI passes on Python 3.10, 3.11, and 3.12;
- strict online empirical rebuild downloads pinned O*NET sources, regenerates all evidence, runs tests, and passes only with zero git diff;
- strict empirical rebuild completed successfully;
- latest professor-facing documentation commit completed CI successfully.

## Licensing
- repository code/documentation license restored to the complete MIT text;
- GitHub recognizes the repository license as MIT;
- `THIRD_PARTY_DATA.md` records O*NET / USDOL-ETA CC BY 4.0 attribution and modification notice;
- source data licensing is kept distinct from the repository's MIT code license.

## Interpretation boundary
This repository measures turnover in versioned O*NET software-skill portfolios. It does not estimate causal human skill depreciation, worker performance loss, training effectiveness, or individual proficiency. Renewal pressure is a descriptive workforce-planning signal that can reflect both substantive labor-market change and database/measurement maintenance.

## GitHub metadata
The recommended About text and final topics are recorded in `GITHUB_METADATA.md`. The current GitHub repository description and Topics remain UI metadata to be entered separately because repository-metadata mutation is not exposed by the connected GitHub interface used for this repair.
