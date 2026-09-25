#!/usr/bin/env python3
from research.model import load_summary, validate_bundle
import json
s=load_summary()
print(json.dumps(s,indent=2,ensure_ascii=False))
print('bundle_validation:', 'PASS' if validate_bundle() else 'FAIL')
