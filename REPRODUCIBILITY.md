# Reproducibility

## Offline
```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
```

Offline tests operate on packaged derived evidence and study-specific pure functions.

## Full source rebuild
```bash
python scripts/fetch_and_analyze.py
```

The rebuild requires internet access and retrieves the source recorded in `data/source_manifest.json`. It intentionally does not substitute generated observations if retrieval fails.

## Reproducibility boundary
External sources can change or move. The manifest records the source identity, DOI/version where available, retrieval date, and reuse note. Derived results in this release correspond to the source state retrieved on 2026-09-25.
