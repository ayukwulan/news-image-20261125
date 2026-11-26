#!/usr/bin/env python3
"""Draw THE WORLD TODAY - Wednesday 25 November 2026.

A newspaper front page summing up 25 November 2026 in one 1024x1024 PNG.
Pillow only, no network, fully deterministic: same input -> same bytes.
Run: python3 draw.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (248, 244, 233)
INK = (26, 26, 26)
MUTED = (90, 83, 72)
RED = (163, 22, 33)
RULE = (26, 26, 26)
SEA = (38, 84, 124)
SKY = (214, 228, 238)

REGION_COLOURS = {
    "MIDDLE EAST": (185, 28, 28),
    "EUROPE": (29, 78, 216),
    "AFRICA": (194, 65, 12),
    "ASIA": (21, 128, 61),
    "NORTH AMERICA": (109, 40, 217),
    "SOUTH AMERICA": (161, 98, 7),
    "OCEANIA": (14, 116, 144),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(text, fnt, width, draw):
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1]
    return text + "..."


def chip(draw, x, y, num, colour=RED, r=11):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=colour, outline=(255, 255, 255), width=1)
    f = font(SANS_B, 12 if len(str(num)) < 2 else 11)
    tw = draw.textlength(str(num), font=f)
    draw.text((x - tw / 2, y - 7), str(num), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
# (number, region, beat, headline, detail)
SUPPORTING = [
    (2, "MIDDLE EAST", "IRAN WAR",
     "Houthis strike Ras Tanura refinery",
     "Houthis said they hit Saudi Arabia's Ras Tanura refinery."),
    (3, "MIDDLE EAST", "IRAN WAR",
     "Houthi strike hits Riyadh's tallest tower",
     "Saudi Civil Defense said 11 people were hurt in the strike."),
    (4, "MIDDLE EAST", "ISRAEL-HAMAS WAR",
     "Israel kills Hamas security chief in Gaza",
     "Mohammad Abuelouf, his wife and two children were killed."),
    (5, "EUROPE", "UKRAINE WAR",
     "Russian strike on Odesa kills two",
     "A child was among three hurt; Kyiv flats were hit too."),
    (6, "EUROPE", "UKRAINE WAR",
     "Putin: Kyiv keeps hitting Russian refineries",
     "Putin said Kyiv kept striking refineries despite Trump's plea."),
    (7, "EUROPE", "UKRAINE WAR",
     "490,334 Russian soldiers dead since 2022",
     "Leaked Russian figures analysed by the BBC: 490,334 dead."),
    (8, "EUROPE", "CLIMATE",
     "Pope Leo: COP31 failure is 'troubling'",
     "The pope urged leaders to act after COP31 collapsed with no deal."),
    (9, "OCEANIA", "SECURITY",
     "Solomon Islands bar foreign military bases",
     "A treaty with Australia precludes any foreign military base there."),
]

BRIEFS = [
    (10, "NORTH AMERICA", "TECH", "Huawei convicted in US trial"),
    (11, "NORTH AMERICA", "TRADE", "US proposes tariffs on 14 partners"),
    (12, "NORTH AMERICA", "MARKETS", "Nasdaq falls 2%, near bear market"),
    (13, "NORTH AMERICA", "ECONOMY", "US inflation hits 3.8% in October"),
    (14, "ASIA", "SPACE", "Shenzhou-24 docks; Pakistani aboard Tiangong"),
    (15, "ASIA", "CHINA", "Official sentenced to death for leaking secrets"),
    (16, "ASIA", "LABOUR", "Bangladesh garment wage up 36% to $139"),
    (17, "MIDDLE EAST", "SYRIA", "IS attack kills two security men in Hasaka"),
    (18, "AFRICA", "SECURITY", "Saudi national kidnapped by IS men in Niger"),
    (19, "EUROPE", "MIGRATION", "Record 2,100+ migrants reach Canary Islands"),
    (20, "NORTH AMERICA", "SECURITY", "CIA and ODNI hit by cyber breach"),
    (21, "NORTH AMERICA", "TECH", "Senator Booker presses Nvidia over Huang"),
    (22, "NORTH AMERICA", "MARKETS", "Nvidia down 35% from October peak"),
    (23, "NORTH AMERICA", "TECH", "Anthropic falls below $83 IPO price"),
    (24, "EUROPE", "SPORT", "Sinner has minor right-knee surgery"),
    (25, "EUROPE", "SPORT", "Man City 2-2 Napoli as Cherki rescues hosts"),
    (26, "EUROPE", "SPORT", "Real Madrid hit PSV 5-1; Bellingham stars"),
    (27, "AFRICA", "SPORT", "Senegal reinstated as AFCON champions"),
    (28, "EUROPE", "SPORT", "Czechia beat Canada 2-0 into Davis Cup semis"),
    (29, "NORTH AMERICA", "SPORT", "Steelers release Aaron Rodgers"),
    (30, "AFRICA", "SUDAN WAR", "RSF drone strikes kill 19 civilians"),
    (31, "AFRICA", "SECURITY", "At least 30 killed by militants in Nigeria"),
    (32, "AFRICA", "DISASTER", "Ten killed in bus-truck crash in Egypt"),
    (33, "ASIA", "DISASTER", "26 miners trapped in illegal gold mine"),
    (34, "EUROPE", "TECH", "Decathlon breach exposes 130,000 customers"),
    (35, "SOUTH AMERICA", "SECURITY", "Ecuador and US weigh joint military ops"),
]

NUMBERS = [
    ("490,334", "Russian soldiers dead since 2022, per leaked figures analysed by the BBC"),
    ("2,100+", "migrants reached Spain's Canary Islands in a single day, a record (Reuters)"),
    ("3.8%", "US inflation in October, year on year; core PCE 3.3% (US Bureau of Economic Analysis)"),
    ("14", "trading partners face new US tariffs over factory overcapacity (Reuters)"),
]

# Coarse dotted world map, 56 cols x 22 rows ('#' = land).
WORLD = [
    "...###########...###.......###...................###################...",
    "..#############..####......#####.................#######################.",
    ".###############..........#######..............########################.",
    "..#############...........######...............######################..",
    "...##########............####.................####################....",
    "....#########............#####................##################......",
    ".....########............#######.............###############.........",
    "......#######...........########..###........#############...........",
    ".......######...........########.............##########.............",
    "........####............########.............#########..............",
    ".........###...........########..............######.................",
    "..........####.........######...............####....................",
    "..........#####........######..............#####....................",
    "...........#####.......#####...............####.....................",
    "...........#####........####..............######....................",
    "............####........###..............#######...................",
    ".............###........###...............#####....................",
    "..............##..........................####....................",
    "..............##............................##....................",
    "..............#....................................................",
    "....................................................................",
    "....................................................................",
]

# (story number, lon, lat, dx, dy) pin offsets in pixels
PINS = [
    (1, 56.5, 26.5, 0, 0),
    (3, 46.7, 24.6, -8, 16),
    (4, 34.5, 31.5, -22, -8),
    (5, 30.7, 46.5, 2, -20),
    (9, 160.0, -9.0, 0, 0),
    (14, 98.5, 39.8, 0, -8),
    (16, 90.4, 23.8, 0, 8),
    (17, 40.7, 36.5, 24, -10),
    (18, 2.1, 13.5, 0, 0),
    (19, -16.0, 28.3, 0, 0),
    (30, 32.5, 15.6, 16, 14),
    (33, 106.8, -6.2, 0, 0),
]


def draw_lead_art(d, x0, y0, w, h):
    """Tanker at sea, mine blast. PIL shapes only."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY, outline=INK, width=1)
    # sun
    d.ellipse([x0 + w - 52, y0 + 10, x0 + w - 20, y0 + 42], fill=(232, 178, 74))
    # sea
    d.rectangle([x0, y0 + h - 52, x0 + w, y0 + h], fill=SEA)
    for wy in (y0 + h - 44, y0 + h - 30, y0 + h - 16):
        for wx in range(x0 + 8, x0 + w - 20, 34):
            d.arc([wx, wy, wx + 26, wy + 12], 0, 180, fill=(255, 255, 255), width=2)
    # tanker hull
    hx, hy = x0 + 18, y0 + h - 78
    d.polygon([(hx, hy), (hx + 190, hy), (hx + 178, hy + 26), (hx + 12, hy + 26)],
              fill=(44, 44, 46))
    d.rectangle([hx + 24, hy - 22, hx + 120, hy], fill=(120, 28, 32))
    d.rectangle([hx + 128, hy - 14, hx + 150, hy], fill=(120, 28, 32))
    d.rectangle([hx + 158, hy - 34, hx + 172, hy], fill=(230, 230, 230))
    d.rectangle([hx + 158, hy - 40, hx + 172, hy - 34], fill=(44, 44, 46))
    # explosion burst above the bow
    ex, ey = x0 + w - 78, y0 + 52
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        r = 34 if i % 2 == 0 else 16
        pts.append((ex + r * __import__("math").cos(ang),
                    ey + r * __import__("math").sin(ang)))
    d.polygon(pts, fill=(232, 120, 28), outline=(163, 22, 33))
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 214, 64))
    # naval mine, spiked circle
    mx, my = x0 + w - 150, y0 + h - 34
    for i in range(8):
        ang = i * 3.14159 / 4
        d.line([mx, my, mx + 16 * __import__("math").cos(ang),
                my + 16 * __import__("math").sin(ang)], fill=(26, 26, 26), width=2)
    d.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(26, 26, 26))
    # smoke
    d.ellipse([ex - 46, ey - 34, ex - 14, ey - 6], fill=(120, 120, 120))
    d.ellipse([ex - 30, ey - 44, ex + 2, ey - 16], fill=(150, 150, 150))


