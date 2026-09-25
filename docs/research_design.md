# Research Design

## Research question
How much do occupation–technology portfolios persist or turn over between O*NET 25.1 (2020) and O*NET 31.0 (2026)?

## Design
Longitudinal secondary analysis of two versioned O*NET database releases.

## Source and unit of analysis
Source: O*NET 25.1 Technology Skills and O*NET 31.0 Software Skills. The operational unit follows the public dataset and is documented in `data/source_manifest.json` and `docs/data_dictionary.md`.

## Hypotheses
1. H1: occupation-level technology portfolios exhibit substantial persistence but not complete stability.
2. H2: renewal pressure is heterogeneous across occupations rather than captured by a single portfolio-wide churn rate.

## Method
Normalize technology/software example strings, form unique occupation–technology pairs for each release, restrict occupation-level comparisons to codes appearing in both releases, and calculate global and occupation-level Jaccard similarity. Preserve the official Hot Technology and In Demand indicators as descriptive attributes rather than causal signals.

## Validity boundary
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.
