# -*- coding: utf-8 -*-
"""
Self-check for the medieval GUI (no Ren'Py window):
1) every file referenced by gui.rpy exists and matches the README 5.4 size
   table to the pixel;
2) 9-slice edge bands are uniform along the stretch axis;
3) Pillow mockups at real size: dialog (textbox+namebox+text), choices,
   main menu, save slots, preferences widgets -> saved to tools/gui_previews.
"""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = Path(".")
G = ROOT / "game" / "gui"
OUT = ROOT / "tools" / "gui_previews"
OUT.mkdir(parents=True, exist_ok=True)

FONT_R = "game/fonts/OldStandard-Regular.ttf"
FONT_B = "game/fonts/OldStandard-Bold.ttf"
INK = "#241811"
ACCENT = "#7b2f22"

# README 5.4 table
SIZES = {
    "main_menu.png": (1920, 1080), "game_menu.png": (1920, 1080),
    "overlay/main_menu.png": (1920, 1080),
    "overlay/game_menu.png": (1920, 1080),
    "overlay/confirm.png": (1920, 1080),
    "textbox.png": (1920, 277), "namebox.png": (450, 54),
    "frame.png": (900, 375), "notify.png": (1383, 64), "skip.png": (360, 64),
    "nvl.png": (1920, 1080), "bubble.png": (200, 155),
    "thoughtbubble.png": (200, 133),
    "button/choice_idle_background.png": (1185, 52),
    "button/choice_hover_background.png": (1185, 52),
    "button/idle_background.png": (450, 49),
    "button/hover_background.png": (450, 49),
    "button/quick_idle_background.png": (150, 45),
    "button/quick_hover_background.png": (150, 45),
    "button/slot_idle_background.png": (414, 309),
    "button/slot_hover_background.png": (414, 309),
    "button/check_foreground.png": (105, 49),
    "button/check_hover_foreground.png": (105, 49),
    "button/check_selected_foreground.png": (105, 49),
    "button/check_selected_hover_foreground.png": (105, 49),
    "button/radio_foreground.png": (105, 49),
    "button/radio_hover_foreground.png": (105, 49),
    "button/radio_selected_foreground.png": (105, 49),
    "button/radio_selected_hover_foreground.png": (105, 49),
    "bar/left.png": (525, 38), "bar/right.png": (525, 38),
    "bar/top.png": (38, 525), "bar/bottom.png": (38, 525),
    "slider/horizontal_idle_bar.png": (525, 38),
    "slider/horizontal_hover_bar.png": (525, 38),
    "slider/horizontal_idle_thumb.png": (15, 38),
    "slider/horizontal_hover_thumb.png": (15, 38),
    "slider/vertical_idle_bar.png": (38, 525),
    "slider/vertical_hover_bar.png": (38, 525),
    "slider/vertical_idle_thumb.png": (38, 15),
    "slider/vertical_hover_thumb.png": (38, 15),
    "scrollbar/horizontal_idle_bar.png": (1050, 18),
    "scrollbar/horizontal_hover_bar.png": (1050, 18),
    "scrollbar/horizontal_idle_thumb.png": (1050, 18),
    "scrollbar/horizontal_hover_thumb.png": (1050, 18),
    "scrollbar/vertical_idle_bar.png": (18, 1050),
    "scrollbar/vertical_hover_bar.png": (18, 1050),
    "scrollbar/vertical_idle_thumb.png": (18, 1050),
    "scrollbar/vertical_hover_thumb.png": (18, 1050),
    "window_icon.png": (250, 250),
    "tex/parchment.png": (512, 512), "tex/wood.png": (512, 512),
}

errors = []

# ---- 1) sizes + RGBA mode
for rel, size in SIZES.items():
    p = G / rel
    if not p.exists():
        errors.append(f"MISSING {rel}")
        continue
    with Image.open(p) as im:
        if im.size != size:
            errors.append(f"SIZE {rel}: {im.size} != {size}")
        if im.mode != "RGBA":
            errors.append(f"MODE {rel}: {im.mode}")

# ---- 1b) opaque surfaces: no alpha holes (task #6.1 regression)
# plain ImageDraw with alpha REPLACES pixel alpha; shadows must be composited.
for rel in ("textbox.png", "nvl.png", "main_menu.png", "game_menu.png"):
    im = Image.open(ROOT / "game" / "gui" / rel).convert("RGBA")
    lo = im.getchannel("A").getextrema()[0]
    if lo != 255:
        errors.append(f"ALPHA {rel}: min alpha {lo} != 255 (transparent hole)")

