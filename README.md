Mars Pathfinder
A terrain-aware Marswalk route planner with a crew-resource layer.
Prototype for the NASA Space Apps Challenge 2026, Interplanetary Survival Guide: Martian Map.
> **Research / decision-support prototype.** Not flight-certified, not a real spacesuit monitor, not a guarantee of astronaut
> safety, and not a substitute for mission control. Resource and medical inputs are hypothetical demo values.
---
1. What it does
An astronaut (or planner) picks a start and a destination on a map of a real Martian location. The app computes a route
across real NASA terrain data, then shows what that route means for the crew:
3D Mars landing page: a rotating, draggable, zoomable globe (plain WebGL, no libraries). Clicking Mars (or pressing ENTER MISSION, Enter or Space) flies in toward the Jezero region and fades into Mission Control. Add `?skip` to the address to bypass it.
Layered map: HiRISE orthoimage, hillshade, elevation, slope and a roughness (rock-terrain) layer, with overlays for
excluded terrain and unknown (no-data) areas.
Computed route: A* path search on the terrain grid. Dijkstra is built in as a baseline, and a button compares the two.
Route metrics: distance, elevation gain/loss, slope statistics, roughness along the route, and an interactive elevation profile.
Adjustable cost model: sliders for the slope limit, slope penalty, roughness limit and roughness penalty. The route recomputes live.
Hypothetical round-trip oxygen estimator: metabolic assumptions to oxygen needed outbound and return, projected reserve and CO2 produced.
Pharmaceutical and medical module: FEFO inventory with low-stock / expiry / recall alerts, and crew vital-sign monitoring (demo data).
Life-support module: oxygen partial pressure, CO2, cabin pressure, temperature, water and oxygen supply, with units, colour and icon status, and editable thresholds.
Alerts: one prioritised list combining route, life-support, medical and pharmaceutical alerts, each with a suggested action.
Data & Methods tab: dataset register, methods and limitations.
2. Pilot area and data
Item	Value
Location	Eastern valley of Jezero Crater region, 18.59-18.79 N, 78.09-78.20 E (about 6.5 x 11.6 km strip)
Terrain	HiRISE DTM `DTEED_033651_1990_033717_1990_A01` (MRO/HiRISE, NASA/JPL/University of Arizona)
Imagery	`ESP_033651_1990_IRB_D_01_ORTHO` (false colour: infrared-red-blue)
Native resolution	2.019 m/pixel, 3202 x 5764
Projection	Equirectangular, centre longitude 78.15 E, standard parallel 15 N, Mars sphere radius 3394.84 km (planetocentric, east positive)
Elevation range	-2740.4 m to -2152.6 m (Mars datum used by the product)
Valid coverage	about 76 % of the rectangle (the strip is tilted; the rest is no-data)
Used by the app	8.08 m grid (4 x 4 block mean, a block must be at least 75 % valid), 800 x 1441 cells
Original NASA products come from the HiRISE DTM catalog (uahirise.org/dtm). Keep the originals unchanged; everything in `data/` is derived.
3. How to run
Just view the app: double-click `web/index.html` (Chrome, Edge or Firefox). It is one self-contained file: no internet, server or install needed.
Click the map once to set the start and again for the destination (or use the Set start / Set destination buttons). Cells with no data are rejected.
Move the sliders to change the cost model. The route updates.
Press Compare A* vs Dijkstra to check that both return the same optimal cost.
Hover the elevation profile to see the matching point on the map.
Open the other tabs for the pharmaceutical, life-support, alerts and methods views.
Run the Python engine and tests (Python 3.10+, `pip install numpy opencv-python`):
```bash
python3 -m unittest discover -s tests -t .   # 14 tests
python3 run_demo.py                          # computes the demo route, writes data/route.geojson, profile.json, route_preview.png
```
Rebuild the web app after editing `web/template.html` (needs `numpy`, `Pillow`; `mars_2k.jpg` must sit next to `build.py`):
```bash
cd web
python3 build.py /path/to/ESP_033651_1990_IRB_D_01_ORTHO.JP2
```
4. Project structure
```
pathfinder/            Python route engine
  terrain.py           slope and block-mean helpers
  routing.py           A*, Dijkstra, route metrics, cost model
tests/test_routing.py  14 unit tests
run_demo.py            end-to-end demo on the real terrain
data/
  dtm_8m.npy           8 m elevation grid (NaN = no data)
  rough_8m.npy         8 m roughness grid in metres
  route.geojson        demo route (lon/lat)
  profile.json         demo elevation profile
web/
  template.html        app source (HTML + CSS + JavaScript, no dependencies)
  landing.html/.css/.js  source of the 3D landing page (already merged into template.html)
  mars_2k.jpg          Mars colour map for the landing globe (Solar System Scope, CC BY 4.0)
  build.py             embeds the data and texture into template.html -> index.html
  index.html           the finished, self-contained app
```
5. Methods
Route planning. The terrain is an 8-connected grid. Each move costs
```
cost = distance_3D * (1 + k * (slope / slope_limit)^2 + kr * (roughness / roughness_limit)^2)
```
where `slope = |dz| / horizontal step`. Moves are hard-excluded when the slope exceeds the slope limit, when either cell is
rougher than the roughness limit, or when any cell is no-data. Unknown terrain is never treated as safe. The A* heuristic is straight-line
distance, which never overestimates because the cost multiplier is at least 1, so A* and Dijkstra return the same optimal cost.
The JavaScript search in the app is a port of `pathfinder/routing.py`; both give the same route and cost on the default case
(12.85 km, +317 m / -337 m, maximum slope 20.4 %).
Default parameters (prototype assumptions, not NASA limits): slope limit 47 % (about 25 degrees), k = 4, roughness limit 1.0 m, kr = 3.
Slope layer. Central-difference gradient of the 8 m DTM (display only). The planner uses move-to-move slopes.
Roughness layer. RMS of the 2 m DTM elevation minus its Gaussian smooth (sigma about 8 m), averaged over each 8 m cell.
It flags blocky or broken terrain. It does not resolve individual boulders.
Oxygen estimator. Energy = metabolic watts x time. Oxygen = energy / 20.1 kJ per litre. Uphill adds watts per percent grade.
Return uses the same path reversed. CO2 = respiratory quotient x oxygen. Every input is a configurable placeholder.
Alert levels. 0 NORMAL, 1 WATCH, 2 ALERT, 3 CRITICAL, always shown with an icon and a word, not colour alone.
Bands are editable as JSON on the Life-Support tab.
6. Reference values and what is official
NASA reference values (oxygen partial pressure 145-155 mmHg normal, CO2 at most 3 mmHg, cabin pressure above 5 and up to 15 psia)
come from the team's pharmaceutical module document, which cites NASA-STD-3001 Volume 2 Rev F.
They have not been independently re-checked against the standard. Verify before the final submission.
Water and oxygen-supply percentage bands, cabin temperature, and all crew vital-sign bands are proposed settings and are
labelled "proposed" in the app. Vital-sign bands need clinician confirmation. The system flags readings; it does not diagnose or prescribe.
Oxygen is shown as a partial pressure in mmHg for cabin monitoring and as a percentage of stored supply for reserves. These are different quantities.
7. Limitations (read before presenting)
Data kinds: only optical and topographic data (both MRO HiRISE) are used so far. Spectral, thermal, atmospheric and radiation layers are not yet included.
Ortho coverage: the orthoimage covers only part of the DTM footprint; hillshade fills the rest.
Landing page: needs WebGL. Without it the page shows a plain fallback and the ENTER MISSION button still works. It honours the browser's reduced-motion setting (no auto-spin, simple fade). The planet shown is a generic global colour map, not the pilot strip.
Hazards: slope and roughness only. No individual boulders, sand softness, traction, thermal, dust, radiation or communications model.
Resolution: an 8 m grid hides features of a few metres.
Pharmaceutical and vital-sign data are fictional demo data. Expiry alerts use the current date of whoever opens the page.
Estimators: metabolic, speed and oxygen values are assumptions, not a suit model, and do not predict survival.
Location: this strip is roughly 40 km east of the Perseverance landing site, so rover traverse and sample-site data may not fall inside it.
8. Roadmap
Add layers from further NASA missions through Mars Trek (CRISM minerals, THEMIS thermal, MOLA regional topography) with a provenance card for each.
Add real, source-linked science targets, the USGS geologic map, and point-of-view images from Perseverance raw images.
Add an atmospheric or radiation conditions panel with the observation date and source shown.
State one clear science objective for the mission and tie the route, resources and alerts to it.
Review the thresholds against NASA-STD-3001 and with a clinician; replace demo medical data with a documented fictional dataset.
9. Reproducing the derived data
```python
import numpy as np
from scipy.ndimage import gaussian_filter

# 1. Read the PDS3 .IMG (header = 12808 bytes, 32-bit little-endian floats, 5764 x 3202)
a = np.fromfile("DTEED_033651_1990_033717_1990_A01.IMG", dtype="<f4", offset=12808).reshape(5764, 3202).astype("float64")
valid = np.isfinite(a) & (a > -1e30)

# 2. 8 m elevation grid: 4x4 block mean, block valid if >= 75 % of cells valid  (see pathfinder/terrain.py: block_mean)

# 3. Roughness: residual from an ~8 m Gaussian smooth, RMS per 4x4 block (>= 12 valid cells)
v = np.where(valid, a, 0.0)
smooth = gaussian_filter(v, 4.0) / np.maximum(gaussian_filter(valid.astype(float), 4.0), 1e-9)
resid = np.where(valid, a - smooth, 0.0)
blocks = (resid[:5764, :3200] ** 2).reshape(1441, 4, 800, 4)
count = valid[:5764, :3200].reshape(1441, 4, 800, 4).sum((1, 3))
rough = np.where(count >= 12, np.sqrt(blocks.sum((1, 3)) / np.maximum(count, 1)), np.nan)
```
The no-data value in the raw file is `0xFF7FFFFB` (a large negative float); the `a > -1e30` test removes it.
10. Credits and attribution
Terrain and imagery: NASA/JPL/University of Arizona, Mars Reconnaissance Orbiter HiRISE.
Challenge: NASA Space Apps Challenge 2026, Interplanetary Survival Guide: Martian Map.
Landing-page Mars texture: Solar System Scope (solarsystemscope.com/textures), CC BY 4.0, via Wikimedia Commons, based on NASA imagery data. The attribution is shown on the landing page and in the Data & Methods tab; keep it if you redistribute the app.
NASA does not endorse this project. It is an independent prototype built by the team for the challenge.
Team: add team name and members here