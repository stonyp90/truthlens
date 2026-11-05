#!/usr/bin/env python3
"""Splash TruthLens — particules → assemblage → résolution nette vers le lockup.

Pattern du venture studio (cf. Bespoke) : un champ de particules se déplace,
s'assemble pour former le signe (anneau-lentille + iris) et le wordmark,
impulsion à la complétion, puis fondu vers le lockup vectoriel net.
Sobre, haut de gamme. Aucune promesse de détection : le slogan est
« Mesuré, jamais deviné. »
"""
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1920, 1080, 30, 6.0
FRAMES = int(FPS * DUR)
BG = (9, 13, 19)            # navy profond (brand du site)
CYAN = (76, 201, 240)       # accent TruthLens
WHITE = (232, 238, 244)
AMBER = (255, 183, 3)

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

OUT = Path(__file__).with_name("splash-truthlens.mp4")
random.seed(42)

# ---------- Cible : anneau-lentille + iris + wordmark, échantillonnés en points
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
cx, cy, R = W // 2, 400, 150
md.ellipse([cx - R, cy - R, cx + R, cy + R], outline=255, width=26)
r2 = 62
md.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=255, width=16)
font_big = ImageFont.truetype(FONT_BOLD, 138)
text = "TRUTHLENS"
tw = md.textlength(text, font=font_big)
md.text(((W - tw) / 2, 640), text, fill=255, font=font_big)

pts = []
px = mask.load()
for y in range(0, H, 5):
    for x in range(0, W, 5):
        if px[x, y] > 0:
            pts.append((x + random.uniform(-2, 2), y + random.uniform(-2, 2)))
random.shuffle(pts)
N = min(2400, len(pts))
targets = pts[:N]

particles = []
for i in range(N):
    particles.append(
        {
            "sx": random.uniform(0, W),
            "sy": random.uniform(0, H),
            "tx": targets[i][0],
            "ty": targets[i][1],
            "delay": random.uniform(0, 0.55),
            "size": random.uniform(1.6, 3.6),
            "col": CYAN if random.random() < 0.72 else (WHITE if random.random() < 0.8 else AMBER),
            "ph": random.uniform(0, math.tau),
        }
    )
# particules ambiantes qui ne s'assemblent pas
ambient = [
    {"x": random.uniform(0, W), "y": random.uniform(0, H), "s": random.uniform(0.8, 1.8),
     "ph": random.uniform(0, math.tau)}
    for _ in range(160)
]


def ease_out_expo(t):
    return 1 if t >= 1 else 1 - pow(2, -10 * t)


def draw_lockup(alpha):
    """Le lockup net (vectoriel) qui se révèle à la fin."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = int(255 * alpha)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=CYAN + (a,), width=10)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=WHITE + (a,), width=7)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=CYAN + (a,))
    d.text(((W - tw) / 2, 640), text, fill=WHITE + (a,), font=font_big)
    f2 = ImageFont.truetype(FONT_REG, 44)
    sub = "INDICE DE TENSION VIDÉO"
    sw = d.textlength(sub, font=f2)
    d.text(((W - sw) / 2, 830), sub, fill=(170, 190, 205) + (a,), font=f2)
    f3 = ImageFont.truetype(FONT_REG, 36)
    tag = "Mesuré, jamais deviné."
    gw = d.textlength(tag, font=f3)
    d.text(((W - gw) / 2, 905), tag, fill=CYAN + (a,), font=f3)
    return layer


FRAMES_DIR = Path(__file__).with_name("frames")
FRAMES_DIR.mkdir(exist_ok=True)

for f in range(FRAMES):
    t = f / FPS
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")

    # ambiance
    for a_ in ambient:
        tw_ = 0.5 + 0.5 * math.sin(t * 0.9 + a_["ph"])
        d.ellipse([a_["x"], a_["y"], a_["x"] + a_["s"], a_["y"] + a_["s"]],
                  fill=(90, 130, 160, int(40 + 60 * tw_)))

    # progression d'assemblage : démarre à 0.4 s, complète ~3.6 s
    prog = min(1.0, max(0.0, (t - 0.4) / 3.2))
    # impulsion à la complétion (~3.6 s)
    if 3.6 < t < 4.4:
        pr = (t - 3.6) / 0.8
        rr = R + pr * 190
        alpha = int(160 * (1 - pr))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=CYAN + (alpha,), width=4)

    final_alpha = min(1.0, max(0.0, (t - 4.2) / 1.1))  # révélation du lockup net
    p_alpha = 1.0 - 0.72 * final_alpha

    for p in particles:
        lt = min(1.0, max(0.0, (prog - p["delay"]) / max(0.05, 1 - p["delay"])))
        e = ease_out_expo(lt)
        x = p["sx"] + (p["tx"] - p["sx"]) * e
        y = p["sy"] + (p["ty"] - p["sy"]) * e
        if lt >= 1:  # micro-respiration une fois assemblé
            x += math.sin(t * 1.4 + p["ph"]) * 1.1
            y += math.cos(t * 1.2 + p["ph"]) * 1.1
        s = p["size"]
        col = p["col"] + (int(235 * p_alpha),)
        d.ellipse([x - s / 2, y - s / 2, x + s / 2, y + s / 2], fill=col)

    if final_alpha > 0:
        img = Image.alpha_composite(img.convert("RGBA"), draw_lockup(final_alpha)).convert("RGB")

    img.save(FRAMES_DIR / f"f{f:04d}.png")

subprocess.run(
    ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(FRAMES_DIR / "f%04d.png"),
     "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
     "-preset", "medium", "-movflags", "+faststart", str(OUT)],
    check=True, capture_output=True,
)
print("OK", OUT, OUT.stat().st_size)
