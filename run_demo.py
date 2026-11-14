import json, math, time, numpy as np, cv2
from pathfinder.routing import astar, dijkstra, route_metrics
from pathfinder.terrain import slope_pct

Z = np.load("data/dtm_8m.npy"); F = 4
RES = 2.0192195414267 * F
R_MARS, LON0, LAT1 = 3394839.8133163, 78.15, math.radians(15.0)
X0, Y0, PX = -3446.807757215175, 1113298.7133851524, 2.0192195414267

def rc_to_lonlat(r, c):
    x = X0 + (c * F + F / 2) * PX; y = Y0 - (r * F + F / 2) * PX
    return LON0 + math.degrees(x / (R_MARS * math.cos(LAT1))), math.degrees(y / R_MARS)

valid = np.isfinite(Z)
rows = np.where(valid.any(axis=1))[0]
def pick(r):
    cs = np.where(valid[r])[0]; return (int(r), int(cs[len(cs)//2]))
start, goal = pick(rows[0] + 40), pick(rows[-1] - 40)
print("start", start, rc_to_lonlat(*start), "goal", goal, rc_to_lonlat(*goal))

t = time.time(); path, cost, n = astar(Z, RES, start, goal); print("A* %.1fs expanded %d cost %.1f" % (time.time()-t, n, cost))
m = route_metrics(Z, RES, path)
print({k: round(v, 1) for k, v in m.items() if not k.startswith("profile")})

# Dijkstra baseline on a real-terrain crop around the route's first 250x250 window
r0, c0 = start[0], max(0, start[1]-125)
crop = Z[r0:r0+250, c0:c0+250]
s = (0, start[1]-c0); vr, vc = np.where(np.isfinite(crop)); i = np.argmax(vr + 0*vc)
g = (int(vr[i]), int(vc[i]))
pa, ca, na = astar(crop, RES, s, g); pd, cd, nd = dijkstra(crop, RES, s, g)
print("crop check: A* cost %.4f (exp %d) vs Dijkstra %.4f (exp %d)" % (ca, na, cd, nd))

coords = [rc_to_lonlat(*p) for p in path]
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {
    "algorithm": "A* 8-connected, 8 m grid", "max_slope_limit_pct": 47.0, "assumption": "prototype, not NASA limit",
    **{k: v for k, v in m.items() if not k.startswith("profile")}},
    "geometry": {"type": "LineString", "coordinates": coords}}]}, open("data/route.geojson", "w"))
json.dump({"dist_m": m["profile_dist_m"], "elev_m": m["profile_elev_m"]}, open("data/profile.json", "w"))

# preview: hillshade + route
gy, gx = np.gradient(np.nan_to_num(Z, nan=np.nanmin(Z)), RES); sl = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, gy)
hs = np.clip(np.sin(np.radians(45))*np.cos(sl) + np.cos(np.radians(45))*np.sin(sl)*np.cos(np.radians(315)-asp), 0, 1)
img = cv2.cvtColor((hs*255).astype("uint8"), cv2.COLOR_GRAY2BGR); img[~valid] = 0
cv2.polylines(img, [np.array([[c, r] for r, c in path], np.int32)], False, (0, 220, 255), 2)
cv2.circle(img, start[::-1], 8, (0, 255, 0), -1); cv2.circle(img, goal[::-1], 8, (0, 0, 255), -1)
cv2.imwrite("data/route_preview.png", img)
