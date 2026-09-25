# Analysis Plan

## Status
This document describes the released analysis. It is **not a preregistration**.

## Descriptive target
How much do occupation–software-skill portfolios persist or turn over between O*NET 25.1 and O*NET 31.0, and how heterogeneous is that renewal pressure across occupations?

## Comparability rule
O*NET documents the Technology Skills → Software Skills rename and associated field renames in release 30.3. Occupation codes are matched directly. Matching 25.1 and 31.0 Occupation Data files are used to verify titles for the common codes.

## Primary operationalization
Normalize software example strings by lowercasing and replacing non-alphanumeric sequences with spaces. Collapse duplicate O*NET-SOC code × normalized software pairs.

### Scope A: all-release pair comparison
Compare every unique code–software pair in each skill file.

### Scope B: common-code longitudinal comparison
Restrict both releases to the 902 occupation codes represented in both skill files. Compute:
- pair-set Jaccard;
- occupation-level Jaccard for every common code;
- complete distribution summaries.

The two scopes are reported separately.

## Hypotheses
1. H1: common-code software portfolios show substantial persistence but incomplete stability.
2. H2: occupation-level renewal pressure is heterogeneous.

These are assessed descriptively, not with a claim of statistical significance.

## Heterogeneity outputs
- mean and median;
- population standard deviation;
- minimum and maximum;
- Q10, Q25, Q75, Q90;
- share below Jaccard 0.25;
- share below Jaccard 0.50;
- share at or above Jaccard 0.75.

## Sensitivity analysis
Exact software names may change while broader functional categories remain stable. Repeat the common-code overlap analysis using normalized **Commodity Title (25.1)** and **Element Name (31.0)**, fields whose rename relationship is documented by O*NET.

Raw Commodity Code and Element ID identifiers are not treated as longitudinally identical identifiers.

## Source attributes
Hot Technology is aggregated to unique code–software pairs using an “any Y” rule. In Demand is summarized only for 2026 because the field did not exist in release 25.1.

## Missingness and exclusions
No software pair is imputed. Occupations absent from either skill file are excluded only from occupation-level longitudinal comparison, while remaining part of the all-release pair comparison when present.

## Interpretation boundary
Observed turnover can reflect real demand change, database maintenance, naming changes, taxonomy/classification updates, and data-collection revisions. It is a renewal-pressure indicator for workforce planning, not a causal rate of worker skill loss.
