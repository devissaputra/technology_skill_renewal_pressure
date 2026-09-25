# Empirical Study Protocol

## Study
Technology Skill Renewal Pressure: O*NET 2020–2026

## Research question
How much do occupation–technology portfolios persist or turn over between O*NET 25.1 (2020) and O*NET 31.0 (2026)?

## Design and source
Longitudinal secondary analysis of two versioned O*NET database releases. Source: O*NET 25.1 Technology Skills and O*NET 31.0 Software Skills. Analysis/retrieval date: 2026-09-25.

## Hypotheses
1. H1: occupation-level technology portfolios exhibit substantial persistence but not complete stability.
2. H2: renewal pressure is heterogeneous across occupations rather than captured by a single portfolio-wide churn rate.

## Operationalization and method
Normalize technology/software example strings, form unique occupation–technology pairs for each release, restrict occupation-level comparisons to codes appearing in both releases, and calculate global and occupation-level Jaccard similarity. Preserve the official Hot Technology and In Demand indicators as descriptive attributes rather than causal signals.

## Primary empirical result
Across 902 occupation codes appearing in both releases, the global occupation–technology-pair Jaccard similarity is 0.685 and the median occupation-level Jaccard is 0.6875. The low-similarity tail demonstrates strong heterogeneity in portfolio renewal pressure.

## Validity and claim boundary
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.

## Reproducibility status
The repository packages derived results, study-specific analysis functions, deterministic or seeded procedures where relevant, an internet-enabled source rebuild script, and tests for both computations and critical scientific invariants. The released analysis was documented after dataset selection and should not be represented as preregistered.
