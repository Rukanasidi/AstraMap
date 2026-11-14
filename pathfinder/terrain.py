"""Terrain helpers. All distances in metres, elevations in metres (Mars datum), slope in percent (rise/run*100)."""
import numpy as np

def slope_pct(z, res):
    """Central-difference slope in percent. NaN-aware: any NaN in the stencil gives NaN."""
    gy, gx = np.gradient(z, res)
    return 100.0 * np.hypot(gx, gy)

def block_mean(a, f, min_valid=0.75):
    """Downsample by integer factor f; a block is NaN if fewer than min_valid of its cells are valid."""
    h, w = (a.shape[0] // f) * f, (a.shape[1] // f) * f
    blk = a[:h, :w].reshape(h // f, f, w // f, f)
    ok = np.isfinite(blk)
    cnt = ok.sum(axis=(1, 3))
    s = np.where(ok, blk, 0).sum(axis=(1, 3))
    return np.where(cnt >= f * f * min_valid, s / np.maximum(cnt, 1), np.nan)
