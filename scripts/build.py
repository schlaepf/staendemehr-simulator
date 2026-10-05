#!/usr/bin/env python3
"""Inline data/cantons.json and data/map.json into src/template.html -> index.html."""
import json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
cantons = json.loads((root / "data" / "cantons.json").read_text())
rahmen = json.loads((root / "data" / "rahmen.json").read_text())
map_ = json.loads((root / "data" / "map.json").read_text())
data = f"const CANTONS = {json.dumps(cantons, separators=(',', ':'))};\nconst RAHMEN = {json.dumps(rahmen, separators=(',', ':'))};\nconst MAP = {json.dumps(map_, separators=(',', ':'))};"
html = (root / "src" / "template.html").read_text().replace("/*__DATA__*/", data)
(root / "index.html").write_text(html)
print(f"index.html: {len(html) / 1024:.0f} KB")
