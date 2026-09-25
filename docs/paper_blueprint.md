# Paper Blueprint

## Working title
Technology Skill Renewal Pressure: O*NET 2020–2026

## Motivation
Workforce-planning systems need to distinguish durable technology requirements from portfolios that are changing quickly. Versioned O*NET releases allow the same occupation codes to be compared over time without treating a proprietary job-posting sample as ground truth.

## Research question
How much do occupation–technology portfolios persist or turn over between O*NET 25.1 (2020) and O*NET 31.0 (2026)?

## Data and method
Normalize technology/software example strings, form unique occupation–technology pairs for each release, restrict occupation-level comparisons to codes appearing in both releases, and calculate global and occupation-level Jaccard similarity. Preserve the official Hot Technology and In Demand indicators as descriptive attributes rather than causal signals.

## Results to report
Across 902 occupation codes appearing in both releases, the global occupation–technology-pair Jaccard similarity is 0.685 and the median occupation-level Jaccard is 0.6875. The low-similarity tail demonstrates strong heterogeneity in portfolio renewal pressure. Report the packaged headline metrics and the full relevant derived table; do not cherry-pick only the strongest contrast.

## Robustness / sensitivity
The release reports both global pair-set Jaccard similarity and the distribution of occupation-level Jaccard values over the 902 common occupation codes. Exact duplicate occupation–technology pairs are collapsed after deterministic text normalization. Because O*NET changed file naming and taxonomy conventions over time, more aggressive alias matching would be a separate sensitivity analysis and could change the measured churn.

## Limitations
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.

## Publication integrity
Do not describe this repository as peer reviewed, preregistered, or externally validated unless those events actually occur. Distinguish analysis of public data from original data collection.
