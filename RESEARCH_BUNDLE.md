# Research Bundle Definition

This repository is treated as a research bundle because it links one explicit research question to a named empirical source, a documented operationalization, executable analysis code, derived evidence, reproducibility checks, visual evidence, validity boundaries, and a paper-ready interpretation path.

## Question
How much do occupation–technology portfolios persist or turn over between O*NET 25.1 (2020) and O*NET 31.0 (2026)?

## Empirical core
Versioned occupation–technology set comparison using Jaccard similarity.

## Main result
Across 902 occupation codes appearing in both releases, the global occupation–technology-pair Jaccard similarity is 0.685 and the median occupation-level Jaccard is 0.6875. The low-similarity tail demonstrates strong heterogeneity in portfolio renewal pressure.

## Boundary
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.

## Release criterion
A release passes only if source provenance, code, derived tables, JSON summary, README claims, figures, and tests agree numerically and semantically.
