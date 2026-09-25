# Reproducibility

## Offline validation

```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
```

The offline suite verifies:
- exact release metrics;
- complete 902-code table size and uniqueness;
- all-release versus common-code scope;
- pair-count reconciliation;
- occupation-level distribution statistics;
- exact low-similarity tail extraction;
- title stability;
- category-name sensitivity;
- robustness-table/JSON agreement;
- pinned source row counts and SHA-256 fingerprints.

## Pinned source files

| Source | Rows | SHA-256 |
|---|---:|---|
| 25.1 Technology Skills | 29,012 | `19de2a84a52a77841f9879fd026ece1a0dc2bc5611ea306e015b74ef22d00ddc` |
| 31.0 Software Skills | 31,821 | `6aabb96b464288db849580e6510530efff3f80e25dde2bb23f1fc36bb526b016` |
| 25.1 Occupation Data | 1,016 | `63e6029d3d30ff5c7cf39b5304a733b77a409e01c65ae7095fe92f6d18d74a66` |
| 31.0 Occupation Data | 1,016 | `a09eae1d6609686e44e05b7290993a1c8b523d8ca224bc0eedc194c855c3ee02` |

## Verify current upstream bytes

```bash
python scripts/fetch_and_analyze.py
```

The command stops if an O*NET file no longer matches the released fingerprint or row count.

## Regenerate the release

```bash
python scripts/fetch_and_analyze.py --write
```

This regenerates:
- `data/derived/primary_results.csv`;
- `data/derived/secondary_results.csv`;
- `data/derived/robustness_results.csv`;
- `results/empirical_summary.json`;
- all four SVG research figures.

## GitHub Actions

`.github/workflows/ci.yml` runs the offline suite on Python 3.10, 3.11, and 3.12.

`.github/workflows/empirical-rebuild.yml` downloads the four pinned O*NET files, regenerates the complete release, runs tests, and requires **zero git diff**. It does not update source fingerprints automatically.

## Intentional source updates

The script contains a `--refresh-fingerprints` option only for an intentional new release. It should be used only after reviewing O*NET release/schema changes and versioning the resulting empirical release. Normal CI never uses it.
