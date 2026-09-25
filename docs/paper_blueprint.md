# Paper Blueprint

## Working title
Technology Skill Renewal Pressure: Longitudinal Evidence from O*NET Software-Skill Portfolios, 2020–2026

## Motivation
L&D and workforce-planning systems need to distinguish durable technology requirements from occupation portfolios that change rapidly. Versioned O*NET releases offer a reproducible public source for studying this turnover without treating a proprietary job-posting sample as ground truth.

## Research question
How much do occupation–software-skill portfolios persist or turn over between O*NET 25.1 and O*NET 31.0, and how heterogeneous is that renewal pressure across occupations?

## Data
- O*NET 25.1 Technology Skills, November 2020;
- O*NET 31.0 Software Skills snapshot, August 2026;
- matching 25.1 and 31.0 Occupation Data.

O*NET records release 30.3 as the most recent Software Skills content update and documents the Technology Skills → Software Skills rename.

## Methods
1. normalize exact software example strings;
2. deduplicate code–software pairs;
3. distinguish all-release from 902-common-code Jaccard;
4. report the complete occupation-level Jaccard distribution;
5. validate common-code title stability;
6. repeat overlap analysis on normalized Commodity Title / Element Name categories.

## Main results
- all-release pair Jaccard: **0.6890**;
- common-code pair Jaccard: **0.7016**;
- occupation median: **0.6923**;
- Q10–Q90: **0.4286–0.8517**;
- 13.97% of common occupations below 0.50;
- 36.03% at or above 0.75;
- category-name common-code Jaccard: **0.8169**;
- median occupation category Jaccard: **0.8481**;
- zero title changes among the 902 common codes.

## Interpretation
The gap between exact-name and category-level persistence is substantively important: part of apparent software renewal is within broader categories that remain stable. That supports a layered workforce-planning interpretation rather than a simple “skills became obsolete” narrative.

## Robustness and limitations
Report all 902 occupations, not only the low-similarity tail. Preserve the distinction between database turnover and human skill depreciation. Discuss vendor naming, source maintenance, content-update timing, taxonomy/classification maintenance, and the absence of worker-level outcome data.

## Publication integrity
Do not claim preregistration, peer review, causal identification, or external validation unless those events occur.
