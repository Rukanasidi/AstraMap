"""Rebuild web/index.html (self-contained) from template.html.
Needs: ../data/dtm_8m.npy and the HiRISE ortho JP2 (path as argv[1]); numpy + Pillow."""
import sys, base64, io, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
z = np.load("../data/dtm_8m.npy"); ZMIN = -2740.5
u = np.where(np.isfinite(z), np.round((z - ZMIN) * 100), 65535).astype("<u2")
im = Image.open(sys.argv[1]).convert("RGB").resize((1600, 2882), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=78, optimize=True)
t = open("template.html").read().replace("__DTM_B64__", base64.b64encode(u.tobytes()).decode()).replace("__ORTHO_B64__", base64.b64encode(buf.getvalue()).decode())
rg = np.load("../data/rough_8m.npy"); ru = np.where(np.isfinite(rg), np.clip(np.round(rg * 100), 0, 254), 255).astype("u1")
t = t.replace("__ROUGH_B64__", base64.b64encode(ru.tobytes()).decode())
open("index.html", "w").write(t); print("wrote index.html", len(t) // 1024, "KB")
