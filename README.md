# Ständemehr-Simulator

Interactive, single-file web app: set the yes share and turnout for each of the 26 Swiss cantons and see the overall yes share, the number of cantons in favour (Ständemehr) and whether a proposal is accepted (needs both Volksmehr and Ständemehr).

- Eligible voters per canton (incl. Swiss abroad) and default values: BFS results of the 14 June 2026 vote «Keine 10-Millionen-Schweiz!».
- Half-cantons count ½; 12 of 23 cantonal votes are needed; a canton at exactly 50 % counts as "no".
- Languages: DE, FR, IT, RM, EN. Responsive: desktop, tablet and phone.

Open `index.html` directly. To regenerate: `python3 scripts/fetch_data.py && python3 scripts/make_map.py && python3 scripts/make_eu_scenario.py && python3 scripts/build.py` (edit `src/template.html`, not `index.html`).

## Data sources and credits
- Eligible voters and starting values: Federal Statistical Office (BFS), open data of the vote of 14 June 2026.
- Historical per-canton results for the hypothetical "Rahmenverträge" scenario: [Swissvotes](https://swissvotes.ch) (Année Politique Suisse, University of Bern).
- Map shapes: [swiss-maps](https://github.com/interactivethings/swiss-maps) (based on swisstopo data).

The "Rahmenverträge" scenario is a hypothetical illustration, not a forecast.
