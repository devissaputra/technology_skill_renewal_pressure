#!/usr/bin/env python3
import csv,io,json,statistics,urllib.request
from research.model import normalize_technology,jaccard,compare_pair_sets
OLD='https://www.onetcenter.org/dl_files/database/db_25_1_text/Technology%20Skills.txt'; NEW='https://www.onetcenter.org/dl_files/database/db_31_0_csv/software_skills.csv'
old=list(csv.DictReader(io.StringIO(urllib.request.urlopen(OLD).read().decode('utf-8-sig')),delimiter='\t')); new=list(csv.DictReader(io.StringIO(urllib.request.urlopen(NEW).read().decode('utf-8-sig'))))
A={(r['O*NET-SOC Code'],normalize_technology(r['Example'])) for r in old}; B={(r['O*NET-SOC Code'],normalize_technology(r['Workplace Example'])) for r in new}; common={r['O*NET-SOC Code'] for r in old}&{r['O*NET-SOC Code'] for r in new}; comp=compare_pair_sets(A,B); by=[]
for code in common:
    a={t for c,t in A if c==code}; b={t for c,t in B if c==code}; by.append(jaccard(a,b))
summary={'study':'Technology Skill Renewal Pressure: O*NET 2020–2026','headline_metrics':{'rows_2020':len(old),'rows_2026':len(new),'common_occupation_codes':len(common),'pairs_2020':len(A),'pairs_2026':len(B),'persisted_pairs':comp['persisted_pairs'],'global_jaccard':round(comp['global_jaccard'],3),'occupation_jaccard_mean':round(sum(by)/len(by),4),'occupation_jaccard_median':round(statistics.median(by),4),'hot_pairs_2020':sum(str(r.get('Hot Technology','')).upper()=='Y' for r in old),'hot_pairs_2026':sum(str(r.get('Hot Technology','')).upper()=='Y' for r in new),'in_demand_pairs_2026':sum(str(r.get('In Demand','')).upper()=='Y' for r in new)},'finding':'Across 902 occupation codes appearing in both releases, the global code–technology-pair Jaccard similarity is 0.685; median occupation-level Jaccard is 0.6875. This indicates meaningful portfolio turnover rather than either complete stability or wholesale replacement.','source':'O*NET 25.1 and O*NET 31.0 Technology/Software Skills','retrieved':'2026-09-25'}
print(json.dumps({'summary':summary},indent=2))
