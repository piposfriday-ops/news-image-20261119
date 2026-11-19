#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed coordinates, fixed colours, seeded star positions.
No network, no timestamps, no randomness outside the seeded generator.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (18, 38, 66)
GREY = (90, 88, 82)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def star(draw, cx, cy, r, fill):
    """Five-point star centred at (cx, cy)."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def panel(draw, box, title=None):
    """Thin black panel border."""
    draw.rectangle(box, outline=INK, width=2)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 14, W, 18], fill=RED)
mast = font(SERIF, 68)
d.text((W // 2, 24), "THE WORLD", font=mast, fill=INK, anchor="ma")
sub = font(SANS_B, 19)
d.text((W // 2, 96), "T H U R S D A Y,  1 9  N O V E M B E R  2 0 2 6", font=sub, fill=INK, anchor="ma")
d.rectangle([24, 126, W - 24, 129], fill=INK)
d.rectangle([24, 133, W - 24, 134], fill=INK)

# ---------------------------------------------------------------- lead: GTA VI
LX, LY, LW, LH = 24, 142, 976, 290
panel(d, [LX, LY, LX + LW, LY + LH])
AX, AY, AW, AH = LX + 2, LY + 2, 560, LH - 4  # art area
vgrad(d, [AX, AY, AX + AW, AY + AH], (255, 154, 61), (123, 75, 148))
# sun
d.ellipse([AX + 500, AY + 30, AX + 556, AY + 86], fill=(255, 214, 120))
# skyline silhouettes (back, lighter purple)
for bx, bw, bh in [(0, 70, 150), (80, 60, 190), (150, 80, 130), (240, 55, 175), (305, 75, 140), (390, 60, 185), (460, 90, 150)]:
    d.rectangle([AX + bx, AY + AH - 92 - bh, AX + bx + bw, AY + AH - 92], fill=(94, 52, 110))
# skyline silhouettes (front, dark)
for bx, bw, bh in [(20, 55, 95), (95, 70, 70), (180, 60, 110), (255, 80, 80), (350, 55, 100), (425, 70, 75), (505, 50, 90)]:
    d.rectangle([AX + bx, AY + AH - 92 - bh, AX + bx + bw, AY + AH - 92], fill=(52, 28, 68))
# lit windows
rng = random.Random(7)
for _ in range(46):
    bx = AX + rng.randint(8, AW - 14)
    by = AY + AH - 92 - rng.randint(10, 170)
    d.rectangle([bx, by, bx + 5, by + 7], fill=(255, 214, 120))
# palm trees
for px, ph in [(70, 70), (520, 84)]:
    d.line([(AX + px, AY + AH - 92), (AX + px + 8, AY + AH - 92 - ph)], fill=(38, 22, 50), width=5)
    for ang in (-70, -35, 0, 35, 70):
        import math
        a = math.radians(ang - 90)
        ex = AX + px + 8 + 34 * math.cos(a)
        ey = AY + AH - 92 - ph + 30 * math.sin(a)
        d.line([(AX + px + 8, AY + AH - 92 - ph), (ex, ey)], fill=(38, 22, 50), width=4)
# water
d.rectangle([AX, AY + AH - 92, AX + AW, AY + AH], fill=(30, 42, 84))
for wy in range(AY + AH - 84, AY + AH - 4, 12):
    d.line([(AX + 12, wy), (AX + AW - 12, wy)], fill=(255, 154, 61), width=2)
# neon sign on the water
neon = font(SANS_B, 34)
d.text((AX + AW // 2, AY + AH - 78), "VICE CITY", font=neon, fill=(255, 240, 180), anchor="ma",
       stroke_width=2, stroke_fill=(255, 80, 160))

# lead text (right of art)
TX = AX + AW + 22
d.text((TX, LY + 14), "CULTURE  ·  GAMING", font=font(SANS_B, 17), fill=RED)
y = LY + 44
for line in wrap(d, "VICE CITY OPENS ITS DOORS", font(SERIF, 40), 976 - (TX - LX) - 22):
    d.text((TX, y), line, font=font(SERIF, 40), fill=INK)
    y += 47
y += 8
for line in wrap(d, "Grand Theft Auto VI launches worldwide after a 13-year wait, as gamers enter Vice City.",
                 font(SANS, 20), 976 - (TX - LX) - 22):
    d.text((TX, y), line, font=font(SANS, 20), fill=(40, 40, 40))
    y += 27

# ---------------------------------------------------------------- row 2: two panels
RY, RH = 444, 258
# --- panel A: APEC trilateral
PX, PW = 24, 476
panel(d, [PX, RY, PX + PW, RY + RH])
ax, ay, aw, ah = PX + 2, RY + 2, PW - 4, 128
d.rectangle([ax, ay, ax + aw, ay + ah], fill=(214, 228, 240))
# table
d.rectangle([ax, ay + ah - 26, ax + aw, ay + ah], fill=(120, 72, 48))


def flag_us(x, y, w, h):
    for i in range(13):
        d.rectangle([x, y + i * h // 13, x + w, y + (i + 1) * h // 13],
                    fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 7 // 13], fill=(30, 50, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 6 + c * 13, y + 5 + r * 11, x + 9 + c * 13, y + 8 + r * 11], fill=(255, 255, 255))


def flag_cn(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(d, x + 16, y + 14, 10, (255, 222, 0))
    for sx, sy in [(34, 8), (40, 14), (40, 22), (34, 28)]:
        star(d, x + sx, y + sy, 4, (255, 222, 0))


def flag_ru(x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


for i, fn in enumerate([flag_us, flag_cn, flag_ru]):
    fx = ax + 52 + i * 140
    d.line([(fx + 34, ay + 14), (fx + 34, ay + ah - 26)], fill=(60, 60, 60), width=3)
    fn(fx, ay + 14, 68, 44)
d.text((PX + PW // 2, RY + 140), "TRUMP, XI & PUTIN", font=font(SERIF, 32), fill=INK, anchor="ma")
d.text((PX + PW // 2, RY + 178), "MEET IN SHENZHEN", font=font(SERIF, 32), fill=INK, anchor="ma")
for j, line in enumerate(wrap(d, "Trilateral talks open on the sidelines of the APEC summit.",
                              font(SANS, 17), PW - 36)):
    d.text((PX + 18, RY + 218 + j * 22), line, font=font(SANS, 17), fill=(40, 40, 40))

# --- panel B: US-Iran Gulf
QX, QW = 524, 476
panel(d, [QX, RY, QX + QW, RY + RH])
bx, by, bw, bh = QX + 2, RY + 2, QW - 4, 128
d.rectangle([bx, by, bx + bw, by + bh], fill=(16, 34, 64))
rng2 = random.Random(11)
for _ in range(40):
    sx = bx + rng2.randint(4, bw - 4)
    sy = by + rng2.randint(4, 60)
    d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 230, 255))
# missile arcs
for cx0, cx1, peak in [(30, 200, 26), (250, 420, 18)]:
    pts = []
    for t in range(21):
        x = bx + cx0 + (cx1 - cx0) * t / 20
        y = by + bh - 30 - peak * 4 * (t / 20) * (1 - t / 20) * 4
        pts.append((x, y))
    d.line(pts, fill=(255, 200, 80), width=2)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=(255, 200, 80))
# ships
for sx in (90, 330):
    d.rectangle([bx + sx, by + bh - 34, bx + sx + 90, by + bh - 20], fill=(70, 80, 95))
    d.rectangle([bx + sx + 34, by + bh - 52, bx + sx + 56, by + bh - 34], fill=(90, 100, 118))
# explosion bursts
for ex, ey in [(bx + 200, by + bh - 46), (bx + 420, by + bh - 40)]:
    star(d, ex, ey, 22, (255, 170, 40))
    star(d, ex, ey, 12, (255, 240, 160))
d.text((QX + QW // 2, RY + 140), "US–IRAN STRIKES WIDEN", font=font(SERIF, 32), fill=INK, anchor="ma")
d.text((QX + QW // 2, RY + 178), "ACROSS THE GULF", font=font(SERIF, 32), fill=INK, anchor="ma")
for j, line in enumerate(wrap(d, "Iran hits US bases in Kuwait and Bahrain after a US strike on Qeshm Island.",
                              font(SANS, 17), QW - 36)):
    d.text((QX + 18, RY + 218 + j * 22), line, font=font(SANS, 17), fill=(40, 40, 40))

# ---------------------------------------------------------------- row 3: three panels
TY, TH = 714, 236
TW = 320
# --- panel 1: Jeffries / Capitol
p1x = 24
panel(d, [p1x, TY, p1x + TW, TY + TH])
a1x, a1y, a1w, a1h = p1x + 2, TY + 2, TW - 4, 104
d.rectangle([a1x, a1y, a1x + a1w, a1y + a1h], fill=(196, 214, 228))
# capitol dome
d.rectangle([a1x + 60, a1y + a1h - 34, a1x + a1w - 60, a1y + a1h], fill=(240, 240, 235))
d.pieslice([a1x + 110, a1y + 18, a1x + a1w - 110, a1y + 78], 180, 360, fill=(240, 240, 235))
d.rectangle([a1x + 156, a1y + 6, a1x + 160, a1y + 22], fill=(60, 60, 60))
d.rectangle([a1x + 160, a1y + 6, a1x + 186, a1y + 16], fill=(178, 34, 34))
for cx in range(a1x + 84, a1x + a1w - 84, 22):
    d.rectangle([cx, a1y + a1h - 30, cx + 8, a1y + a1h - 8], fill=(120, 120, 110))
d.rectangle([a1x, a1y + a1h - 8, a1x + a1w, a1y + a1h], fill=(74, 110, 74))
d.text((p1x + TW // 2, TY + 112), "JEFFRIES TO BE FIRST", font=font(SERIF, 25), fill=INK, anchor="ma")
d.text((p1x + TW // 2, TY + 142), "BLACK SPEAKER", font=font(SERIF, 25), fill=INK, anchor="ma")
for j, line in enumerate(wrap(d, "Democrats nominate Hakeem Jeffries; he takes the gavel on 3 January.",
                              font(SANS, 15), TW - 28)):
    d.text((p1x + 14, TY + 176 + j * 19), line, font=font(SANS, 15), fill=(40, 40, 40))

# --- panel 2: Voyager 1
p2x = 352
panel(d, [p2x, TY, p2x + TW, TY + TH])
a2x, a2y, a2w, a2h = p2x + 2, TY + 2, TW - 4, 104
d.rectangle([a2x, a2y, a2x + a2w, a2y + a2h], fill=(8, 10, 26))
rng3 = random.Random(19)
for _ in range(48):
    sx = a2x + rng3.randint(4, a2w - 4)
    sy = a2y + rng3.randint(4, a2h - 4)
    r = rng3.choice([1, 1, 2])
    d.ellipse([sx, sy, sx + r, sy + r], fill=(255, 255, 255))
# probe: body + dish + boom
d.line([(a2x + 150, a2y + 52), (a2x + 96, a2y + 30)], fill=(200, 170, 90), width=3)
d.ellipse([a2x + 84, a2y + 18, a2x + 108, a2y + 42], outline=(230, 200, 120), width=3)
d.polygon([(a2x + 150, a2y + 40), (a2x + 172, a2y + 52), (a2x + 172, a2y + 68), (a2x + 150, a2y + 80)],
          fill=(210, 180, 100))
d.line([(a2x + 172, a2y + 60), (a2x + 216, a2y + 46)], fill=(200, 170, 90), width=3)
d.rectangle([a2x + 216, a2y + 40, a2x + 236, a2y + 52], fill=(90, 140, 200))
d.text((p2x + TW // 2, TY + 112), "VOYAGER 1 REACHES", font=font(SERIF, 25), fill=INK, anchor="ma")
d.text((p2x + TW // 2, TY + 142), "A LIGHT-DAY", font=font(SERIF, 25), fill=INK, anchor="ma")
for j, line in enumerate(wrap(d, "The probe, nearly 50 years in space, is believed to have travelled a light-day from Earth.",
                              font(SANS, 15), TW - 28)):
    d.text((p2x + 14, TY + 176 + j * 19), line, font=font(SANS, 15), fill=(40, 40, 40))

# --- panel 3: EU loan
p3x = 680
panel(d, [p3x, TY, p3x + TW, TY + TH])
a3x, a3y, a3w, a3h = p3x + 2, TY + 2, TW - 4, 104
d.rectangle([a3x, a3y, a3x + a3w, a3y + a3h], fill=(0, 51, 153))
import math
for i in range(12):
    ang = -math.pi / 2 + i * math.pi / 6
    sx = a3x + a3w // 2 + 34 * math.cos(ang)
    sy = a3y + a3h // 2 + 34 * math.sin(ang)
    star(d, sx, sy, 7, (255, 204, 0))
d.text((p3x + TW // 2, TY + 112), "EU PLANS €45BN", font=font(SERIF, 25), fill=INK, anchor="ma")
d.text((p3x + TW // 2, TY + 142), "UKRAINE LOAN", font=font(SERIF, 25), fill=INK, anchor="ma")
for j, line in enumerate(wrap(d, "Brussels proposes a €45bn loan for Kyiv, to be repaid after Russia pays reparations.",
                              font(SANS, 15), TW - 28)):
    d.text((p3x + 14, TY + 176 + j * 19), line, font=font(SANS, 15), fill=(40, 40, 40))

# ---------------------------------------------------------------- ticker
d.rectangle([0, 962, W, 1024], fill=NAVY)
tick = font(SANS_B, 17)
d.text((W // 2, 974), "ALSO TODAY  ·  Nvidia chief Jensen Huang quits  ·  Cyclone Akvan nears India  ·  Fed points to more hikes",
       font=tick, fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 997), "Pew: Islam set to be the world's largest faith by 2035",
       font=tick, fill=(255, 220, 120), anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
