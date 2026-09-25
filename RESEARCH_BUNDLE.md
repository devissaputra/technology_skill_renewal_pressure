# Research Bundle Definition

This repository qualifies as an empirical research bundle because one explicit L&D/workforce research question is connected to versioned official sources, byte-level provenance, a complete analysis population, sensitivity analysis, executable regeneration, tests, CI, visual evidence, and bounded interpretation.

## Empirical core
- 29,012 O*NET 25.1 Technology Skills rows;
- 31,821 O*NET 31.0 Software Skills rows;
- 902 occupation codes represented in both skill files;
- complete 902-row occupation comparison;
- exact-name and category-name overlap analyses.

## Main release metrics
- all-release pair Jaccard: **0.6890**;
- common-code pair Jaccard: **0.7016**;
- occupation median Jaccard: **0.6923**;
- category-name common-code Jaccard: **0.8169**;
- median occupation category Jaccard: **0.8481**.

## Research contribution
The bundle separates three questions that would otherwise be conflated:
1. total database pair turnover;
2. within-common-occupation software-name turnover;
3. broader category turnover.

That layered design makes the L&D interpretation more defensible.

## Source integrity
Four O*NET source files are pinned by row count and SHA-256. Normal empirical rebuilding rejects changed source bytes. Raw source files are not redistributed.

## Release criterion
PASS requires:
- exact source fingerprints;
- complete 902-row evidence;
- correct all-release/common-code scope labels;
- distributional heterogeneity diagnostics;
- category-name sensitivity;
- title stability check;
- summary/CSV reconciliation;
- offline CI;
- zero-diff online source rebuild;
- explicit O*NET licensing and claim boundaries.
