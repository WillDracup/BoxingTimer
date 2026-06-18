"""Draws the app icons: a blue boxing glove on the beech-green background.
Run:  py make_icons.py     (needs Pillow)
Not required to run the app — only to regenerate the PNG icons."""
from PIL import Image, ImageDraw

BG    = (78, 163, 41)     # background — beech-leaf green #4ea329, matching the app
BLUE  = (31, 104, 216)    # glove body — #1f68d8, the sparring blue
BLUE_D= (18, 70, 158)     # cuff / shadow
BLUE_H= (120, 160, 242)   # highlight
SEAM  = (15, 54, 130)     # stitching seams

def draw_glove(size, pad_frac=0.0):
    """Render at 4x then downscale for smooth edges. The glove is laid out in a
    design space and centred (by its bounding box) inside the tile."""
    S = size * 4
    img = Image.new("RGBA", (S, S), BG)
    d = ImageDraw.Draw(img)

    # available square — keep a base margin so the glove is nicely inset and centred;
    # maskable icons pass a larger pad_frac for the safe zone.
    base = 0.15
    p = S * max(pad_frac, base)
    ax0, ay0, A = p, p, S - 2 * p

    # design space + its bounding box (thumb at left, cuff at bottom)
    DX0, DY0, DX1, DY1 = 4, 6, 92, 92
    dw, dh = DX1 - DX0, DY1 - DY0
    scale = A / max(dw, dh)
    offx = ax0 + (A - dw * scale) / 2
    offy = ay0 + (A - dh * scale) / 2
    def T(x, y): return (offx + (x - DX0) * scale, offy + (y - DY0) * scale)
    def Sc(v): return v * scale
    def rrect(b, r, fill): d.rounded_rectangle([T(b[0], b[1]), T(b[2], b[3])], radius=Sc(r), fill=fill)
    def ell(b, fill):      d.ellipse([T(b[0], b[1]), T(b[2], b[3])], fill=fill)
    def arc(b, a0, a1, fill, w): d.arc([T(b[0], b[1]), T(b[2], b[3])], a0, a1, fill=fill, width=max(1, int(Sc(w))))

    # 1) wrist cuff (behind, darker), with a thin strap line
    rrect((32, 72, 80, 92), 11, BLUE_D)
    d.line([T(36, 81), T(76, 81)], fill=SEAM, width=max(1, int(Sc(2.4))))

    # 2) thumb — a rounded lobe to the lower left, drawn before the pad so the
    #    pad overlaps it and it reads as the thumb of the grip
    ell((6, 42, 44, 80), BLUE)

    # 3) main knuckle pad — big, bulbous, rounded
    rrect((22, 6, 90, 74), 32, BLUE)

    # 4) the one defining seam: the crease curving around the base of the thumb
    arc((28, 28, 58, 80), 100, 258, SEAM, 3.2)

    # 5) rim sheen along the upper-left edge (a crescent, not a blob)
    arc((27, 11, 83, 63), 176, 252, BLUE_H, 7)

    return img.resize((size, size), Image.LANCZOS)

def save(size, name, **kw):
    draw_glove(size, **kw).save(name)
    print("wrote", name)

save(192, "icon-192.png")
save(512, "icon-512.png")
save(512, "icon-maskable-512.png", pad_frac=0.26)
save(180, "apple-touch-icon.png")
print("done")
