# -*- coding: utf-8 -*-
"""
Redraw ALL medieval GUI assets (README-AI.md section 5.4).
Sizes are FIXED - they match the table and the Frame borders in screens.rpy.
Palette is strictly README 5.2. No gold, no gloss, no neon.
Textures come from game/gui/tex/ (gen_textures.py).
"""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

G = "game/gui"
TEX = G + "/tex"
FONT_DIR = "game/fonts"

# --- palette (README 5.2) ---
PAPER = "#e7dcc2"
EDGE = "#d3c19c"
DEEP = "#bfa87f"
WOOD_DARK = "#2c1d13"
WOOD_MID = "#3d2a1c"
WOOD_LIGHT = "#513a26"
INK = "#241811"          # main text ink
INK2 = "#4a382a"         # secondary ink
RULE = "#3a2a1d"         # ink rule color (5.3)
MUTED = "#6d5a45"
ACCENT = "#7b2f22"       # cinnabar
ACCENT_H = "#5c1f15"

# rgb triples for alpha-composited drawing (PIL: hex string + alpha tuple)
DEEP_RGB = (0xBF, 0xA8, 0x7F)
WOOD_DARK_RGB = (0x2C, 0x1D, 0x13)
CONFIRM_RGB = (0x1B, 0x12, 0x0C)

PARCH = Image.open(TEX + "/parchment.png").convert("RGBA")
WOOD = Image.open(TEX + "/wood.png").convert("RGBA")


