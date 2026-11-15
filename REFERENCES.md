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
   *Used for:* the 3D globe on the landing page.

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

12. Python, NumPy, SciPy, Pillow and OpenCV (data processing, routing engine, tests and previews); plain HTML, CSS, JavaScript and WebGL for the app (no third-party front-end libraries).

## Disclaimer

NASA does not endorse this project. It is an independent educational prototype, not flight-certified and not a safety system.
