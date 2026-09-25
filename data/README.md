# Data

## Primary sources
- O*NET 25.1 Technology Skills;
- O*NET 31.0 Software Skills;
- O*NET 25.1 Occupation Data;
- O*NET 31.0 Occupation Data.

The exact source URLs, release dates, row counts, and SHA-256 fingerprints are recorded in `source_manifest.json`.

## Licensing
O*NET database content is used under CC BY 4.0 with USDOL/ETA attribution. Raw source files are not redistributed here. See `../THIRD_PARTY_DATA.md`.

## Derived evidence
- `derived/primary_results.csv`: all 902 common occupations;
- `derived/secondary_results.csv`: ten lowest exact-name Jaccards;
- `derived/robustness_results.csv`: distribution and category-name sensitivity diagnostics.

## Measurement notes
Technology Skills was renamed Software Skills in O*NET 30.3. The exact-name comparison uses Example / Workplace Example. The sensitivity analysis uses normalized Commodity Title / Element Name.

Hot Technology and In Demand counts are deduplicated **pair counts**, not raw row counts.

## Construct boundary
Database portfolio turnover is an indicator of occupational software-skill renewal pressure. It is not a direct measure of individual worker skill depreciation, training quality, or causal learning outcomes.