def paper_bg(w, h, ox=0, oy=0):
    im = Image.new("RGBA", (w, h))
    for x in range(-1, w // 512 + 2):
        for y in range(-1, h // 512 + 2):
            im.paste(PARCH, (x * 512 + ox, y * 512 + oy))
    return im.crop((0, 0, w, h)) if (ox or oy) else im


def wood_bg(w, h, ox=0, oy=0):
    im = Image.new("RGBA", (w, h))
    for x in range(-1, w // 512 + 2):
        for y in range(-1, h // 512 + 2):
            im.paste(WOOD, (x * 512 + ox, y * 512 + oy))
    return im.crop((0, 0, w, h))


def solid(w, h, color):
    return Image.new("RGBA", (w, h), color)


def ink_box(im, x0, y0, x1, y1, lw=2, color=RULE):
    """2px double-line-safe box drawn with explicit rectangles (no AA)."""
    d = ImageDraw.Draw(im)
    d.rectangle([x0, y0, x1, y0 + lw - 1], fill=color)          # top
    d.rectangle([x0, y1 - lw + 1, x1, y1], fill=color)          # bottom
    d.rectangle([x0, y0 + lw, x0 + lw - 1, y1 - lw], fill=color)   # left
    d.rectangle([x1 - lw + 1, y0 + lw, x1, y1 - lw], fill=color)   # right


def double_ink_box(im, inset=6, lw=2, gap=4, color=RULE):
    w, h = im.size
    ink_box(im, inset, inset, w - 1 - inset, h - 1 - inset, lw, color)
    i2 = inset + lw + gap
    if h - 1 - i2 > i2:
        ink_box(im, i2, i2, w - 1 - i2, h - 1 - i2, lw, color)


def darken(im, f=0.93):
    """Brightness multiply on RGB only (keep alpha)."""
    r, g, b, a = im.split()
    r = r.point(lambda v: int(v * f))
    g = g.point(lambda v: int(v * f))
    b = b.point(lambda v: int(v * f))
    return Image.merge("RGBA", (r, g, b, a))


def save(im, path):
    im.save(path)
    print("OK", path, im.size)


def ring(im, t, color=EDGE):
    """Solid uniform border ring t px thick - the 9-slice safe edge."""
    w, h = im.size
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, t - 1], fill=color)
    d.rectangle([0, h - t, w - 1, h - 1], fill=color)
    d.rectangle([0, 0, t - 1, h - 1], fill=color)
    d.rectangle([w - t, 0, w - 1, h - 1], fill=color)


# ---------------------------------------------------------------- panels
def panel_paper(w, h, ring_t, dbl=True, inset=None, ox=0, oy=0):
    """Parchment panel: textured center, uniform ring, double ink rule."""
    im = paper_bg(w, h, ox, oy)
    ring(im, ring_t)
    if inset is None:
        inset = max(2, ring_t // 2 - 1)     # rule sits INSIDE the ring band
    ink_box(im, inset, inset, w - 1 - inset, h - 1 - inset, 2, RULE)
    if dbl:
        i2 = inset + 6                       # 2px line + 4px gap + 2px line
        if min(w, h) > 2 * i2 + 6:
            ink_box(im, i2, i2, w - 1 - i2, h - 1 - i2, 2, RULE)
    return im


def main():
    rnd = random.Random(11)
    off = lambda: (rnd.randint(0, 511), rnd.randint(0, 511))
    offk = lambda: {'ox': rnd.randint(0, 511), 'oy': rnd.randint(0, 511)}

    # ---------------- textbox 1920x277 (plain Image, no 9-slice)
    w, h = 1920, 277
    im = paper_bg(w, h, *off())
    d = ImageDraw.Draw(im)
    # 13 px dark wood "table edge" on top
    im.paste(wood_bg(w, 13), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 13, w - 1, 13], fill=WOOD_DARK)
    # double ink rule along the wood edge
    d.rectangle([0, 16, w - 1, 17], fill=RULE)
    d.rectangle([0, 22, w - 1, 23], fill=RULE)
    # soft inner shadow under the rule (#bfa87f a40 -> 0 over 30 px).
    # drawn on a transparent overlay + alpha_composite: a direct ImageDraw
    # line with alpha REPLACES pixel alpha and punches holes in the paper.
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(30):
        a = int(40 * (1 - i / 30))
        od.line([(0, 26 + i), (w - 1, 26 + i)], fill=DEEP_RGB + (a,), width=1)
    im = Image.alpha_composite(im, ov)
    d = ImageDraw.Draw(im)
    # bottom = screen edge: no border, just a hair of deep shade
    d.rectangle([0, h - 2, w - 1, h - 1], fill=EDGE)
    save(im, G + "/textbox.png")

    # ---------------- namebox 450x54, Borders(5,5,5,5)
    w, h = 450, 54
    im = panel_paper(w, h, 5, dbl=True, inset=1, ox=off()[0], oy=off()[1])
    d = ImageDraw.Draw(im)
    # vertical ink tick 3 px near the left edge
    d.rectangle([17, 14, 19, h - 15], fill=INK)
    save(im, G + "/namebox.png")

    # ---------------- frame 900x375, Borders(6,6,6,6)
    im = panel_paper(900, 375, 6, dbl=True, inset=2, **offk())
    save(im, G + "/frame.png")

    # ---------------- notify 1383x64, Borders(24,8,60,8)
    im = panel_paper(1383, 64, 8, dbl=False, inset=3, **offk())
    save(im, G + "/notify.png")

    # ---------------- skip 360x64, Borders(24,8,75,8)
    im = panel_paper(360, 64, 8, dbl=False, inset=3, **offk())
    save(im, G + "/skip.png")

    # ---------------- nvl 1920x1080, Borders(0,15,0,30)
    w, h = 1920, 1080
    im = paper_bg(w, h, *off())
    d = ImageDraw.Draw(im)
    # top band (15 px, stretched horizontally -> keep it flat-color)
    d.rectangle([0, 0, w - 1, 11], fill=WOOD_DARK)
    d.rectangle([0, 12, w - 1, 13], fill=RULE)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))  # see textbox alpha note
    od = ImageDraw.Draw(ov)
    for i in range(24):   # inner shadow below the band
        a = int(36 * (1 - i / 24))
        od.line([(0, 15 + i), (w - 1, 15 + i)], fill=DEEP_RGB + (a,))
    im = Image.alpha_composite(im, ov)
    d = ImageDraw.Draw(im)
    # bottom band (30 px)
    d.rectangle([0, h - 30, w - 1, h - 29], fill=RULE)
    d.rectangle([0, h - 26, w - 1, h - 1], fill=EDGE)
    save(im, G + "/nvl.png")

    # ---------------- bubbles (9-slice 55,55,55,95)
    def bubble(w, h, tail):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        body = paper_bg(w, h, *off())
        m = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(m)
        md.rounded_rectangle([2, 2, w - 3, h - (30 if tail else 3)],
                             radius=16, fill=255)
        if tail:
            md.polygon([(18, h - 34), (6, h - 3), (44, h - 24)], fill=255)
        im.paste(body, (0, 0), m)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([2, 2, w - 3, h - (30 if tail else 3)],
                            radius=16, outline=RULE, width=2)
        if tail:
            d.polygon([(18, h - 34), (6, h - 3), (44, h - 24)],
                      fill=None, outline=RULE, width=2)
        return im

    save(bubble(200, 155, True), G + "/bubble.png")

    # thoughtbubble 200x133: body + three trailing dots
    w, h = 200, 133
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    body = paper_bg(w, h, *off())
    m = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(m)
    md.rounded_rectangle([2, 2, w - 3, h - 14], radius=16, fill=255)
    md.ellipse([20, h - 20, 34, h - 6], fill=255)
    md.ellipse([8, h - 12, 16, h - 4], fill=255)
    im.paste(body, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, w - 3, h - 14], radius=16, outline=RULE, width=2)
    d.ellipse([20, h - 20, 34, h - 6], outline=RULE, width=2)
    d.ellipse([8, h - 12, 16, h - 4], outline=RULE, width=2)
    save(im, G + "/thoughtbubble.png")

    # ---------------- buttons
    def button(w, h, ring_t, inset, hover=False):
        im = panel_paper(w, h, ring_t, dbl=False, inset=inset, **offk())
        if hover:
            im = darken(im, 0.92)
            ink_box(im, inset, inset, w - 1 - inset, h - 1 - inset, 2, ACCENT)
        return im

    # choice 1185x52, Borders(150,8,150,8)
    save(button(1185, 52, 8, 3), G + "/button/choice_idle_background.png")
    save(button(1185, 52, 8, 3, True), G + "/button/choice_hover_background.png")
    # plain 450x49, Borders(6,6,6,6)
    save(button(450, 49, 6, 2), G + "/button/idle_background.png")
    save(button(450, 49, 6, 2, True), G + "/button/hover_background.png")

    # quick 150x45, Borders(15,6,15,0): open bottom edge
    def quick(hover=False):
        w, h = 150, 45
        im = paper_bg(w, h, *off())
        d = ImageDraw.Draw(im)
        # uniform bands: top 6 px; bottom 10 px flat paper-ish (border=0 ->
        # center stretches, keep bottom rows featureless)
        d.rectangle([0, 0, w - 1, 5], fill=EDGE)
        d.rectangle([0, 0, 5, h - 11], fill=EDGE)
        d.rectangle([w - 6, 0, w - 1, h - 11], fill=EDGE)
        d.rectangle([0, h - 10, w - 1, h - 1], fill=PAPER)
        col = ACCENT if hover else RULE
        d.rectangle([2, 2, w - 3, 3], fill=col)
        d.rectangle([2, 2, 3, h - 11], fill=col)
        d.rectangle([w - 4, 2, w - 3, h - 11], fill=col)
        if hover:
            im = darken(im, 0.92)
            d = ImageDraw.Draw(im)
            d.rectangle([2, 2, w - 3, 3], fill=ACCENT)
            d.rectangle([2, 2, 3, h - 11], fill=ACCENT)
            d.rectangle([w - 4, 2, w - 3, h - 11], fill=ACCENT)
        return im

    save(quick(), G + "/button/quick_idle_background.png")
    save(quick(True), G + "/button/quick_hover_background.png")

    # slot 414x309, Borders(15,15,15,15) - fixed size, free to decorate
    def slot(hover=False):
        w, h = 414, 309
        im = panel_paper(w, h, 15, dbl=True, inset=4, **offk())
        col = ACCENT if hover else RULE
        if hover:
            im = darken(im, 0.92)
            ink_box(im, 4, 4, w - 5, h - 5, 2, col)
            ink_box(im, 12, 12, w - 13, h - 13, 2, col)
        d = ImageDraw.Draw(im)
        # corner lozenges (ink diamonds) - static, decorative
        for cx, cy in [(22, 22), (w - 23, 22), (22, h - 23), (w - 23, h - 23)]:
            d.polygon([(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)],
                      fill=col)
        return im

    save(slot(), G + "/button/slot_idle_background.png")
    save(slot(True), G + "/button/slot_hover_background.png")

    # ---------------- check / radio foregrounds 105x49 (task #6.2)
    # Frame-as-Window semantics: a bare Image foreground keeps native size and
    # is anchored bottom-left; borders(78,0,27,0) => text occupies x0..77 and
    # the circle sits at x78..99 right behind it. Screens styles anchor the
    # foreground xalign=1.0, so the circle renders at the RIGHT edge of the
    # plate: [ text ... (o) ]. Left 78 px stay transparent for the text.
    WFG, HFG = 105, 49
    CX0, CY0, CX1, CY1 = 78, 14, 99, 35      # 21x21 circle box
    INK_C = "#3a2c1c"                         # ink outline per lead's note
    INK_C_H = "#54402a"                       # hover: slightly lighter ink
    WHITE = "#f2ecdc"                         # warm paper-white marker dot

    def fg_base():
        return Image.new("RGBA", (WFG, HFG), (0, 0, 0, 0))

    def fg_radio(kind):
        im = fg_base(); d = ImageDraw.Draw(im)
        if kind == "idle":
            d.ellipse([CX0, CY0, CX1, CY1], outline=INK_C, width=2)
        elif kind == "hover":
            d.ellipse([CX0, CY0, CX1, CY1], outline=INK_C_H, width=2)
        elif kind == "selected":
            d.ellipse([CX0, CY0, CX1, CY1], fill=ACCENT)
            d.ellipse([CX0, CY0, CX1, CY1], outline=RULE, width=1)
            d.ellipse([85, 21, 92, 28], fill=WHITE)
        else:  # selected_hover: same fill, brighter rim
            d.ellipse([CX0, CY0, CX1, CY1], fill=ACCENT)
            d.ellipse([CX0, CY0, CX1, CY1], outline=ACCENT_H, width=2)
            d.ellipse([85, 21, 92, 28], fill=WHITE)
        return im

    def fg_check(kind):
        im = fg_base(); d = ImageDraw.Draw(im)
        box = [CX0 + 1, CY0, CX1 - 1, CY1]
        col = {"idle": INK_C, "hover": INK_C_H}.get(kind, RULE)
        if kind in ("idle", "hover"):
            d.rectangle(box, outline=col, width=2)
        else:
            d.rectangle(box, fill=ACCENT)
            d.line([(CX0 + 5, 26), (CX0 + 9, 31), (CX1 - 4, 18)],
                   fill=WHITE, width=3, joint="curve")
        return im

    for kind, suffix in [("idle", ""), ("hover", "_hover"),
                         ("selected", "_selected"),
                         ("selected_hover", "_selected_hover")]:
        save(fg_radio(kind), G + "/button/radio%s_foreground.png" % suffix)
        save(fg_check(kind), G + "/button/check%s_foreground.png" % suffix)

    # ---------------- bars 525x38 / 38x525, Borders(6,6,6,6)
    def hbar_filled():
        w, h = 525, 38
        im = solid(w, h, ACCENT)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, 1], fill=ACCENT_H)
        d.rectangle([0, h - 2, w - 1, h - 1], fill=ACCENT_H)
        ink_box(im, 0, 0, w - 1, h - 1, 2, INK)
        # subtle fibre speckle, still cinnabar-family
        for _ in range(240):
            x, y = rnd.randint(3, w - 4), rnd.randint(3, h - 4)
            d.point((x, y), fill=ACCENT_H)
        return im

    def hbar_muted():
        w, h = 525, 38
        im = solid(w, h, EDGE)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, 1], fill=DEEP)
        d.rectangle([0, h - 2, w - 1, h - 1], fill=DEEP)
        ink_box(im, 0, 0, w - 1, h - 1, 2, RULE)
        return im

    lf = hbar_filled(); rt = hbar_muted()
    save(lf, G + "/bar/left.png")
    save(rt, G + "/bar/right.png")
    save(lf.transpose(Image.ROTATE_90), G + "/bar/top.png")
    save(rt.transpose(Image.ROTATE_90), G + "/bar/bottom.png")

    # ---------------- sliders 525x38 bar / 15x38 thumb
    def slider_bar(hover=False):
        w, h = 525, 38
        im = solid(w, h, EDGE)
        d = ImageDraw.Draw(im)
        col = ACCENT if hover else RULE
        d.rectangle([0, 2, w - 1, 3], fill=col)          # in top band
        d.rectangle([0, h - 4, w - 1, h - 3], fill=col)  # in bottom band
        d.rectangle([0, 16, w - 1, 21], fill=DEEP)       # groove (center)
        return im

    def slider_thumb(hover=False):
        w, h = 15, 38
        im = solid(w, h, WOOD_MID)
        d = ImageDraw.Draw(im)
        edge = ACCENT if hover else WOOD_DARK
        d.rectangle([0, 0, w - 1, 1], fill=edge)
        d.rectangle([0, h - 2, w - 1, h - 1], fill=edge)
        d.rectangle([0, 0, 1, h - 1], fill=edge)
        d.rectangle([w - 2, 0, w - 1, h - 1], fill=edge)
        d.rectangle([6, 4, 8, h - 5], fill=WOOD_LIGHT)   # grain highlight
        return im

    hb = slider_bar(False); hh = slider_bar(True)
    tb = slider_thumb(False); th = slider_thumb(True)
    save(hb, G + "/slider/horizontal_idle_bar.png")
    save(hh, G + "/slider/horizontal_hover_bar.png")
    save(tb, G + "/slider/horizontal_idle_thumb.png")
    save(th, G + "/slider/horizontal_hover_thumb.png")
    save(hb.transpose(Image.ROTATE_90), G + "/slider/vertical_idle_bar.png")
    save(hh.transpose(Image.ROTATE_90), G + "/slider/vertical_hover_bar.png")
    save(tb.transpose(Image.ROTATE_90), G + "/slider/vertical_idle_thumb.png")
    save(th.transpose(Image.ROTATE_90), G + "/slider/vertical_hover_thumb.png")

    # ---------------- scrollbars 1050x18 / thumb same size
    def sb_bar(hover=False):
        w, h = 1050, 18
        im = solid(w, h, EDGE)
        d = ImageDraw.Draw(im)
        col = ACCENT if hover else RULE
        d.rectangle([0, 3, w - 1, 3], fill=col)
        d.rectangle([0, h - 4, w - 1, h - 4], fill=col)
        d.rectangle([0, 8, w - 1, 9], fill=DEEP)
        return im

    def sb_thumb(hover=False):
        w, h = 1050, 18
        im = solid(w, h, INK2 if not hover else ACCENT_H)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, 1], fill=INK)
        d.rectangle([0, h - 2, w - 1, h - 1], fill=INK)
        d.rectangle([2, 7, w - 3, 10], fill=MUTED)
        return im

    b = sb_bar(False); bh = sb_bar(True)
    t = sb_thumb(False); tth = sb_thumb(True)
    save(b, G + "/scrollbar/horizontal_idle_bar.png")
    save(bh, G + "/scrollbar/horizontal_hover_bar.png")
    save(t, G + "/scrollbar/horizontal_idle_thumb.png")
    save(tth, G + "/scrollbar/horizontal_hover_thumb.png")
    save(b.transpose(Image.ROTATE_90), G + "/scrollbar/vertical_idle_bar.png")
    save(bh.transpose(Image.ROTATE_90), G + "/scrollbar/vertical_hover_bar.png")
    save(t.transpose(Image.ROTATE_90), G + "/scrollbar/vertical_idle_thumb.png")
    save(tth.transpose(Image.ROTATE_90), G + "/scrollbar/vertical_hover_thumb.png")

    # ---------------- menu backgrounds 1920x1080
    def menu_bg(path, seed):
        r2 = random.Random(seed)
        w, h = 1920, 1080
        im = wood_bg(w, h, r2.randint(0, 511), r2.randint(0, 511))
        # parchment sheet, 60 px margin, drop shadow 6/18/a90
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.rectangle([60 + 6, 60 + 6, w - 61 + 6, h - 61 + 6],
                     fill=(0, 0, 0, 90))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        im = Image.alpha_composite(im, sh)
        sheet = paper_bg(w - 120, h - 120, r2.randint(0, 511), r2.randint(0, 511))
        # sheet inner shadow near its own edges (aged look), overlay-composited
        # so pixel alpha stays 255 (plain ImageDraw would punch holes)
        sov = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
        sd2 = ImageDraw.Draw(sov)
        for i in range(18):
            a = int(26 * (1 - i / 18))
            sd2.rectangle([i, i, sheet.width - 1 - i, sheet.height - 1 - i],
                          outline=DEEP_RGB + (a,))
        sheet = Image.alpha_composite(sheet, sov)
        im.paste(sheet, (60, 60))
        d = ImageDraw.Draw(im)
        # double ink frame on the sheet
        d.rectangle([60, 60, w - 61, h - 61], outline=RULE, width=2)
        ink_box(im, 78, 78, w - 79, h - 79, 2, RULE)
        ink_box(im, 86, 86, w - 87, h - 87, 2, RULE)
        save(im, path)

    menu_bg(G + "/main_menu.png", 101)
    menu_bg(G + "/game_menu.png", 202)

    # ---------------- overlays 1920x1080
    w, h = 1920, 1080

    def nav_wash(path):
        """Затенение ТОЛЬКО под левой колонкой навигации.

        Рамки main_menu_frame / game_menu_outer_frame рисуют этот PNG 1:1 на
        весь экран, поэтому форма затемнения задаётся здесь, а не размером
        рамки. Ранее ложились равномерной тонировкой на весь пергаментный
        лист: в главном меню лист темнел до #887b68 (цитаты 3.6:1, название
        2.5:1), в игровом меню колонки настроек падали до 2.7:1.
        """
        im = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(im)
        for x in range(w):
            if x <= 380:
                a = 125
            elif x < 460:
                a = int(125 * (460 - x) / 80)
            else:
                a = 0
            if a:
                d.line([(x, 0), (x, h - 1)], fill=WOOD_DARK_RGB + (a,))
        save(im, path)

    nav_wash(G + "/overlay/main_menu.png")
    nav_wash(G + "/overlay/game_menu.png")

    save(solid(w, h, CONFIRM_RGB + (150,)), G + "/overlay/confirm.png")

    # ---------------- window icon 250x250
    w, h = 250, 250
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    body = paper_bg(w, h, 7, 3)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([2, 2, w - 3, h - 3], radius=30, fill=255)
    im.paste(body, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, w - 3, h - 3], radius=30, outline=INK, width=3)
    d.rounded_rectangle([9, 9, w - 10, h - 10], radius=24, outline=RULE, width=2)
    f_big = ImageFont.truetype(FONT_DIR + "/OldStandard-Bold.ttf", 96)
    f_sm = ImageFont.truetype(FONT_DIR + "/OldStandard-Regular.ttf", 40)
    for ch, cx in (("О", 62), ("Д", 188)):
        bb = d.textbbox((0, 0), ch, font=f_big)
        d.text((cx - (bb[0] + bb[2]) / 2, 68), ch, font=f_big, fill=INK)
    d.text((125 - 14, 100), "и", font=f_sm, fill=ACCENT)
    d.rectangle([70, 196, 180, 198], fill=RULE)
    save(im, G + "/window_icon.png")


if __name__ == "__main__":
    main()
