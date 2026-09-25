from __future__ import annotations
import csv, json, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def normalize_technology(s):return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def jaccard(a,b):return len(a&b)/len(a|b) if a|b else 0.0
def compare_pair_sets(old_pairs,new_pairs):
    inter=len(old_pairs&new_pairs); union=len(old_pairs|new_pairs); return {'persisted_pairs':inter,'global_jaccard':inter/union if union else 0.0}
def load_summary():return json.loads((ROOT/'results/empirical_summary.json').read_text())
def load_low_similarity_subset():
    with (ROOT/'data/derived/primary_results.csv').open() as f:return list(csv.DictReader(f))
def validate_bundle():
    s=load_summary()['headline_metrics']; rows=load_low_similarity_subset(); vals=[float(r['jaccard']) for r in rows]
    return s['common_occupation_codes']==902 and s['rows_2026']==31821 and len(rows)==10 and vals==sorted(vals)
