#!/usr/bin/env python3
"""Download the official results of the 14 June 2026 vote (BFS open data) and
extract the per-canton figures used as defaults into data/cantons.json."""
import json, urllib.request, pathlib

URL = "https://ogd-static.voteinfo-app.ch/v1/ogd/sd-t-17-02-20260614-eidgAbstimmung.json"
VORLAGE = 6860  # Volksinitiative «Keine 10-Millionen-Schweiz! (Nachhaltigkeitsinitiative)»
HALF = {6, 7, 12, 13, 15, 16}  # OW, NW, BS, BL, AR, AI
ABBR = "ZH BE LU UR SZ OW NW GL ZG FR SO BS BL SH AR AI SG GR AG TG TI VD VS NE GE JU".split()

root = pathlib.Path(__file__).resolve().parent.parent
raw = json.load(urllib.request.urlopen(URL))
v = next(x for x in raw["schweiz"]["vorlagen"] if x["vorlagenId"] == VORLAGE)
cantons = []
for k in v["kantone"]:
    r, n = k["resultat"], int(k["geoLevelnummer"])
    cantons.append({
        "id": n, "abbr": ABBR[n - 1], "half": n in HALF,
        "voters": r["anzahlStimmberechtigte"],
        "turnout": round(r["stimmbeteiligungInProzent"], 2),
        "yes": round(r["jaStimmenInProzent"], 2),
    })
(root / "data" / "cantons.json").write_text(json.dumps(cantons, indent=1))
print(f"{len(cantons)} cantons, {sum(c['voters'] for c in cantons)} eligible voters")
