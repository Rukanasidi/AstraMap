# Mars Pathfinder – terrain + route engine (prototype)

Data: HiRISE DTM DTEED_033651_1990_033717_1990_A01 (NASA/JPL/University of Arizona, MRO/HiRISE), 2.019 m/px,
Mars equirectangular (centre lon 78.15 E, std parallel 15 N, radius 3394.84 km), 3202 x 5764 px.
Derived: data/dtm_8m.npy = 4x4 block mean (8.08 m/px; blocks <75% valid are NaN/no-data).

Run:   python3 run_demo.py            (needs numpy, opencv; ~10 s)
Test:  python3 -m unittest discover -s tests -t .

Cost model = PROTOTYPE ASSUMPTIONS (not NASA limits): hard exclusion above 47 % (~25 deg) edge slope,
no-data cells excluded, slope penalty k=4. Hazards/boulders/dunes are NOT modelled yet.
Outputs: data/route.geojson (lon/lat, east-positive planetocentric), data/profile.json, data/route_preview.png

## Front end (web/index.html)
Self-contained, no internet or libraries needed: just double-click web/index.html (Chrome/Edge/Firefox).
Click the map twice (start, destination) to compute a route in the browser (A* port of routing.py).
Rebuild after changing template.html:  cd web && python3 build.py <path to ESP_033651_1990_IRB_D_01_ORTHO.JP2>

## Roughness (rock-terrain proxy)
data/rough_8m.npy = RMS of (2 m DTM minus its ~8 m Gaussian smooth) per 8 m cell, in metres. Routing excludes cells above the
roughness limit (default 1.0 m) and penalises roughness (kr = 3). It flags blocky terrain; it does NOT resolve individual boulders.
