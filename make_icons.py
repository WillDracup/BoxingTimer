"""Generates the app icons by recolouring the Vecteezy boxing-glove artwork into
our palette: a WHITE glove (with the green background showing through the seams)
on the beech-green background.

Source artwork: "Boxing sign icon" by Vecteezy (Sports_(112).jpg). It is NOT
committed to this repo (the Vecteezy licence doesn't allow redistributing the
original asset) — only the recoloured PNG icons we render are. Point SRC at the
downloaded file to regenerate.  Run:  py make_icons.py   (needs Pillow)
"""
import os
from PIL import Image

SRC = r"C:\Users\user\Downloads\vecteezy_boxing-sign-icon-vector-illustration-for-personal-and-commercial-use-clean-look-trendy-icon_421048\Sports_(112).jpg"

BG    = (78, 163, 41)      # beech-leaf green #4ea329, matching the app
GLOVE = (255, 255, 255)    # white glove

# levels for turning the (near black/white) source into a clean alpha mask:
# darker than LO = solid glove, lighter than HI = background, smooth between.
LO, HI = 95, 175

def load_mask():
    """Return an 'L' image where 255 = glove, 0 = background, autocropped to the glove."""
    g = Image.open(SRC).convert("L")
    lut = [0 if v >= HI else 255 if v <= LO else int(round((HI - v) / (HI - LO) * 255))
           for v in range(256)]
    a = g.point(lut)                       # alpha: glove opaque, background transparent
    bbox = a.getbbox()
    return a.crop(bbox) if bbox else a

MASK = load_mask()

def make(size, pad_frac):
    S = size * 4                            # supersample for smooth downscale
    canvas = Image.new("RGBA", (S, S), BG + (255,))
    avail = S * (1 - 2 * pad_frac)
    mw, mh = MASK.size
    scale = avail / max(mw, mh)
    w, h = max(1, round(mw * scale)), max(1, round(mh * scale))
    m = MASK.resize((w, h), Image.LANCZOS)
    glove = Image.new("RGBA", (w, h), GLOVE + (0,))
    glove.putalpha(m)                       # white where the glove is, transparent elsewhere
    canvas.alpha_composite(glove, ((S - w) // 2, (S - h) // 2))
    return canvas.resize((size, size), Image.LANCZOS)

def save(size, name, pad_frac):
    make(size, pad_frac).save(name)
    print("wrote", name)

if not os.path.exists(SRC):
    raise SystemExit("Source artwork not found. Update SRC to the downloaded Vecteezy JPG.")

save(192, "icon-192.png", 0.16)
save(512, "icon-512.png", 0.16)
save(512, "icon-maskable-512.png", 0.26)
save(180, "apple-touch-icon.png", 0.16)
print("done")
