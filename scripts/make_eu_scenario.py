#!/usr/bin/env python3
"""Build a hypothetical 'Rahmenverträge' scenario (data/rahmen.json).

Per-canton pro-EU share = national target (logit scale) + the canton's average
logit deviation from the national result over past Swiss-EU votes (Swissvotes
dataset). Turnout = per-canton mean turnout of those votes (excl. EWR 1992).
"""
import csv, json, math, os, urllib.request
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, '..')
SV = os.path.join(root, 'tmp', 'sv.csv')
if not os.path.exists(SV):
    os.makedirs(os.path.dirname(SV), exist_ok=True)
    urllib.request.urlretrieve('https://swissvotes.ch/page/dataset/swissvotes_dataset.csv', SV)
ABBR = "ZH BE LU UR SZ OW NW GL ZG FR SO BS BL SH AR AI SG GR AG TG TI VD VS NE GE JU".split()
# (anr, label, yes == pro-EU?)
VOTES = [(388,'EWR 1992',True),(464,'Bilaterale I 2000',True),(517,'Schengen/Dublin 2005',True),
         (519,'Personenfreizügigkeit Ost 2005',True),(540,'Personenfreizügigkeit 2009',True),
         (580,'Masseneinwanderungsinitiative 2014',False),(631,'Begrenzungsinitiative 2020',False)]
TARGET = 55.0  # national pro-EU share of valid votes in the hypothetical vote (%)
rows = {int(r['anr']): r for r in csv.DictReader(open(SV, encoding='utf-8-sig'), delimiter=';') if (r['anr'] or '').isdigit()}
lg = lambda p: math.log(p/(1-p)); inv = lambda x: 1/(1+math.exp(-x))
cantons = json.load(open(os.path.join(root, 'data', 'cantons.json')))

dev = [[] for _ in ABBR]; turn = [[] for _ in ABBR]
for anr, label, proeu in VOTES:
    r = rows[anr]; nat = float(r['volkja-proz'])/100
    if not proeu: nat = 1-nat
    for i, a in enumerate(ABBR):
        p = float(r[f'{a.lower()}-japroz'])/100
        if not proeu: p = 1-p
        dev[i].append(lg(p)-lg(nat))
        if anr != 388: turn[i].append(float(r[f'{a.lower()}-bet']))
off = [sum(d)/len(d) for d in dev]
tmean = [sum(t)/len(t) for t in turn]
w = [c['voters']*t for c, t in zip(cantons, tmean)]
def national(shift): return sum(wi*inv(lg(TARGET/100)+shift+o) for wi, o in zip(w, off))/sum(w)
lo, hi = -3, 3
for _ in range(60):
    mid = (lo+hi)/2
    lo, hi = (mid, hi) if national(mid)*100 < TARGET else (lo, mid)
shift = (lo+hi)/2
out = {}
for c, o, t in zip(cantons, off, tmean):
    out[str(c['id'])] = {'yes': round(inv(lg(TARGET/100)+shift+o)*100, 1), 'turnout': round(t, 1)}
json.dump(out, open(os.path.join(root, 'data', 'rahmen.json'), 'w'), indent=1)
cy = sum((0.5 if c['half'] else 1) for c in cantons if out[str(c['id'])]['yes'] > 50)
for c in cantons: print(c['abbr'], out[str(c['id'])])
print('national', round(national(shift)*100, 2), 'cantons yes', cy,
      'turnout', round(sum(c['voters']*float(out[str(c['id'])]['turnout']) for c in cantons)/sum(c['voters'] for c in cantons), 1))
