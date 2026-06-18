"""Draws the app icons: a red boxing glove on a dark background.
Run:  py make_icons.py     (needs Pillow)
Not required to run the app — only to regenerate the PNG icons."""
from PIL import Image, ImageDraw

INK   = (78, 163, 41)     # background — beech-leaf green #4ea329, matching the app
RED   = (31, 104, 216)    # glove body — #1f68d8, same as the sparring blue
RED_D = (20, 72, 162)     # shadow / outline
RED_H = (122, 160, 240)   # highlight
SEAM  = (16, 58, 138)

def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def draw_glove(size, bg=True, pad_frac=0.0):
    """Render at 4x then downscale for smooth edges."""
    S = size * 4
    img = Image.new("RGBA", (S, S), INK if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # working area (maskable leaves padding so nothing important is clipped)
    p = S * pad_frac
    x0, y0, x1, y1 = p, p, S - p, S - p
    w = x1 - x0
    cx = (x0 + x1) / 2

    # cuff (wrist) at the bottom
    cuff_w = w * 0.46
    cuff_h = w * 0.20
    cuff_top = y0 + w * 0.66
    rrect(d, [cx - cuff_w/2, cuff_top, cx + cuff_w/2, cuff_top + cuff_h],
          r=cuff_h*0.32, fill=RED_D)

    # main fist body
    fist_w = w * 0.62
    fist_h = w * 0.52
    fx0 = cx - fist_w/2
    fy0 = y0 + w * 0.16
    rrect(d, [fx0, fy0, fx0 + fist_w, fy0 + fist_h], r=fist_w*0.34, fill=RED)

    # thumb (left bump)
    th = w * 0.26
    ty = fy0 + fist_h*0.30
    d.ellipse([fx0 - th*0.55, ty, fx0 + th*0.55, ty + th], fill=RED)

    # knuckle highlight
    d.ellipse([cx - fist_w*0.30, fy0 + fist_h*0.12,
               cx + fist_w*0.10, fy0 + fist_h*0.46], fill=RED_H)

    # seam between fingers and thumb
    d.line([cx - fist_w*0.12, fy0 + fist_h*0.18,
            cx - fist_w*0.12, fy0 + fist_h*0.92], fill=SEAM, width=int(S*0.012))

    return img.resize((size, size), Image.LANCZOS)

def save(size, name, **kw):
    draw_glove(size, **kw).save(name)
    print("wrote", name)

# a little smaller than before: more padding around the glove on every icon
save(192, "icon-192.png", pad_frac=0.13)
save(512, "icon-512.png", pad_frac=0.13)
save(512, "icon-maskable-512.png", pad_frac=0.24)
save(180, "apple-touch-icon.png", pad_frac=0.13)
print("done")