# ---- 2) gui.rpy referenced files exist
txt = (ROOT / "game" / "gui.rpy").read_text(encoding="utf-8")
refs = set(re.findall(r'"((?:gui|fonts)/[^"]+\.ttf|(?:gui|fonts)/[^"]+\.png)"', txt))
for r in sorted(refs):
    if "[prefix_]" in r:
        continue
    if not (ROOT / "game" / r).exists():
        errors.append(f"gui.rpy ref missing on disk: game/{r}")
# [prefix_] templates: Ren'Py falls back to the no-prefix name, so only the
# base file is required (original project shipped only idle/selected anyway)
for pat in set(re.findall(r'"(gui/[^"]*\[prefix_\][^"]*\.png)"', txt)):
    base = pat.replace("[prefix_]", "")
    if not (ROOT / "game" / base).exists():
        errors.append(f"gui.rpy template base missing: game/{base}")

# ---- 3) 9-slice band uniformity (ring constant along stretch axis)
def band_check(rel, t, axis_tol=3):
    im = Image.open(G / rel).convert("RGBA")
    w, h = im.size
    px = im.load()
    import statistics
    def dev(cols):
        vals = []
        for c in cols:
            vals.append(sum(v for v in c) / len(c))
        return max(vals) - min(vals)
    # top band: average color per column
    top = [[px[x, y] for y in range(t) for _ in (0,)] for x in range(t, w - t)]
    top = [[sum(px[x, y][k] for y in range(t) for k in range(4)) / (t * 4)
            for x in range(t, w - t)]]
    if top[0] and (max(top[0]) - min(top[0])) > axis_tol:
        errors.append(f"BAND {rel}: top band varies {max(top[0])-min(top[0]):.1f}")

for rel, t in [("namebox.png", 5), ("frame.png", 6), ("notify.png", 8),
               ("skip.png", 8), ("button/choice_idle_background.png", 8),
               ("button/choice_hover_background.png", 8),
               ("button/idle_background.png", 6),
               ("button/hover_background.png", 6),
               ("button/slot_idle_background.png", 15),
               ("button/slot_hover_background.png", 15)]:
    band_check(rel, t)

