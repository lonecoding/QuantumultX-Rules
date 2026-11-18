#!/usr/bin/env python3
"""Convert personal root QuanX lists to Surge rules without changing routing data."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['Hijacking','Diagnostics','Telegram','OpenAI','Claude','YouTube','TikTok','Apple','Google','Global','China']
TYPES = {'HOST':'DOMAIN','HOST-SUFFIX':'DOMAIN-SUFFIX','HOST-KEYWORD':'DOMAIN-KEYWORD','HOST-WILDCARD':'DOMAIN-WILDCARD','USER-AGENT':'USER-AGENT'}

def render(source):
    result = []
    for number,line in enumerate(source.splitlines(),1):
        if not line.strip() or line.lstrip().startswith(('#',';','//')):
            continue
        parts = [x.strip() for x in line.split(',')]
        if len(parts) != 3 or parts[0].upper() not in TYPES or not parts[1]:
            raise ValueError(f'Unsupported source rule at line {number}')
        result.append(TYPES[parts[0].upper()]+','+parts[1])
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    expected={}; manifest={}
    for name in NAMES:
        data=(ROOT/(name+'.list')).read_bytes()
        rules=render(data.decode())
        header='# Generated from '+name+'.list by scripts/generate_surge.py.\n# Original rules: blackmatrix7; personal modifications: lonecoding.\n# Policies are assigned by the main Surge profile.\n'
        expected[ROOT/'surge/rules'/(name+'.list')]=header+'\n'.join(rules)+'\n'
        manifest[name]={'rules':len(rules),'source_sha256':hashlib.sha256(data).hexdigest()}
    expected[ROOT/'surge/manifest.json']=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
    changed=[]
    for path,content in expected.items():
        if path.exists() and path.read_text()==content:continue
        changed.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    if args.check and changed:
        raise SystemExit('Stale Surge files: '+', '.join(changed))
    print(f'Surge: {len(NAMES)} lists, {sum(v["rules"] for v in manifest.values())} rules; {len(changed)} files changed.')

if __name__=='__main__':main()
