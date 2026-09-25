# Empirical Study Protocol

## Study
Technology Skill Renewal Pressure: O*NET 2020–2026

## Research question
How much do occupation–software-skill portfolios persist or turn over between O*NET 25.1 and O*NET 31.0, and how heterogeneous is that renewal pressure across occupations?

## Design
Longitudinal secondary analysis of two versioned O*NET software-skill snapshots, supplemented with matching Occupation Data snapshots for code/title validation.

## Source comparability
O*NET documents that release 30.3 renamed **Technology Skills** to **Software Skills** and renamed the corresponding example/category fields. This supports a longitudinal interpretation of the files rather than treating them as unrelated tables.

O*NET 31.0 is the August 2026 database snapshot used here. Its Software Skills file lists release 30.3 as the most recent content update.

## Unit of analysis
The primary unit is a unique normalized **O*NET-SOC code × software example** pair. Exact duplicate pairs are collapsed.

Occupation-level analysis is restricted to the **902 codes present in both skill files**. The matching Occupation Data snapshots show **zero title changes among those 902 codes**.

## Hypotheses
1. H1: occupation software-skill portfolios exhibit substantial persistence but incomplete stability.
2. H2: renewal pressure is heterogeneous across occupations rather than captured adequately by one global churn value.

## Primary measures
- all-release pair-set Jaccard;
- common-code pair-set Jaccard;
- complete distribution of occupation-level Jaccard across 902 common occupations.

## Primary findings
- all-release global Jaccard: **0.6890**;
- common-code global Jaccard: **0.7016**;
- occupation-level mean: **0.6685**;
- occupation-level median: **0.6923**;
- Q10–Q90: **0.4286–0.8517**;
- 13.97% of occupations are below 0.50;
- 36.03% are at or above 0.75.

The all-release statistic is explicitly distinct from the common-code statistic. Only the occupation-level distribution is described as being across the 902 common codes.

## Sensitivity analysis
Software-name changes can exaggerate apparent turnover. A second analysis collapses software examples to normalized O*NET category names using **Commodity Title** in 25.1 and the documented renamed **Element Name** in 31.0.

- common-code category Jaccard: **0.8169**;
- median occupation category Jaccard: **0.8481**.

The higher category-level overlap indicates that some exact-name turnover occurs within broader categories that remain stable.

## Source attributes
Hot Technology values are summarized at the unique pair level after deduplication. In Demand is reported for 2026 only because O*NET added that field after release 25.1.

## Validity boundary
Database turnover combines labor-market change with taxonomy maintenance, data-collection updates, classification revisions, software/vendor naming changes, and other measurement effects. The study therefore operationalizes **renewal pressure**, not pure human skill depreciation or causal obsolescence.

## Reproducibility
Four source files are pinned by SHA-256 and row count. The complete 902-row evidence table, low-similarity diagnostic subset, robustness table, JSON summary, figures, tests, offline CI, and online source-to-output rebuild are synchronized.

The analysis plan documents the released analysis after dataset selection and must not be represented as preregistered.