# ---- 4) mockups
def paste_center(dst, src, x, y):
    dst.paste(src, (x - src.width // 2, y - src.height // 2), src)

# dialog mock: real scene bg (read-only) + textbox + namebox + text
try:
    scene = Image.open("game/images/bg/maryino_terrace.png").convert("RGBA")
    scene = scene.resize((1920, 1080))
except Exception:
    scene = Image.new("RGBA", (1920, 1080), (60, 70, 60, 255))
tb = Image.open(G / "textbox.png").convert("RGBA")
scene.alpha_composite(tb, (0, 1080 - 277))
nb = Image.open(G / "namebox.png").convert("RGBA")
nb_big = nb.resize((450, 54))
scene.alpha_composite(nb_big, (360 - 5, 1080 - 277 - 2))
d = ImageDraw.Draw(scene)
d.text((360 + 24, 1080 - 277 + 4), "Базаров", font=ImageFont.truetype(FONT_B, 44),
       fill=INK)
f34 = ImageFont.truetype(FONT_R, 34)
d.text((402, 1080 - 277 + 75),
       "Май 1859 года. Солнце уже клонится к закату, но всё ещё\n"
       "жжёт пыльную большую дорогу.", font=f34, fill=INK)
scene.convert("RGB").save(OUT / "mock_dialog.png")

# choices mock
bg = Image.open(G / "main_menu.png").convert("RGBA")
ov = Image.open(G / "overlay/game_menu.png").convert("RGBA")
bg.alpha_composite(ov)
ci = Image.open(G / "button/choice_idle_background.png").convert("RGBA")
ch = Image.open(G / "button/choice_hover_background.png").convert("RGBA")
fch = ImageFont.truetype(FONT_R, 34)
y = 420
for i, (btn, label) in enumerate([(ci, "Откуда вы?"),
                                  (ch, "Почему же вы думаете, что я с кем-то ехал?"),
                                  (ci, "А вы, я думаю, доктор, и доктор молодой.")]):
    bg.alpha_composite(btn, (367, y))
    bb = d.textbbox((0, 0), label, font=fch) if False else ImageDraw.Draw(bg).textbbox((0, 0), label, font=fch)
    ImageDraw.Draw(bg).text((367 + (1185 - bb[2] + bb[0]) / 2, y + 9),
                            label, font=fch, fill=ACCENT if btn is ch else "#4a382a")
    y += 85
bg.convert("RGB").save(OUT / "mock_choices.png")

# main menu mock: bg + overlay + nav text + title
mm = Image.open(G / "main_menu.png").convert("RGBA")
mo = Image.open(G / "overlay/main_menu.png").convert("RGBA")
mm.alpha_composite(mo)
dm = ImageDraw.Draw(mm)
fn = ImageFont.truetype(FONT_R, 32)
ft = ImageFont.truetype(FONT_B, 104)
nav = ["Начать игру", "Загрузить", "Настройки", "Галерея", "Музыка",
       "Об игре", "Справка", "Выйти"]
yy = 140
for item in nav:
    dm.text((100, yy), item, font=fn, fill=INK)
    yy += 52
t = "Отцы и дети"
bb = dm.textbbox((0, 0), t, font=ft)
dm.text((1860 - (bb[2] - bb[0]), 900), t, font=ft, fill=INK)
dm.text((1860 - 120, 1010), "1.3", font=fn, fill="#4a382a")
mm.convert("RGB").save(OUT / "mock_main_menu.png")

# saves mock
sm = Image.open(G / "game_menu.png").convert("RGBA")
si = Image.open(G / "button/slot_idle_background.png").convert("RGBA")
sh = Image.open(G / "button/slot_hover_background.png").convert("RGBA")
fs = ImageFont.truetype(FONT_R, 21)
for row in range(2):
    for col in range(3):
        btn = sh if (row, col) == (0, 1) else si
        x = 165 + col * 429
        y = 160 + row * 324
        sm.alpha_composite(btn, (x, y))
        dd = ImageDraw.Draw(sm)
        dd.text((x + 207 - 40, y + 275), "Пт 30 окт. 2026", font=fs,
                fill="#6d5a45")
sm.convert("RGB").save(OUT / "mock_saves.png")

# widgets strip: sliders, bars, scrollbars, check/radio, notify, skip, quick
strip = Image.new("RGBA", (1200, 700), (0, 0, 0, 0))
strip.alpha_composite(Image.open(G / "frame.png").convert("RGBA"), (20, 20))
def put(rel, x, y):
    strip.alpha_composite(Image.open(G / rel).convert("RGBA"), (x, y))
put("slider/horizontal_idle_bar.png", 60, 60)
put("slider/horizontal_idle_thumb.png", 300, 60)
put("slider/horizontal_hover_bar.png", 60, 110)
put("slider/horizontal_hover_thumb.png", 420, 110)
put("bar/left.png", 60, 165)
put("bar/right.png", 60, 210)
# partial filled bar mock
strip.alpha_composite(Image.open(G / "bar/right.png").convert("RGBA"), (600, 165))
lf = Image.open(G / "bar/left.png").convert("RGBA").crop((0, 0, 300, 38))
strip.alpha_composite(lf, (600, 165))
put("scrollbar/horizontal_idle_bar.png", 60, 260)
strip.alpha_composite(Image.open(G / "scrollbar/horizontal_idle_thumb.png")
                      .convert("RGBA").crop((0, 0, 350, 18)), (60, 260))
put("button/check_foreground.png", 60, 310)
put("button/check_selected_foreground.png", 100, 310)
put("button/radio_foreground.png", 150, 310)
put("button/radio_selected_foreground.png", 190, 310)
put("button/quick_idle_background.png", 240, 310)
put("button/quick_hover_background.png", 400, 310)
put("notify.png", 20, 400)
put("skip.png", 20, 480)
put("bubble.png", 900, 310)
put("thoughtbubble.png", 1050, 310)
put("window_icon.png", 900, 480)
paper = Image.new("RGBA", (1200, 700), (231, 220, 194, 255))
paper.alpha_composite(strip)
paper.convert("RGB").save(OUT / "mock_widgets.png")

# 2x2 tiles
for name in ("parchment", "wood"):
    t = Image.open(G / f"tex/{name}.png").convert("RGBA")
    g = Image.new("RGBA", (1024, 1024))
    for x in range(2):
        for y in range(2):
            g.paste(t, (x * 512, y * 512))
    g.save(OUT / f"tile_{name}_2x2.png")

print("ERRORS:" if errors else "ALL CHECKS PASSED")
for e in errors:
    print(" -", e)
