# -*- coding: utf-8 -*-
"""
Genereate seamless 512x512 textures for the medieval GUI.
Implements README-AI.md section 5.3:
 - parchment.png: base #e7dcc2, effect_noise alpha 18-25, 40-60 fibers
   (#d3c19c, a 20-40, blur 1), 6-10 radial stains (#bfa87f, a 12-25),
   periodic edge vignette (>=0.94).
 - wood.png: base #3d2a1c, vertical grain lines via
   base + 8*sin(k*x + 6*periodic_noise(y)), colors #2c1d13/#513a26,
   2-3 long cracks alpha 60, vignette. Periodic in BOTH axes (harmonic
   frequencies are integer multiples of 2*pi/512) -> seamless tiling.
 - rule.png: double ink line, 2 px, #3a2a1d, gap 4 px.
Every drawn element is stamped 9 times with offsets
(-512,0,+512)x(-512,0,+512) on a padded transparent layer, then flattened.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

S = 512
PAD = 16  # padding around tile for blur-safe edge handling
TEX = "game/gui/tex"

# palette (README 5.2)
PAPER = (0xE7, 0xDC, 0xC2)
PAPER_EDGE = (0xD3, 0xC1, 0x9C)
PAPER_DEEP = (0xBF, 0xA8, 0x7F)
WOOD_DARK = (0x2C, 0x1D, 0x13)
WOOD_MID = (0x3D, 0x2A, 0x1C)
WOOD_LIGHT = (0x51, 0x3A, 0x26)
INK = (0x3A, 0x2A, 0x1D)


def shifted_stamp(layer_draw_fn):
    """Call draw_fn(draw, ox, oy) 9 times so the element wraps seamlessly."""
    for ox in (-S, 0, S):
        for oy in (-S, 0, S):
            layer_draw_fn(ox, oy)


def make_parchment(seed=7):
    rnd = random.Random(seed)
    base = Image.new("RGBA", (S, S), PAPER + (255,))

    # --- per-pixel noise (spatially uncorrelated -> inherently seamless) ---
    noise = Image.effect_noise((S, S), 22).convert("L")
    dark = Image.new("RGBA", (S, S), (0x6B, 0x55, 0x33, 0))
    dark.putalpha(noise.point(lambda v: int(v * 25 / 128)))  # peak alpha ~25
    base = Image.alpha_composite(base, dark)

    # --- fibers on padded transparent layer, stamped 9x ---
    lay = Image.new("RGBA", (S + 2 * PAD, S + 2 * PAD), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    def stamp(fn):
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                fn(ox, oy)

    for _ in range(rnd.randint(40, 60)):
        # parameters drawn ONCE, then the same element stamped 9x
        x0 = rnd.uniform(0, S) + PAD
        y0 = rnd.uniform(0, S) + PAD
        ang = rnd.uniform(0, 2 * math.pi)
        ln = rnd.uniform(40, 200)
        a = rnd.randint(20, 40)
        w = rnd.choice([1, 1, 2])
        x1 = x0 + math.cos(ang) * ln
        y1 = y0 + math.sin(ang) * ln

        def fiber(ox, oy, x0=x0, y0=y0, x1=x1, y1=y1, a=a, w=w):
            d.line([x0 + ox, y0 + oy, x1 + ox, y1 + oy],
                   fill=PAPER_EDGE + (a,), width=w)
        stamp(fiber)
    lay = lay.filter(ImageFilter.GaussianBlur(1))
    base = Image.alpha_composite(base, lay.crop((PAD, PAD, PAD + S, PAD + S)))

    # --- radial stains, 9x stamped ---
    lay2 = Image.new("RGBA", (S + 2 * PAD, S + 2 * PAD), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(lay2)

    for _ in range(rnd.randint(6, 10)):
        cx = rnd.uniform(0, S) + PAD
        cy = rnd.uniform(0, S) + PAD
        rx = rnd.uniform(25, 90)
        ry = rx * rnd.uniform(0.55, 1.0)
        peak = rnd.randint(12, 25)
        steps = 14

        def stain(ox, oy, cx=cx, cy=cy, rx=rx, ry=ry, peak=peak, steps=steps):
            for i in range(steps, 0, -1):
                f = i / steps
                a = int(peak * (1 - f) ** 2)
                d2.ellipse([cx - rx * f + ox, cy - ry * f + oy,
                            cx + rx * f + ox, cy + ry * f + oy],
                           fill=PAPER_DEEP + (a,))
        shifted_stamp(stain)
    base = Image.alpha_composite(base, lay2.crop((PAD, PAD, PAD + S, PAD + S)))

    # --- periodic vignette: darkens toward tile edges, identical on both
    # sides of each seam so 2x2 tiling stays continuous ---
    # --- vignette: kept almost invisible (0.988 floor) because any darker
    # edge band repeats with the tile and reads as a grid on full-screen
    # backgrounds; real darkening is drawn per-asset instead ---
    depth = 0.012
    band = 28
    lut = []
    for i in range(S):
        dist = min(i, S - 1 - i)
        if dist >= band:
            lut.append(1.0)
        else:
            t = 1.0 - dist / band
            lut.append(1.0 - depth * t * t * (3 - 2 * t))  # smoothstep
    gray = Image.new("L", (S, S), 255)
    gp = gray.load()
    for y in range(S):
        for x in range(S):
            m = min(lut[x], lut[y])
            gp[x, y] = int(255 * m)
    rgb = base.convert("RGB")
    rgb = ImageChops.multiply(rgb, Image.merge("RGB", (gray, gray, gray)))
    out = Image.new("RGBA", (S, S))
    out.paste(rgb, (0, 0))
    return out


def periodic_noise_fn(seed, harmonics=6, decay=1.0):
    rnd = random.Random(seed)
    terms = [(rnd.uniform(0.4, 1.0) / (k + 1) ** decay,
              rnd.uniform(0, 2 * math.pi), k + 1)
             for k in range(harmonics)]
    amp = sum(a for a, _, _ in terms)

    def f(y):
        v = 0.0
        for a, ph, k in terms:
            v += a * math.sin(2 * math.pi * k * y / S + ph)
        return v / amp  # ~[-1,1]
    return f


def make_wood(seed=21):
    """
    Old dark oak: nearly straight vertical grain lines that wander slowly,
    built as contours of  sin(2*pi*k*x/S + A*noise2d(x,y))  where noise2d is
    a sum of integer-harmonic plane waves (k*2pi/512 in BOTH axes) -> the
    tile is mathematically seamless in x and y.  Contrast is asymmetric:
    mostly mid wood, thin dark lines, faint light fibres (no zebra bands).
    """
    rnd = random.Random(seed)
    two_pi = 2 * math.pi
    # 2D periodic noise: small x-harmonics (slow wander across columns),
    # moderate y-harmonics (gentle meander along the grain)
    terms = []
    for _ in range(16):
        k = rnd.randint(0, 2)
        l = rnd.randint(1, 5)
        terms.append((rnd.uniform(0.3, 1.0) / l ** 0.5, k, l,
                      rnd.uniform(0, two_pi)))
    amp = sum(t[0] for t in terms)

    def noise2d(x, y):
        v = 0.0
        for a, k, l, ph in terms:
            v += a * math.sin(two_pi * (k * x + l * y) / S + ph)
        return v / amp

    k_main = 6          # ~6 grain periods per 512 px -> lines every ~85 px
    k_fine = 17         # secondary thinner fibres
    px, md, lt = WOOD_DARK, WOOD_MID, WOOD_LIGHT
    img = Image.new("RGB", (S, S))
    data = []
    fm = two_pi * k_main / S
    ff = two_pi * k_fine / S
    jr = random.Random(seed + 5)
    for y in range(S):
        for x in range(S):
            n = noise2d(x, y)
            u = math.sin(fm * x + 1.6 * n) + 0.3 * math.sin(ff * x - 1.1 * n)
            u = max(-1.3, min(1.3, u)) / 1.3
            j = jr.uniform(-2.5, 2.5)
            if u > 0.80:                      # thin dark ink-like grain line
                f = min(1.0, (u - 0.80) / 0.25) ** 0.8
                c = tuple(int(md[i] + (px[i] - md[i]) * f) for i in range(3))
            elif u < -0.85:                   # faint raised fibre
                f = min(1.0, (-u - 0.85) / 0.30) * 0.5
                c = tuple(int(md[i] + (lt[i] - md[i]) * f) for i in range(3))
            else:                             # mid wood body, soft shading
                base = 0.30 + 0.10 * u
                c = tuple(int(px[i] + (lt[i] - px[i]) * base)
                          for i in range(3))
            c = tuple(max(0, min(255, int(v + j))) for v in c)
            data.append(c)
    img.putdata(data)

    out = img.convert("RGBA")

    # --- 2-3 long cracks, alpha 60, stamped 9x; drift removed so the
    # polyline start/end line up across the horizontal seam ---
    lay = Image.new("RGBA", (S + 2 * PAD, S + 2 * PAD), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cracks = []
    for _ in range(rnd.randint(2, 3)):
        x0 = rnd.uniform(0, S)
        pts = []
        x = x0
        for y in range(0, S + 1, 16):
            x += rnd.uniform(-4, 4)
            pts.append([x, y])
        drift = (pts[-1][0] - x0) / (S / 16)
        for i, p in enumerate(pts):
            p[0] -= drift * i
        pts[-1][0] = pts[0][0]
        cracks.append(pts)

    def draw_crack(pts):
        def fn(ox, oy):
            d.line([(p[0] + PAD + ox, p[1] + PAD + oy) for p in pts],
                   fill=(0x14, 0x0C, 0x07, 60), width=1)
        shifted_stamp(fn)

    for pts in cracks:
        draw_crack(pts)
    out = Image.alpha_composite(out, lay.crop((PAD, PAD, PAD + S, PAD + S)))

    # --- vignette: near-invisible for the same reason as parchment
    # (any edge band repeats with the tile and reads as a grid) ---
    depth = 0.012
    band = 36
    lut = []
    for i in range(S):
        dist = min(i, S - 1 - i)
        if dist >= band:
            lut.append(1.0)
        else:
            t = 1.0 - dist / band
            lut.append(1.0 - depth * t * t * (3 - 2 * t))
    gray = Image.new("L", (S, S))
    gp = gray.load()
    for y in range(S):
        for x in range(S):
            gp[x, y] = int(255 * min(lut[x], lut[y]))
    rgb = out.convert("RGB")
    rgb = ImageChops.multiply(rgb, Image.merge("RGB", (gray, gray, gray)))
    o2 = Image.new("RGBA", (S, S))
    o2.paste(rgb, (0, 0))
    return o2


def make_rule():
    # double ink line: 2 px line, 4 px gap, 2 px line -> 8 px tall
    w, h = 512, 8
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, 1], fill=INK + (255,))
    d.rectangle([0, 6, w - 1, 7], fill=INK + (255,))
    return im


if __name__ == "__main__":
    import os
    os.makedirs(TEX, exist_ok=True)
    p = make_parchment()
    p.save(f"{TEX}/parchment.png")
    print("parchment", p.size, p.mode)
    w = make_wood()
    w.save(f"{TEX}/wood.png")
    print("wood", w.size, w.mode)
    r = make_rule()
    r.save(f"{TEX}/rule.png")
    print("rule", r.size, r.mode)
