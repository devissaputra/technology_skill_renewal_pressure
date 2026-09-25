# Technology Skill Renewal Pressure: O*NET 2020–2026

> **Empirical Research Bundle** · **Portfolio Track: Learning & Development Research** · Workforce Skills / Skill Renewal / Occupational Intelligence

Longitudinal empirical comparison of O*NET 25.1 and 31.0 technology/software-skill portfolios across 902 common occupation codes.

![Empirical workflow](assets/architecture.svg)

## Study status

**Completed secondary empirical analysis.** Reported findings were calculated from the named public source on 25 September 2026. The rebuild script contains **no synthetic fallback**. Raw source data are not republished unless source terms permit it; `data/source_manifest.json` records provenance, retrieval details, licensing notes, and the claim boundary.

## Research question

> How much do occupation–technology portfolios persist or turn over between O*NET 25.1 (2020) and O*NET 31.0 (2026)?

## Design

- **Design:** Longitudinal secondary analysis of two versioned O*NET database releases
- **Source:** O*NET 25.1 Technology Skills and O*NET 31.0 Software Skills
- **Source page:** https://www.onetcenter.org/db_releases.html
- **Direct data endpoint:** `https://www.onetcenter.org/dl_files/database/db_25_1_text/Technology%20Skills.txt ; https://www.onetcenter.org/dl_files/database/db_31_0_csv/software_skills.csv`
- **Retrieval / analysis date:** 2026-09-25
- **Licensing / reuse note:** O*NET database releases are available under CC BY 4.0 with required USDOL/ETA attribution.

## Hypotheses

1. H1: occupation-level technology portfolios exhibit substantial persistence but not complete stability.
2. H2: renewal pressure is heterogeneous across occupations rather than captured by a single portfolio-wide churn rate.

## Empirical method

Normalize technology/software example strings, form unique occupation–technology pairs for each release, restrict occupation-level comparisons to codes appearing in both releases, and calculate global and occupation-level Jaccard similarity. Preserve the official Hot Technology and In Demand indicators as descriptive attributes rather than causal signals.

![Method](assets/method.svg)

## Headline empirical finding

Across 902 occupation codes appearing in both releases, the global occupation–technology-pair Jaccard similarity is 0.685 and the median occupation-level Jaccard is 0.6875. The low-similarity tail demonstrates strong heterogeneity in portfolio renewal pressure.

### Headline metrics

- **rows 2020**: 29012
- **rows 2026**: 31821
- **common occupation codes**: 902
- **pairs 2020**: 28929
- **pairs 2026**: 31706
- **persisted pairs**: 24649
- **global jaccard**: 0.685
- **occupation jaccard mean**: 0.6641
- **occupation jaccard median**: 0.6875
- **hot pairs 2020**: 12664
- **hot pairs 2026**: 11204
- **in demand pairs 2026**: 2316

The packaged derived tables are documented in `docs/data_dictionary.md`. That document states explicitly whether each CSV is a complete analysis table or a diagnostic subset.

![Research evidence](assets/research_design.svg)

## What this study can and cannot claim

**Can claim:** the computations in this repository summarize the named public dataset under the documented operationalization.

**Cannot claim:** Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.

![Finding and boundary](assets/evaluation.svg)

## Reproduce

Offline verification of packaged empirical results:

```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
```

Recompute the empirical analysis from the public source (internet required):

```bash
python scripts/fetch_and_analyze.py
```

The online rebuild calls study-specific functions from `research/model.py`; the tests exercise those functions and scientific invariants rather than only checking file presence.

## Research bundle contents

- `README.md` — study overview and bounded findings
- `EMPIRICAL_STUDY.md` — protocol, validity, and interpretation
- `data/source_manifest.json` — provenance, license note, and claim boundary
- `data/derived/` — compact derived empirical tables
- `results/empirical_summary.json` — machine-readable headline results
- `scripts/fetch_and_analyze.py` — public-source rebuild
- `research/model.py` — reusable study-specific analysis functions
- `tests/` — behavioral and scientific-invariant tests
- `docs/` — analysis plan, data dictionary, paper blueprint, references, originality map
- `assets/` — four study-specific SVG figures

## Research integrity

This bundle distinguishes **source data**, **operationalization**, **result**, and **interpretation**. The analysis plan documents the released analysis; it is **not described as preregistered**. Public data do not automatically validate a construct, so proxy and external-validity limits are explicit.
