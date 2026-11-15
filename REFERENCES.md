# References and Sources

Everything Mars Pathfinder uses or cites, with what it was used for and its status.

## NASA / USGS data (used in the app)

1. **HiRISE Digital Terrain Model `DTEED_033651_1990_033717_1990_A01`**
   NASA/JPL/University of Arizona, Mars Reconnaissance Orbiter, HiRISE. Catalog: https://www.uahirise.org/dtm
   *Used for:* elevation, slope, roughness and route planning (2.019 m/pixel, resampled to 8 m).

2. **HiRISE orthoimage `ESP_033651_1990_IRB_D_01_ORTHO`** (infrared-red-blue false colour)
   NASA/JPL/University of Arizona, MRO/HiRISE. Same catalog as above.
   *Used for:* the imagery base layer.

## Landing-page texture (used in the app)

3. **Mars colour map, `Solarsystemscope_texture_2k_mars.jpg`** (2048 x 1024)
   Solar System Scope (https://www.solarsystemscope.com/textures/), licensed CC BY 4.0, based on NASA imagery data.
   Obtained via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Solarsystemscope_texture_2k_mars.jpg
   Required attribution: "Solar System Scope, CC BY 4.0, via Wikimedia Commons".
   *Used for:* the 3D globe on the landing page and, since the 3D globe view was added to Mission Control, as the default surface texture of that globe (embedded in the file, works offline).

## Challenge material

4. **NASA Space Apps Challenge 2026, "Interplanetary Survival Guide: Martian Map"**
   https://www.spaceappschallenge.org/2026/challenges/interplanetary-survival-guide-martian-map/
   *Used for:* scope, objectives and the idea of layering several kinds of data for a Marswalk.

5. **Challenge resources list** (provided with the challenge; **not yet integrated as data**)
   - JPL Mars Trek: https://trek.nasa.gov/mars/
   - USGS-NASA Planetary Geologic Mapping Program: https://astrogeology-usgs.hub.arcgis.com/pages/interactive-maps-mars
   - Curiosity proposed route example: https://science.nasa.gov/resource/curiositys-proposed-path-up-mount-sharp/
   - Mars Perseverance Raw Images Gallery: https://mars.nasa.gov/mars2020/multimedia/raw-images/

## Algorithms

6. Hart, P. E., Nilsson, N. J., and Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths." *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107. (A\*)
7. Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs." *Numerische Mathematik*, 1, 269-271. (baseline search)

## Team documents

8. **Mars Pathfinder blueprint (PDF)** and **Pharmaceutical and life-support module (DOCX)**, written by the team.
   *Used for:* scope, provenance and uncertainty rules, alert levels, and the thresholds listed below.

## Thresholds and constants (verify before final submission)

9. **NASA-STD-3001, Volume 2, Rev F** (human spaceflight health and performance standard), cited by the team's pharmaceutical document for oxygen partial pressure, CO2 and cabin pressure ranges.
   **Status: the values were taken from the team document and have not been independently checked against the standard.**
10. **Energy equivalent of oxygen (about 20.1 kJ per litre) and respiratory quotient (0.85).** Standard exercise-physiology values used in the oxygen estimator. **Status: add a textbook or paper citation of your choice; none was looked up for this project.**
11. **Water, oxygen-supply and cabin-temperature bands, and all crew vital-sign bands.** Proposed settings by the team and the developer, not NASA values. Vital-sign bands need clinician confirmation.

## Software used to build it

12. Python, NumPy, SciPy, Pillow and OpenCV (data processing, routing engine, tests and previews); plain HTML, CSS, JavaScript and WebGL for the app, plus Three.js (item 16) for the Mission Control 3D globe.

## 3D globe in Mission Control (added in the final version)

13. **ARES-V globe module** (`mars-globe.js`, `jezero-data.js`, `pathfinding.js`), written by a Mars Pathfinder team member (repository `nasa-challenge--MarsMap-2026`). Lightly modified: pauses when hidden, label text changed, default texture replaced by item 3.
   *Status:* its Jezero overlay layers and terrain-height function are **illustrative, not derived from the HiRISE strip**; they are hidden by default and labelled as such in the app.
14. **Exploration-target list** (Jezero, Gale, Valles Marineris, Olympus Mons, Gusev, Meridiani: names, coordinates and descriptions), taken from `src/destinations.js` in the team repository `L0C4LH057/Nasa_pathFinders`.
   *Status:* only Jezero has terrain data in this app; the others are navigation targets only.
15. **Surface layers on the globe**, streamed at run time from the USGS Astrogeology Mars web map service (https://planetarymaps.usgs.gov/), so they need an internet connection:
   - **THEMIS infrared, day and night** (Mars Odyssey). Christensen, P. R., et al. (2004). "The Thermal Emission Imaging System (THEMIS) for the Mars 2001 Odyssey Mission." *Space Science Reviews*, 110, 85-130. Used for the thermal layers.
   - **MOLA elevation colour** (Mars Global Surveyor). Smith, D. E., et al. (2001). "Mars Orbiter Laser Altimeter: Experiment summary after the first year of global mapping of Mars." *Journal of Geophysical Research*, 106(E10), 23689-23722. Used for the elevation-colour layer.
   *Status:* the layer names were not verified against the live service when the app was built; if one fails to load the app falls back to the visible layer.
16. **Three.js r128**, MIT licence, https://github.com/mrdoob/three.js (included in `index.html`).

## Considered but not integrated

17. **Global CTX Mosaic of Mars (V01)**, Bruce Murray Laboratory for Planetary Visualization, Caltech: https://murray-lab.caltech.edu/CTX/ (5 m/pixel; free use; credit "NASA/JPL/MSSS/The Murray Lab"; the page asks users to cite its Earth and Space Science paper and to acknowledge the Malin Space Science Systems and JPL teams). Distributed as 4 x 4 degree GeoTIFF tiles with no streaming service; the tile covering Jezero and our HiRISE strip is E076_N016. **Not used in the app unless a Jezero crop is added; do not list it as used until then.** Add the full paper citation from the Murray Lab page if it is used.
18. **JPL Mars Trek** WMTS tile services (https://trek.nasa.gov/tiles/apidoc/trekAPI.html?body=mars) and **ASU JMARS TES mineral maps**: reviewed as possible thermal, spectral and mineral layers; not integrated.
19. **Atmospheric and radiation data** (for example Mars 2020 MEDA weather and Curiosity RAD radiation data from the NASA Planetary Data System): not integrated; these are time series rather than map layers.

## Disclaimer

NASA does not endorse this project. It is an independent educational prototype, not flight-certified and not a safety system.