"""Draws the app icons: a blue boxing glove on the beech-green background.
Run:  py make_icons.py     (needs Pillow)
Not required to run the app — only to regenerate the PNG icons."""
from PIL import Image, ImageDraw

BG    = (78, 163, 41)     # background — beech-leaf green #4ea329, matching the app
GLOVE = (255, 255, 255)   # white glove body (matches the app's white buttons/text)
CUFF  = (205, 212, 223)   # light-grey wrist cuff
LINE  = (122, 135, 156)   # grey stitch / seam lines

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
    DX0, DY0, DX1, DY1 = 10, 6, 86, 90
    dw, dh = DX1 - DX0, DY1 - DY0
    scale = A / max(dw, dh)
    offx = ax0 + (A - dw * scale) / 2
    offy = ay0 + (A - dh * scale) / 2
    def T(x, y): return (offx + (x - DX0) * scale, offy + (y - DY0) * scale)
    def Sc(v): return v * scale
    def rrect(b, r, fill): d.rounded_rectangle([T(b[0], b[1]), T(b[2], b[3])], radius=Sc(r), fill=fill)
    def ell(b, fill):      d.ellipse([T(b[0], b[1]), T(b[2], b[3])], fill=fill)
    def arc(b, a0, a1, fill, w): d.arc([T(b[0], b[1]), T(b[2], b[3])], a0, a1, fill=fill, width=max(1, int(Sc(w))))

    # White flat-icon boxing-glove silhouette (mitten shape), light-grey cuff.
    # 1) wrist cuff
    rrect((34, 64, 82, 90), 10, CUFF)
    # 2) thumb — chunky rounded lobe to the lower left, joined at the bottom
    ell((10, 42, 48, 76), GLOVE)
    # 3) fist / knuckle pad — big rounded block
    rrect((30, 6, 86, 70), 24, GLOVE)
    # 4) carve a concave notch at the thumb/fingers junction (bite from the upper-left)
    ell((16, 18, 44, 46), BG)
    # 5) stitch lines: knuckle seam near the top + the cuff band
    arc((44, 12, 74, 42), 200, 322, LINE, 3.4)
    d.line([T(40, 70), T(76, 70)], fill=LINE, width=max(1, int(Sc(2.6))))

    return img.resize((size, size), Image.LANCZOS)

def save(size, name, **kw):
    draw_glove(size, **kw).save(name)
    print("wrote", name)

save(192, "icon-192.png")
save(512, "icon-512.png")
save(512, "icon-maskable-512.png", pad_frac=0.26)
save(180, "apple-touch-icon.png")
print("done")
