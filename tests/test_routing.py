import math, unittest, numpy as np
from pathfinder.routing import astar, dijkstra, route_metrics
from pathfinder.terrain import slope_pct

class T(unittest.TestCase):
    def test_flat_straight_line(self):
        z = np.zeros((5, 11)); p, c, _ = astar(z, 10.0, (2, 0), (2, 10))
        self.assertAlmostEqual(c, 100.0); self.assertEqual(len(p), 11)

    def test_astar_equals_dijkstra_on_random_terrain(self):
        rng = np.random.default_rng(1)
        for _ in range(10):
            z = np.cumsum(np.cumsum(rng.normal(0, 0.3, (30, 30)), 0), 1) * 0.2
            _, ca, _ = astar(z, 5.0, (0, 0), (29, 29), max_slope_pct=60)
            _, cd, _ = dijkstra(z, 5.0, (0, 0), (29, 29), max_slope_pct=60)
            self.assertAlmostEqual(ca, cd, places=6)

    def test_astar_expands_fewer_nodes(self):
        z = np.zeros((60, 60))
        _, _, ea = astar(z, 1.0, (0, 0), (59, 59)); _, _, ed = dijkstra(z, 1.0, (0, 0), (59, 59))
        self.assertLess(ea, ed)

    def test_wall_forces_detour(self):
        z = np.zeros((9, 9)); z[:, 4] = 1000.0; z[8, 4] = 0.0     # cliff wall with one gap
        p, _, _ = astar(z, 1.0, (0, 0), (0, 8))
        self.assertIn((8, 4), p)
        for q in p: self.assertLess(z[q], 500)

    def test_unreachable_when_fully_blocked(self):
        z = np.zeros((9, 9)); z[:, 4] = 1000.0
        p, c, _ = astar(z, 1.0, (0, 0), (0, 8)); self.assertIsNone(p); self.assertEqual(c, math.inf)

    def test_nodata_is_never_crossed(self):
        z = np.zeros((9, 9)); z[:, 4] = np.nan; z[8, 4] = 0.0
        p, _, _ = astar(z, 1.0, (0, 0), (0, 8))
        self.assertIn((8, 4), p)
        self.assertTrue(all(np.isfinite(z[q]) for q in p))
        z[8, 4] = np.nan
        self.assertIsNone(astar(z, 1.0, (0, 0), (0, 8))[0])

    def test_start_on_nodata_raises(self):
        z = np.zeros((4, 4)); z[0, 0] = np.nan
        with self.assertRaises(ValueError): astar(z, 1.0, (0, 0), (3, 3))

    def test_slope_of_known_plane(self):
        x = np.arange(20) * 8.0; z = np.tile(0.10 * x, (20, 1))      # 10 % grade in x
        s = slope_pct(z, 8.0); self.assertTrue(np.allclose(s[5:15, 5:15], 10.0))

    def test_metrics_on_known_ramp(self):
        z = np.tile(np.array([0, 1, 2, 3, 2, 1.0]) , (3, 1)); p = [(1, i) for i in range(6)]
        m = route_metrics(z, 10.0, p)
        self.assertAlmostEqual(m["distance_m"], 50.0); self.assertAlmostEqual(m["gain_m"], 3.0)
        self.assertAlmostEqual(m["loss_m"], 2.0); self.assertAlmostEqual(m["max_slope_pct"], 10.0)

    def test_steep_move_excluded(self):
        z = np.array([[0.0, 100.0]]); self.assertIsNone(astar(z, 8.0, (0, 0), (0, 1))[0])

    def test_rough_band_is_avoided_when_detour_exists(self):
        z = np.zeros((11, 11)); r = np.zeros((11, 11)); r[:, 5] = 0.9; r[0, 5] = 0.0   # rough wall, one smooth gap at row 0
        p, _, _ = astar(z, 1.0, (5, 0), (5, 10), rough=r, rough_max=1.0, kr=50.0)
        self.assertIn((0, 5), p)

    def test_rough_over_limit_is_excluded_and_unreachable(self):
        z = np.zeros((7, 7)); r = np.zeros((7, 7)); r[:, 3] = 2.0
        self.assertIsNone(astar(z, 1.0, (3, 0), (3, 6), rough=r, rough_max=1.0)[0])

    def test_astar_equals_dijkstra_with_roughness(self):
        rng = np.random.default_rng(7); z = np.cumsum(rng.normal(0, .2, (25, 25)), 0); r = rng.uniform(0, .8, (25, 25))
        a = astar(z, 5.0, (0, 0), (24, 24), max_slope_pct=80, rough=r)[1]; d = dijkstra(z, 5.0, (0, 0), (24, 24), max_slope_pct=80, rough=r)[1]
        self.assertAlmostEqual(a, d, places=6)

    def test_nan_roughness_is_not_safe(self):
        z = np.zeros((5, 5)); r = np.zeros((5, 5)); r[:, 2] = np.nan
        self.assertIsNone(astar(z, 1.0, (2, 0), (2, 4), rough=r)[0])

if __name__ == "__main__": unittest.main()
