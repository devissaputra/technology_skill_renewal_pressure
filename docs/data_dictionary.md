# Data Dictionary

## Provenance
See `data/source_manifest.json`. Raw source observations are not silently republished.

## `data/derived/primary_results.csv`
Diagnostic subset: the ten common occupation codes with the lowest observed Jaccard similarity. Portfolio-wide headline statistics use all 902 common codes.

## `data/derived/secondary_results.csv`
When present and non-empty, this contains a second derived table needed to reproduce a reported comparison. If empty, no second packaged table is required.

## `results/empirical_summary.json`
Machine-readable headline sample sizes, estimates, and the release finding. Values must agree with README text and the derived CSVs.

## Construct boundary
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.
