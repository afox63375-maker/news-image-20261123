#!/usr/bin/env python3
"""Workshop renderer for the news-image-20261123 front page.

Draws entry.png (1024x1024) from the verified 23 November 2026 story list.
Own code, own layout, own illustrations. Deterministic: no randomness,
no timestamps, no network. Run:  python3 draw.py  (writes entry.png here)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 239, 220)
INK = (28, 28, 28)
NAVY = (18, 32, 66)
RED = (172, 30, 30)
DARKRED = (140, 22, 22)
GOLD = (214, 176, 60)
GREY = (112, 106, 90)
LINE = (120, 110, 88)
SKY = (168, 205, 225)
NIGHT = (16, 24, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    for cand in (os.path.join(FONT_DIR, name),
                 os.path.join(FONT_DIR, "DejaVuSans.ttf")):
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------------ icons
def icon_sun(d, cx, cy, r, col=(224, 150, 30)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for k in range(8):
        import math
        a = k * math.pi / 4
        x1 = cx + int((r + 2) * math.cos(a))
        y1 = cy + int((r + 2) * math.sin(a))
        x2 = cx + int((r + 6) * math.cos(a))
        y2 = cy + int((r + 6) * math.sin(a))
        d.line([x1, y1, x2, y2], fill=col, width=2)


def icon_cloud(d, cx, cy, s, col=(150, 150, 145)):
    d.ellipse([cx - s, cy - s // 2, cx, cy + s // 2], fill=col)
    d.ellipse([cx - s // 2, cy - s, cx + s // 2, cy + s // 3], fill=col)
    d.ellipse([cx, cy - s // 2, cx + s, cy + s // 2], fill=col)
    d.rectangle([cx - s, cy, cx + s, cy + s // 2], fill=col)


def icon_rain(d, cx, cy, s):
    icon_cloud(d, cx, cy - 3, s)
    for dx in (-6, 0, 6):
        d.line([cx + dx, cy + s // 2, cx + dx - 2, cy + s // 2 + 7],
               fill=(70, 110, 180), width=2)


def icon_storm(d, cx, cy, s):
    icon_cloud(d, cx, cy - 3, s, col=(90, 90, 95))
    d.polygon([(cx + 2, cy + s // 2), (cx - 4, cy + s + 6),
               (cx + 1, cy + s + 6), (cx - 2, cy + s + 12)], fill=(224, 170, 30))


# ------------------------------------------------------- illustration scenes
def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 228))
    d.ellipse([x + 14, y + 16, x + 74, y + 76], fill=(52, 120, 190))
    d.ellipse([x + 26, y + 30, x + 44, y + 46], fill=(90, 170, 90))
    d.ellipse([x + 48, y + 52, x + 66, y + 68], fill=(90, 170, 90))
    d.rectangle([x + 90, y + 96, x + w - 12, y + 116], fill=(120, 84, 50))
    d.rectangle([x + 90, y + 88, x + w - 12, y + 96], fill=(150, 110, 66))
    for i, c in enumerate([(200, 60, 60), (60, 120, 200), (60, 170, 90),
                           (230, 170, 40), (150, 80, 170), (230, 120, 40)]):
        bx = x + 104 + i * 36
        d.ellipse([bx, y + 62, bx + 16, y + 78], fill=(232, 200, 160))
        d.rectangle([bx - 2, y + 78, bx + 18, y + 96], fill=c)
    d.rectangle([x + w - 66, y + 14, x + w - 14, y + 52], fill=(255, 255, 255),
                outline=INK)
    d.line([x + w - 62, y + 16, x + w - 18, y + 50], fill=RED, width=4)
    d.text((x + w - 58, y + 26), "0", font=SANS_B(16), fill=RED)


def scene_talks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
    d.rectangle([x + 60, y + 34, x + w - 60, y + 108], fill=(196, 160, 110))
    d.polygon([(x + 60, y + 34), (x + w // 2, y + 8), (x + w - 60, y + 34)],
              fill=(150, 60, 50))
    d.rectangle([x + w // 2 - 14, y + 66, x + w // 2 + 14, y + 108],
                fill=(90, 60, 40))
    for px, cols in ((x + 26, [(255, 153, 51), (255, 255, 255), (19, 136, 8)]),
                     (x + w - 52, [(220, 40, 60), (40, 60, 160)])):
        d.line([px + 12, y + 18, px + 12, y + 96], fill=INK, width=2)
        for i, c in enumerate(cols):
            d.rectangle([px, y + 20 + i * 10, px + 24, y + 30 + i * 10], fill=c)
    for fx, c in ((x + 106, (40, 70, 140)), (x + 204, (120, 40, 40))):
        d.ellipse([fx, y + 78, fx + 18, y + 96], fill=(232, 200, 160))
        d.rectangle([fx - 2, y + 96, fx + 20, y + 122], fill=c)
    d.ellipse([x + 150, y + 92, x + 176, y + 104], fill=(232, 200, 160))


def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 48))
    pts = [(x + 16, y + 30), (x + 70, y + 46), (x + 120, y + 40),
           (x + 170, y + 74), (x + 220, y + 66), (x + 268, y + 108),
           (x + 306, y + 132)]
    d.line(pts, fill=(230, 60, 50), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    for i, (cx, top, bot) in enumerate([(x + 40, y + 96, y + 122),
                                        (x + 110, y + 84, y + 118),
                                        (x + 180, y + 100, y + 130),
                                        (x + 250, y + 108, y + 138)]):
        d.rectangle([cx, top, cx + 18, bot], fill=(200, 50, 45))
        d.line([cx + 9, top - 10, cx + 9, bot + 8], fill=(200, 50, 45), width=2)
    d.text((x + 16, y + h - 20), "-17% WEEK", font=SANS_B(13),
           fill=(255, 120, 110))


def scene_fire(d, x, y, w, h):
    # card illustration: everything inside the 74px strip
    d.rectangle([x, y, x + w, y + h], fill=(210, 190, 160))
    for sx, sy, sr in ((x + 60, y + 12, 12), (x + 130, y + 8, 15),
                       (x + 175, y + 14, 10)):
        d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=(90, 88, 86))
    d.rectangle([x + 24, y + 46, x + w - 24, y + h], fill=(120, 118, 112))
    for i in range(3):
        bx = x + 36 + i * 52
        d.polygon([(bx, y + 46), (bx + 24, y + 32), (bx + 48, y + 46)],
                  fill=(90, 88, 84))
    for fx in (x + 56, x + 120, x + 168):
        d.polygon([(fx, y + 46), (fx + 9, y + 26), (fx + 18, y + 46)],
                  fill=(240, 120, 20))
        d.polygon([(fx + 5, y + 46), (fx + 9, y + 34), (fx + 13, y + 46)],
                  fill=(250, 210, 40))
    d.rectangle([x + 118, y + 60, x + 148, y + h], fill=(60, 58, 56))


def scene_exam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 220, 198))
    for i in range(3):
        dx = x + 16 + i * 56
        d.rectangle([dx, y + 56, dx + 44, y + 64], fill=(150, 110, 66))
        d.rectangle([dx + 8, y + 46, dx + 36, y + 56], fill=(255, 255, 255),
                    outline=GREY)
        d.ellipse([dx + 14, y + 26, dx + 30, y + 40], fill=(232, 200, 160))
        d.rectangle([dx + 10, y + 40, dx + 34, y + 56], fill=(70, 90, 140))


def scene_pmi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 210))
    cx, cy, r = x + w // 2, y + 58, 30
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(210, 200, 170))
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 270, fill=(200, 60, 50))
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 270, 315, fill=(230, 170, 40))
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 315, 360, fill=(70, 150, 90))
    import math
    a = math.radians(205)
    d.line([cx, cy, cx + int(24 * math.cos(a)), cy + int(24 * math.sin(a))],
           fill=INK, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    d.text((x + 12, y + 62), "DOWN", font=SANS_B(9), fill=DARKRED)


def scene_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 235))
    d.ellipse([x + 14, y + 24, x + 34, y + 44], fill=(230, 80, 60))
    d.rectangle([x + 56, y + 12, x + w - 56, y + 20], fill=(190, 40, 30))
    d.rectangle([x + 66, y + 6, x + w - 66, y + 12], fill=(190, 40, 30))
    d.rectangle([x + 68, y + 20, x + 76, y + h], fill=(190, 40, 30))
    d.rectangle([x + w - 76, y + 20, x + w - 68, y + h], fill=(190, 40, 30))
    d.rectangle([x + 76, y + 44, x + w - 76, y + 50], fill=(190, 40, 30))
    d.rectangle([x + 78, y + 54, x + w - 78, y + 70], fill=(255, 255, 255),
                outline=INK)
    d.text((x + 86, y + 57), "CLOSED", font=SANS_B(10), fill=DARKRED)


def scene_pmis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 210))
    d.line([x + 16, y + 58, x + w - 16, y + 58], fill=INK, width=2)
    for i, (lbl, ht, c) in enumerate([("EU", 26, (60, 100, 160)),
                                      ("UK", 34, (60, 140, 90)),
                                      ("US", 22, (200, 60, 50))]):
        bx = x + 30 + i * 52
        d.rectangle([bx, y + 58 - ht, bx + 28, y + 58], fill=c)
        d.text((bx + 4, y + 61), lbl, font=SANS_B(10), fill=INK)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
    d.rectangle([x, y + 52, x + w, y + 64], fill=(210, 190, 140))
    for sx in (x + 36, x + w - 48):
        for k in range(3):
            d.rectangle([sx + k * 6, y + 30, sx + k * 6 + 4, y + 52],
                        fill=(240, 220, 140))
    d.rectangle([x + w - 66, y + 22, x + w - 8, y + 40], fill=(200, 60, 50),
                outline=INK)
    d.text((x + w - 60, y + 25), "720/9", font=SANS_B(11),
           fill=(255, 255, 255))
    d.rectangle([x + 96, y + 56, x + 128, y + 62], fill=(190, 140, 80))
    d.ellipse([x + 118, y + 42, x + 130, y + 54], fill=(200, 40, 40))


def scene_aqi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 188, 160))
    d.text((x + 14, y + 20), "335", font=SERIF_B(20), fill=DARKRED)
    d.text((x + 76, y + 28), "HAZARDOUS", font=SANS_B(9), fill=DARKRED)
    for i, bh in enumerate([22, 30, 18, 26, 20]):
        bx = x + 12 + i * 36
        d.rectangle([bx, y + h - bh, bx + 28, y + h], fill=(120, 112, 100))
    d.rectangle([x + 12, y + h - 4, x + w - 12, y + h], fill=(90, 84, 74))


def scene_climate_row(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 216, 180))
    d.rectangle([x + 16, y + 46, x + 76, y + h], fill=(110, 108, 104))
    d.polygon([(x + 22, y + 46), (x + 30, y + 30), (x + 38, y + 46)],
              fill=(90, 88, 86))
    d.ellipse([x + 24, y + 14, x + 42, y + 30], fill=(150, 150, 145))
    d.ellipse([x + 44, y + 8, x + 64, y + 26], fill=(150, 150, 145))
    d.polygon([(x + 118, y + 26), (x + 146, y + 20), (x + 142, y + 44),
               (x + 116, y + 48)], fill=(230, 200, 90))
    d.rectangle([x + 142, y + 30, x + 150, y + 66], fill=(120, 84, 50))
    d.rectangle([x + 96, y + 50, x + 168, y + 70], fill=(255, 255, 255),
                outline=INK)
    d.text((x + 104, y + 55), "PAY UP", font=SANS_B(10), fill=RED)


def scene_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 224, 232))
    d.arc([x + 30, y + 16, x + w - 30, y + 96], 180, 360, fill=(90, 90, 110),
          width=4)
    d.rectangle([x + 30, y + 56, x + 38, y + h], fill=(90, 90, 110))
    d.rectangle([x + w - 38, y + 56, x + w - 30, y + h], fill=(90, 90, 110))
    for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        d.rectangle([x + 14, y + 48 + i * 7, x + 38, y + 55 + i * 7], fill=c)
    cx, cy = x + w - 40, y + 34
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(52, 90, 180))
    for k in range(8):
        import math
        a = k * math.pi / 4
        d.ellipse([cx - 2 + int(15 * math.cos(a)), cy - 2 + int(15 * math.sin(a)),
                   cx + 2 + int(15 * math.cos(a)), cy + 2 + int(15 * math.sin(a))],
                  fill=(255, 220, 60))
    d.ellipse([x + 80, y + 46, x + 98, y + 58], fill=(232, 200, 160))
    d.ellipse([x + w - 98, y + 46, x + w - 80, y + 58], fill=(232, 200, 160))


def scene_myanmar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 200))
    for i, c in enumerate([(250, 200, 40), (60, 160, 70), (200, 50, 40)]):
        d.rectangle([x + 24, y + 6 + i * 12, x + w - 24, y + 18 + i * 12], fill=c)
    cx, cy = x + w // 2, y + 24
    d.polygon([(cx, cy - 9), (cx + 3, cy - 2), (cx + 9, cy - 2),
               (cx + 5, cy + 2), (cx + 7, cy + 8), (cx, cy + 4),
               (cx - 7, cy + 8), (cx - 5, cy + 2), (cx - 9, cy - 2),
               (cx - 3, cy - 2)], fill=(255, 255, 255))
    d.rectangle([x + 40, y + 66, x + w - 40, y + 71], fill=(120, 84, 50))
    d.line([x + w // 2, y + 52, x + w // 2, y + 66], fill=(120, 84, 50), width=3)
    d.rectangle([x + w // 2 - 24, y + 46, x + w // 2 + 24, y + 52],
                fill=(120, 84, 50))


# ------------------------------------------------------------- dotted map
MAP_ROWS = [
    "                                                            ",
    "                                                            ",
    "         #######                       ##########           ",
    "      #############                 #################      ",
    "    ###############      ######   ####################     ",
    "     ##############     ######## ################## ##     ",
    "      ############       ######  ###################       ",
    "       #########         #####    ######## #########       ",
    "        #######           ###      ######  #######  ##      ",
    "         #####            ##        ####    #####           ",
    "          ###             ###        ##      ###            ",
    "           ##            #####       ##       #             ",
    "            ##          #######     ###                     ",
    "             ##         ########    ###                     ",
    "             ###        #########    ##                     ",
    "              ##         ########     #                     ",
    "              ###         ######                            ",
    "               ##          ####                             ",
    "               ##           ##          #######             ",
    "                #           #           #########           ",
    "                            #            #######             ",
    "                                          #####             ",
]
# (story number, grid col, grid row) — pins for the numbered stories
PINS = [(1, 35, 6), (2, 42, 7), (3, 47, 11), (4, 49, 13), (6, 55, 15),
        (7, 53, 7), (9, 57, 17), (10, 40, 9), (11, 33, 7), (12, 44, 9),
        (13, 47, 8)]


def draw_map(d, x, y, w, h):
    cell = 6.1
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                px = x + 6 + c * cell
                py = y + 6 + r * cell
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(178, 148, 90))
    for num, gc, gr in PINS:
        px = x + 6 + gc * cell
        py = y + 6 + gr * cell
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=SANS_B(9))
        d.text((px - tw / 2, py - 6.5), t, font=SANS_B(9), fill=(255, 255, 255))
    d.text((x, y + h - 12), "8 is global — no pin. 5, 10 and 12 share New Delhi.",
           font=SANS(8), fill=GREY)


# ------------------------------------------------------------------ content
LEADS = [
    dict(num=1, tag="COP31: NO DEAL", kicker="ANTALYA, TURKIYE · CLIMATE",
         head="COP31 climate talks collapse with no deal",
         deck="Nearly 200 nations fail to agree after a fight over fossil "
              "fuels; the final draft never mentions them. "
              "(Global Society, Tonga Independent)",
         scene=scene_cop31),
    dict(num=2, tag="NEPAL-INDIA TALKS", kicker="NEW DELHI, INDIA · DIPLOMACY",
         head="Nepal's PM holds talks with Modi in Delhi",
         deck="Balendra Shah's first bilateral visit since taking office "
              "brings MoUs on energy, education and health. "
              "(New Kerala, ObserverVoice)",
         scene=scene_talks),
    dict(num=3, tag="AI ROUT FEARS", kicker="SINGAPORE · MARKETS",
         head="Asia braces for another AI sell-off",
         deck="US futures bounce 2% as Asia opens; Japan shut for a holiday, "
              "Taiwan tightens short-selling after a 17% weekly fall. (Reuters)",
         scene=scene_markets),
]

CARDS = [
    dict(num=4, tag="SEARCH RESUMES", kicker="CIKANDE, INDONESIA",
         head="Factory fire search resumes Monday",
         deck="24 body bags found; ~30 still missing. (Xinhua, AP)",
         scene=scene_fire),
    dict(num=5, tag="EXAMS", kicker="NEW DELHI, INDIA",
         head="JEE Main 2027 sign-up closes today",
         deck="Session 1 registration ends tonight. (Jagran Josh)",
         scene=scene_exam),
    dict(num=6, tag="PMI 46.1", kicker="CANBERRA, AUSTRALIA",
         head="Australia flash PMI falls to 46.1",
         deck="Down from 48.2 as activity shrinks. (Newsquawk)",
         scene=scene_pmi),
    dict(num=7, tag="HOLIDAY", kicker="TOKYO, JAPAN",
         head="Japan markets shut for holiday",
         deck="Labour Thanksgiving Day closes Tokyo. (Reuters)",
         scene=scene_japan),
    dict(num=8, tag="PMIs TODAY", kicker="WORLD",
         head="Flash PMIs due across the West",
         deck="Eurozone, UK and US surveys land today. (Newsquawk)",
         scene=scene_pmis),
    dict(num=9, tag="FINAL DAY", kicker="WELLINGTON, NEW ZEALAND",
         head="Test final day: NZ bat to survive",
         deck="119-2 overnight, trailing by 233. (ESPNcricinfo)",
         scene=scene_cricket),
    dict(num=10, tag="AQI 335", kicker="NEW DELHI, INDIA",
         head="Delhi air turns hazardous",
         deck="AQI 335 as fog hangs over the capital. (weather.com)",
         scene=scene_aqi),
    dict(num=11, tag="CLIMATE ROW", kicker="ANTALYA / AUSTRALIA",
         head="'Arsonists wrote the fire plan'",
         deck="Polluters-pay campaign blasts COP31. (Medianet)",
         scene=scene_climate_row),
    dict(num=12, tag="TRADE PACT", kicker="NEW DELHI, INDIA",
         head="India-EU pact likely signed 16 Dec",
         deck="Trade deal set for Brussels. (Jagran Josh)",
         scene=scene_trade),
    dict(num=13, tag="ASEAN ROW", kicker="NAYPYIDAW, MYANMAR",
         head="Myanmar calls ASEAN move 'unfair'",
         deck="Army-backed government hits back. (Jagran Josh)",
         scene=scene_myanmar),
]

BRIEF = [
    (14, "LISBON", "Thousands march on living costs (Reuters)"),
    (15, "KINSHASA", "WHO: fighting near Ebola area disrupts response (Arab News PK)"),
    (16, "JUBA", "SPLA-IO attack leaves 24 civilians dead (Arab News PK)"),
    (17, "WARSAW", "Russia 'twice tried to kill' US rapper (Arab News PK)"),
    (18, "WASHINGTON", "Democrats clinch House majority, 258 seats (Arab News PK)"),
    (19, "WASHINGTON", "Bessent seeks answers on Nvidia chips to China (Arab News PK)"),
    (20, "GULF OF OMAN", "UKMTO reports tanker incident (Arab News PK)"),
    (21, "ISLAMABAD", "FM hopeful for US-Iran deal (Arab News PK)"),
    (22, "ITANAGAR", "Shah stresses self-reliance in Arunachal (Jagran Josh)"),
    (23, "GOA", "IFFI hosts BRICS film roundtable (Jagran Josh)"),
    (24, "PATNA", "Modi opens AI centre at IIT Patna (Jagran Josh)"),
    (25, "KHARAGPUR", "Google gives $5m for IIT AI research (Jagran Josh)"),
    (26, "NEW DELHI", "Oil import bill up 60% in Oct (Jagran Josh)"),
    (27, "MUMBAI", "Mahindra Last Mile eyes IPO in 18 months (Jagran Josh)"),
    (28, "NEW DELHI", "Rajya Sabha MP Wadkute dies in Delhi (Jagran Josh)"),
    (29, "SPORT", "Anupama defends world snooker title (Daily Jagran)"),
    (30, "HORMUZ", "Strait conflict enters crucial stage (ObserverVoice)"),
    (31, "GOA", "IFFI shows restored film classics (Jagran Josh)"),
    (32, "HYDERABAD", "Students keep up campus protest (Daily Jagran)"),
]

STATS = [("~200", "nations at the COP31 talks"),
         ("0", "fossil-fuel mentions in the draft"),
         ("258", "Democrats' House seats"),
         ("335", "Delhi AQI — hazardous"),
         ("+2%", "Nasdaq futures bounce"),
         ("46.1", "Australia flash PMI")]

REGIONS = [("EUROPE", 2, (47, 93, 138)), ("MIDEAST", 2, (163, 51, 39)),
           ("AMER.", 2, (74, 124, 89)), ("ASIA-PACIFIC", 21, (192, 138, 45)),
           ("AFRICA", 2, (122, 74, 138)), ("WORLD", 3, (68, 68, 68))]

WEATHER = [("ANTALYA", "22/16 C", "sun"),
           ("NEW DELHI", "26/13 C", "cloud"),
           ("WELLINGTON", "18/14 C", "cloud"),
           ("JAKARTA", "34/26 C", "storm"),
           ("TAIPEI", "27/19 C", "cloud"),
           ("CANBERRA", "26/10 C", "rain")]


def tag_and_badge(d, x, y, w, tag, num, h=150):
    tw = d.textlength(tag, font=SANS_B(11)) + 12
    d.rectangle([x, y, x + tw, y + 18], fill=RED)
    d.text((x + 6, y + 3), tag, font=SANS_B(11), fill=(255, 255, 255))
    cx, cy = x + w - 16, y + 16
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255),
              outline=RED, width=2)
    t = str(num)
    tw2 = d.textlength(t, font=SANS_B(11))
    d.text((cx - tw2 / 2, cy - 7.5), t, font=SANS_B(11), fill=RED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)

    # top bar
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((10, 7), "THE WORLD IN ONE DAY", font=SANS_B(12), fill=GOLD)
    right = "32 STORIES · 6 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
    d.text((W - 10 - d.textlength(right, font=SANS(10)), 8), right,
           font=SANS(10), fill=(255, 255, 255))

    # masthead
    d.text((10, 32), "Monday 23 November 2026", font=SERIF_B(60), fill=INK)
    d.text((10, 100), "COP31 collapses with no deal  ·  Nepal's PM meets Modi "
           "in Delhi  ·  Asia braces for another tech sell-off",
           font=SERIF(16), fill=DARKRED)

    # stat strip
    y0, y1 = 128, 170
    d.line([10, y0, W - 10, y0], fill=LINE, width=1)
    cw = (W - 20) / 6
    for i, (num, cap) in enumerate(STATS):
        x = 10 + i * cw
        if i:
            d.line([x, y0 + 4, x, y1 - 4], fill=LINE, width=1)
        d.text((x + 8, y0 + 2), num, font=SERIF_B(26), fill=RED)
        d.text((x + 8, y1 - 14), cap, font=SANS(9), fill=INK)
    d.line([10, y1, W - 10, y1], fill=LINE, width=1)

    # region bar
    y0 = 176
    total = sum(c for _, c, _ in REGIONS)
    x = 10
    for name, count, col in REGIONS:
        seg = (W - 20) * count / total
        d.rectangle([x, y0, x + seg, y0 + 20], fill=col)
        label = f"{name} {count}"
        for size in (11, 10, 9):
            fnt = SANS_B(size)
            if d.textlength(label, font=fnt) <= seg - 4 or size == 9:
                break
        d.text((x + 3, y0 + 10 - size // 2 - 1), label, font=fnt,
               fill=(255, 255, 255))
        x += seg

    # weather strip
    y0 = 202
    d.rectangle([10, y0, 118, y0 + 30], fill=NAVY)
    d.text((16, y0 + 4), "MONDAY", font=SANS_B(11), fill=GOLD)
    d.text((16, y0 + 16), "WEATHER", font=SANS_B(11), fill=(255, 255, 255))
    cw = (W - 20 - 108) / 6
    for i, (city, temps, kind) in enumerate(WEATHER):
        x = 118 + i * cw
        d.rectangle([x, y0, x + cw, y0 + 30], outline=LINE)
        ix = x + 16
        if kind == "sun":
            icon_sun(d, ix, y0 + 15, 7)
        elif kind == "storm":
            icon_storm(d, ix, y0 + 15, 7)
        elif kind == "rain":
            icon_rain(d, ix, y0 + 15, 7)
        else:
            icon_cloud(d, ix, y0 + 15, 7)
        d.text((x + 30, y0 + 3), city, font=SANS_B(10), fill=INK)
        d.text((x + 30, y0 + 16), temps, font=SANS(10), fill=INK)

    # three lead panels
    y0 = 240
    pw = 328
    for i, lead in enumerate(LEADS):
        x = 10 + i * (pw + 10)
        lead["scene"](d, x, y0, pw, 150)
        d.rectangle([x, y0, x + pw, y0 + 150], outline=INK)
        tag_and_badge(d, x, y0, pw, lead["tag"], lead["num"])
        yy = y0 + 158
        d.text((x, yy), f"{lead['num']}  {lead['kicker']}", font=SANS_B(10),
               fill=RED)
        yy += 16
        yy = text_block(d, x, yy, wrap(d, lead["head"], SERIF_B(19), pw),
                        SERIF_B(19), INK, 23)
        text_block(d, x, yy + 2, wrap(d, lead["deck"], SANS(10), pw),
                   SANS(10), INK, 13)

    # ten mini cards, two rows of five
    cw = 197
    gap = (W - 20 - 5 * cw) / 4
    for row in range(2):
        y0 = 484 + row * 138
        for col in range(5):
            card = CARDS[row * 5 + col]
            x = 10 + col * (cw + gap)
            card["scene"](d, x, y0, cw, 74)
            d.rectangle([x, y0, x + cw, y0 + 74], outline=INK)
            tag_and_badge(d, x, y0, cw, card["tag"], card["num"])
            yy = y0 + 80
            d.text((x, yy), card["kicker"], font=SANS_B(8), fill=RED)
            yy += 11
            yy = text_block(d, x, yy,
                            wrap(d, card["head"], SERIF_B(12), cw),
                            SERIF_B(12), INK, 15)
            text_block(d, x, yy + 1,
                       wrap(d, card["deck"], SANS(9), cw), SANS(9), INK, 12)

    # map + brief list
    y0 = 768
    d.text((10, y0), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((150, y0 + 2), "pins match story numbers", font=SERIF(10), fill=GREY)
    draw_map(d, 10, y0 + 18, 380, 140)
    bx = 404
    d.text((bx, y0), "ALSO ON MONDAY 23 NOVEMBER — 19 MORE STORIES",
           font=SANS_B(12), fill=INK)
    d.line([bx, y0 + 17, W - 10, y0 + 17], fill=LINE, width=1)
    half = 10
    for i, (num, place, txt) in enumerate(BRIEF):
        col = 0 if i < half else 1
        r = i if i < half else i - half
        x = bx + col * 308
        yy = y0 + 24 + r * 14
        d.text((x, yy), f"{num}", font=SANS_B(9), fill=RED)
        d.text((x + 20, yy), f"{place}: {txt}", font=SANS(9), fill=INK)

    # date check
    y0 = 934
    d.rectangle([10, y0, W - 10, y0 + 40], outline=RED, width=2)
    d.text((16, y0 + 3), "DATE CHECK", font=SANS_B(11), fill=RED)
    check = ("Wires read up to 00:30 UTC, Monday 23 November 2026: every story "
             "here was first reported on 23 November in at least one time zone, "
             "or happens today. Left out as other days' news: the El Chapo "
             "Isidro capture (20-21 Nov), the Sparta II strike (21 Nov), the "
             "Kyiv drone strike (22 Nov), Liverpool 4-0 Man Utd (22 Nov), the "
             "UN killer-robot talks (21 Nov) and Seoul's minister resigning "
             "(22 Nov).")
    text_block(d, 16, y0 + 16, wrap(d, check, SANS(9), W - 32), SANS(9), INK, 11)

    # sources + bottom bar
    d.text((10, 978),
           "Sources: Reuters, Global Society, Tonga Independent, New Kerala, ObserverVoice, Newsquawk, Xinhua, Jagran Josh, Arab News PK, Medianet, ESPNcricinfo, weather.com. Every story names its outlet. Pictures and map: original, drawn in code.",
           font=SANS(8), fill=GREY)
    d.rectangle([0, 996, W, H], fill=NAVY)
    d.text((10, 1006), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=GOLD)
    tail = "MONDAY 23 NOVEMBER 2026 · ONE PAGE"
    d.text((W - 10 - d.textlength(tail, font=SANS(10)), 1007), tail,
           font=SANS(10), fill=(255, 255, 255))
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
