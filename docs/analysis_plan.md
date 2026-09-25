# Analysis Plan

## Status
This file documents the analysis released in this repository. It is **not a preregistration** and should not be described as one.

## Primary estimand / descriptive target
How much do occupation–technology portfolios persist or turn over between O*NET 25.1 (2020) and O*NET 31.0 (2026)?

## Analysis
Normalize technology/software example strings, form unique occupation–technology pairs for each release, restrict occupation-level comparisons to codes appearing in both releases, and calculate global and occupation-level Jaccard similarity. Preserve the official Hot Technology and In Demand indicators as descriptive attributes rather than causal signals.

## Specified outputs for this release
1. source/sample size and provenance;
2. primary derived metric(s);
3. comparator, cross-group, cross-time, or frontier contrast where applicable;
4. uncertainty, sensitivity, or error information supported by the source;
5. explicit construct and external-validity limitations.

## Missingness / exclusions

Exact duplicate occupation-technology pairs are collapsed after text normalization. Occupation-level comparisons are restricted to the 902 occupation codes present in both releases. Technologies absent from a release are treated as absent observations, not imputed skills.

## Interpretation boundary
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.
