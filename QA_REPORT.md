# Final QA Report

**Release status: PASS after correction.**

## Checks completed
- provenance and source identity reviewed;
- licensing/reuse note recorded;
- derived CSV structure checked against the stated sample and estimand;
- `results/empirical_summary.json` reconciled with packaged evidence;
- README/report language reconciled with the numerical results;
- study-specific methods moved into `research/model.py`;
- tests exercise scientific logic and invariants;
- internet rebuild script has no synthetic fallback;
- four SVG assets regenerated as study-specific figures and XML-validated;
- local Markdown links checked;
- citation metadata points to the final repository slug;
- no preregistration claim is made.

## Final empirical finding
Across 902 occupation codes appearing in both releases, the global occupation–technology-pair Jaccard similarity is 0.685 and the median occupation-level Jaccard is 0.6875. The low-similarity tail demonstrates strong heterogeneity in portfolio renewal pressure.

## Required interpretation boundary
Database change combines labor-market change, taxonomy maintenance, data-collection updates, software/vendor naming changes, and measurement revisions. Pair churn is therefore a renewal-pressure indicator, not a pure rate of human skill depreciation.
