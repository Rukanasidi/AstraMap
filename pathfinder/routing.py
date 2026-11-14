"""Grid route planning: A* (with admissible heuristic) and a Dijkstra baseline.

Cost model (PROTOTYPE ASSUMPTIONS, not NASA safety limits):
  edge_cost = dist3d * (1 + k * (edge_slope / max_slope) ** 2 + kr * (rough / rough_max) ** 2)
  - edge_slope = |dz| / horizontal distance of that move
  - moves with edge_slope > max_slope are HARD-EXCLUDED
  - rough = surface roughness (m, RMS elevation residual, a proxy for blocky/rocky terrain). A move is
    HARD-EXCLUDED if either cell has rough > rough_max; the penalty uses the mean of the two cells. Roughness is optional (rough=None disables it).
  - any NaN (no-data) cell is HARD-EXCLUDED, never treated as safe
The multiplier is always >= 1, so straight-line 2-D distance never overestimates remaining
cost, which keeps the A* heuristic admissible (so A* cost == Dijkstra cost).
"""
import heapq, math
import numpy as np

SQ2 = math.sqrt(2.0)
NEIGHBOURS = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
              (-1, -1, SQ2), (-1, 1, SQ2), (1, -1, SQ2), (1, 1, SQ2)]

def edge_cost(z0, z1, hdist, max_slope_pct, k, r0=0.0, r1=0.0, rough_max=1.0, kr=0.0):
    """Return cost of a move, or None if excluded."""
    if not (math.isfinite(z0) and math.isfinite(z1)):
        return None
    rr = 0.0
    if kr or r0 or r1:
        if not (math.isfinite(r0) and math.isfinite(r1)):
            return None            # unknown roughness is not treated as safe
        if r0 > rough_max or r1 > rough_max:
            return None            # either endpoint too rough -> hard exclusion
        rr = 0.5 * (r0 + r1)
    dz = z1 - z0
    s = abs(dz) / hdist * 100.0
    if s > max_slope_pct:
        return None
    d3 = math.hypot(hdist, dz)
    return d3 * (1.0 + k * (s / max_slope_pct) ** 2 + kr * (rr / rough_max) ** 2)

def _search(z, res, start, goal, max_slope_pct, k, use_heuristic, rough=None, rough_max=1.0, kr=0.0):
    rows, cols = z.shape
    for p in (start, goal):
        if not (0 <= p[0] < rows and 0 <= p[1] < cols) or not math.isfinite(z[p]):
            raise ValueError("start/goal outside grid or on no-data cell: %r" % (p,))
    gscore = {start: 0.0}
    came = {}
    def h(p):
        return res * math.hypot(p[0] - goal[0], p[1] - goal[1]) if use_heuristic else 0.0
    heap = [(h(start), 0.0, start)]
    closed = set()
    expanded = 0
    while heap:
        f, g, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        expanded += 1
        if cur == goal:
            path = [cur]
            while cur in came:
                cur = came[cur]; path.append(cur)
            return path[::-1], g, expanded
        r, c = cur
        z0 = float(z[r, c])
        r0 = float(rough[r, c]) if rough is not None else 0.0
        for dr, dc, m in NEIGHBOURS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or (nr, nc) in closed:
                continue
            r1 = float(rough[nr, nc]) if rough is not None else 0.0
            ec = edge_cost(z0, float(z[nr, nc]), res * m, max_slope_pct, k, r0, r1, rough_max, kr if rough is not None else 0.0)
            if ec is None:
                continue
            ng = g + ec
            if ng < gscore.get((nr, nc), math.inf):
                gscore[(nr, nc)] = ng
                came[(nr, nc)] = cur
                heapq.heappush(heap, (ng + h((nr, nc)), ng, (nr, nc)))
    return None, math.inf, expanded

def astar(z, res, start, goal, max_slope_pct=47.0, k=4.0, rough=None, rough_max=1.0, kr=3.0):
    return _search(z, res, start, goal, max_slope_pct, k, True, rough, rough_max, kr)

def dijkstra(z, res, start, goal, max_slope_pct=47.0, k=4.0, rough=None, rough_max=1.0, kr=3.0):
    return _search(z, res, start, goal, max_slope_pct, k, False, rough, rough_max, kr)

def route_metrics(z, res, path):
    """Distance, elevation gain/loss, slope stats and profile for a path of (row, col) cells."""
    zs = np.array([z[p] for p in path], dtype=float)
    steps = np.array([res * math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(path[:-1], path[1:])])
    dz = np.diff(zs)
    slopes = np.abs(dz) / steps * 100.0
    cum = np.concatenate([[0.0], np.cumsum(steps)])
    return {
        "distance_m": float(steps.sum()),
        "distance_3d_m": float(np.hypot(steps, dz).sum()),
        "gain_m": float(dz[dz > 0].sum()),
        "loss_m": float(-dz[dz < 0].sum()),
        "max_slope_pct": float(slopes.max()) if len(slopes) else 0.0,
        "mean_slope_pct": float(slopes.mean()) if len(slopes) else 0.0,
        "profile_dist_m": cum.tolist(),
        "profile_elev_m": zs.tolist(),
    }