def draw_map(d, x0, y0, w, h):
    cols, rows = 56, 22
    cw, ch = w / cols, h / rows
    for r, line in enumerate(WORLD):
        for c, ch_ in enumerate(line):
            if c >= cols:
                break  # never draw past the declared 56 columns
            if ch_ == "#":
                cx, cy = x0 + c * cw + cw / 2, y0 + r * ch + ch / 2
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(47, 59, 76))
    f = font(SANS_B, 9)
    for num, lon, lat, dx, dy in PINS:
        col = (lon + 170.0) / 360.0 * cols
        row = (75.0 - lat) / 130.0 * rows
        tx = x0 + col * cw
        ty = y0 + row * ch
        px, py = tx + dx, ty + dy
        if dx or dy:
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
            d.line([(tx, ty), (px, py)], fill=RED, width=1)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28
    RX = W - MX

    # ---- masthead
    d.line([(MX, 6), (RX, 6)], fill=RULE, width=3)
    f_title = font(SERIF_B, 56)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 12), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 15)
    dateline = "WEDNESDAY 25 NOVEMBER 2026  ·  35 STORIES  ·  6 CONTINENTS"
    tw = d.textlength(dateline, font=f_date)
    d.text(((W - tw) / 2, 78), dateline, font=f_date, fill=RED)
    f_tag = font(SERIF_I, 13)
    tag = "Everything on this page happened, or was first reported, on Wednesday 25 November 2026."
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 100), tag, font=f_tag, fill=MUTED)
    f_src = font(SANS, 10)
    src = "Sources: Reuters · AP · AFP · BBC · Al Jazeera · Xinhua · US Bureau of Economic Analysis"
    tw = d.textlength(src, font=f_src)
    d.text(((W - tw) / 2, 118), src, font=f_src, fill=MUTED)
    d.line([(MX, 134), (RX, 134)], fill=RULE, width=2)

    # ---- lead story
    y = 144
    f_kick = font(SANS_B, 13)
    d.text((MX, y), "1  ·  MIDDLE EAST · IRAN WAR", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 25)
    head = ["TWO TANKERS HIT MINES", "IN THE STRAIT OF HORMUZ"]
    yy = y + 22
    for line in head:
        d.text((MX, yy), line, font=f_head, fill=INK)
        yy += 30
    f_body = font(SANS, 14)
    body = ("Iran's Revolutionary Guard said two oil tankers struck naval mines, "
            "exploded and caught fire while trying to use an unauthorised route "
            "through the strait, the world's busiest oil chokepoint.")
    blines = wrap(body, f_body, 620, d)
    yy += 4
    for line in blines:
        d.text((MX, yy), line, font=f_body, fill=INK)
        yy += 19
    draw_lead_art(d, 680, y, 316, 138)
    d.line([(MX, 292), (RX, 292)], fill=RULE, width=1)

    # ---- supporting stories 2-9, two columns x four rows
    col_w = 470
    row_h = 49
    y0 = 300
    f_tag2 = font(SANS_B, 10)
    f_h2 = font(SERIF_B, 15)
    f_b2 = font(SANS, 12)
    for i, (num, region, beat, headline, detail) in enumerate(SUPPORTING):
        col = i % 2
        row = i // 2
        x = MX + col * (col_w + 28)
        yy = y0 + row * row_h
        colour = REGION_COLOURS[region]
        chip(d, x + 11, yy + 10, num, colour)
        tx = x + 28
        d.text((tx, yy - 2), "%s · %s" % (region, beat), font=f_tag2, fill=colour)
        d.text((tx, yy + 12), headline, font=f_h2, fill=INK)
        d.text((tx, yy + 31), fit(detail, f_b2, col_w - 28, d), font=f_b2, fill=MUTED)
    d.line([(MX, 498), (RX, 498)], fill=RULE, width=1)

    # ---- map (left) + by the numbers (right)
    y0 = 508
    f_sec = font(SANS_B, 13)
    d.text((MX, y0), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((612, y0), "BY THE NUMBERS", font=f_sec, fill=INK)
    draw_map(d, MX, y0 + 22, 520, 128)  # ends x=548, clear of the numbers strip at 612
    # region legend under the map, kept inside the left column (ends x=548)
    leg = [("M. EAST", "1-4, 17"), ("EUROPE", "5-8, 19"), ("AFRICA", "18, 30-32"),
           ("ASIA", "14-16, 33"), ("N. AMER.", "10-13, 20-23"), ("OCEANIA", "9")]
    f_leg = font(SANS, 10)
    lx, ly = MX, y0 + 150
    for name, nums in leg:
        d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=REGION_COLOURS[
            {"M. EAST": "MIDDLE EAST", "EUROPE": "EUROPE", "AFRICA": "AFRICA",
             "ASIA": "ASIA", "N. AMER.": "NORTH AMERICA", "OCEANIA": "OCEANIA"}[name]])
        label = "%s %s" % (name, nums)
        d.text((lx + 12, ly), label, font=f_leg, fill=MUTED)
        lx += int(d.textlength(label, font=f_leg)) + 26
        if lx > 548:
            lx = MX
            ly += 13
    # numbers strip
    f_big = font(SERIF_B, 28)
    f_lab = font(SANS, 12)
    ny = y0 + 22
    for big, label in NUMBERS:
        d.text((612, ny), big, font=f_big, fill=RED)
        for j, line in enumerate(wrap(label, f_lab, 384 - int(d.textlength(big, font=f_big)) - 14, d)):
            d.text((612 + int(d.textlength(big, font=f_big)) + 14, ny + 4 + j * 15),
                   line, font=f_lab, fill=INK)
        ny += 38
    d.line([(MX, 684), (RX, 684)], fill=RULE, width=1)

    # ---- briefs 10-35, two columns x thirteen rows
    y0 = 692
    row_h = 24
    f_num = font(SANS_B, 12)
    f_btag = font(SANS_B, 9)
    f_bh = font(SANS, 12)
    for i, (num, region, beat, headline) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        x = MX + col * (col_w + 28)
        yy = y0 + row * row_h
        colour = REGION_COLOURS[region]
        d.text((x, yy), str(num), font=f_num, fill=colour)
        nx = x + 26
        tag = "%s · %s" % (region, beat)
        d.text((nx, yy + 1), tag, font=f_btag, fill=colour)
        hx = nx + int(d.textlength(tag, font=f_btag)) + 7
        d.text((hx, yy), fit(headline, f_bh, RX - hx, d), font=f_bh, fill=INK)
    d.line([(MX, 1006), (RX, 1006)], fill=RULE, width=1)
    f_foot = font(SANS, 10)
    foot = "THE WORLD TODAY — Wednesday 25 November 2026 · 35 stories · All events happened or were first reported on 25 November 2026."
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, 1011), foot, font=f_foot, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
