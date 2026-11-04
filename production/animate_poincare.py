"""Renderiza el video de Poincare. Uso: animate_poincare.py <en|es> [--still] [--scene N]

Las animaciones son esquemas propios para explicar la idea, no simulaciones del flujo de Ricci.
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, "D:/Dev/mathdb-video")
from animate import (BG, BLUE, FPS, GREEN, H, INK, MUTED, ORANGE, PAD, PANEL, RED, W, centered, draw_caption, f_body,
                     f_math, f_title, fade, fmt, items, mix, sentence_cues, text_block, title, wav_seconds, wrap)

BASE = Path("D:/Dev/mathdb-video/poincare")
PROJECT = Path("D:/Dev/docker-phonon/projects/poincare")
ROPE = (250, 204, 21)
APPLE = (190, 60, 60)
DONUT = (180, 125, 70)

TEXT = {
    "en": {
        1: {"title": "The Shape of a World You Cannot Leave", "sub": "The Poincaré conjecture, for everyone"},
        2: {"title": "The rope test", "good": "The rope comes back", "bad": "The rope gets stuck"},
        3: {"title": "One dimension up", "q": "Finite, no edge, and every rope comes back.", "q2": "Must it be the 3-sphere?"},
        4: {"title": "A century of trying", "open": "still unsolved", "five": "dimensions 5 and up", "four": "dimension 4", "three": "dimension 3", "start": "the question"},
        5: {"title": "Let the shape heal itself", "heat": "heat evens out", "flow": "Ricci flow evens out shape"},
        6: {"title": "The trouble: a neck that pinches", "cut": "Cut and cap, then keep going", "pinch": "The neck pinches first"},
        7: {"title": "Perelman, 2002–2003", "items": ["Trouble spots look like a few simple models", "Each cut removes a definite amount of volume", "So cuts cannot pile up endlessly in finite time"],
            "prize": "Fields Medal and a million-dollar prize: declined both"},
        8: {"title": "Everything disappears", "fwd": "Passes the rope test: every piece vanishes", "back": "Run it backward: only a sphere can be rebuilt"},
        9: {"title": "Can a computer check it?",
            "cards": [("Reported", "A 2026 team reported a Lean proof. MathDB marks one version as Lean verified."),
                      ("Not done by us", "We did not run that huge check ourselves."),
                      ("Limits", "It does not explain the idea, or prove the code asks Poincaré's exact question."),
                      ("Standing", "The theorem already rests on two decades of expert review.")]},
        10: {"title": "A question about shape, answered by watching shape change", "items": ["All mathematics: the people named in the sources. Explanation made with AI assistance.", "Sources: Perelman; Hamilton; Colding–Minicozzi; Kleiner–Lott; Morgan–Tian; Cao–Zhu; Qin et al."]},
    },
    "es": {
        1: {"title": "La forma de un mundo del que no puedes salir", "sub": "La conjetura de Poincaré, para todo el mundo"},
        2: {"title": "La prueba de la cuerda", "good": "La cuerda regresa", "bad": "La cuerda se atasca"},
        3: {"title": "Una dimensión más", "q": "Finito, sin borde, y toda cuerda regresa.", "q2": "¿Tiene que ser la 3-esfera?"},
        4: {"title": "Un siglo de intentos", "open": "sin resolver", "five": "dimensiones 5 y más", "four": "dimensión 4", "three": "dimensión 3", "start": "la pregunta"},
        5: {"title": "Dejar que la forma se suavice sola", "heat": "el calor se iguala", "flow": "el flujo de Ricci iguala la forma"},
        6: {"title": "El problema: un cuello que se estrangula", "cut": "Cortar, tapar y seguir", "pinch": "El cuello se estrangula primero"},
        7: {"title": "Perelman, 2002–2003", "items": ["Los puntos problemáticos se parecen a pocos modelos simples", "Cada corte elimina una cantidad definida de volumen", "Así, los cortes no se acumulan sin fin en tiempo finito"],
            "prize": "Medalla Fields y premio de un millón de dólares: rechazó ambos"},
        8: {"title": "Todo desaparece", "fwd": "Pasa la prueba de la cuerda: cada pieza se desvanece", "back": "Hacia atrás: solo se puede reconstruir una esfera"},
        9: {"title": "¿Puede comprobarlo una computadora?",
            "cards": [("Informado", "Un equipo informó en 2026 de una prueba en Lean. MathDB marca una versión como verificada."),
                      ("No lo hicimos", "Nosotros no ejecutamos esa enorme comprobación."),
                      ("Límites", "No explica la idea, ni demuestra que el código haga la pregunta exacta de Poincaré."),
                      ("Respaldo", "El teorema ya se apoya en dos décadas de revisión experta.")]},
        10: {"title": "Una pregunta sobre la forma, respondida observando cómo cambia", "items": ["Toda la matemática: las personas citadas. Explicación hecha con ayuda de IA.", "Fuentes: Perelman; Hamilton; Colding–Minicozzi; Kleiner–Lott; Morgan–Tian; Cao–Zhu; Qin y otros."]},
    },
}

rng = random.Random(11)
STARS = [(rng.random() * W, rng.random() * 880, rng.random()) for _ in range(260)]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ant(d, x, y, size=7):
    d.ellipse((x - size, y - size, x + size, y + size), fill=(30, 20, 15), outline=INK)
    d.ellipse((x + size * 0.6, y - size * 0.6, x + size * 1.6, y + size * 0.4), fill=(30, 20, 15), outline=INK)


def closed_curve(cx, cy, radius_fn, n=240, squash=1.0):
    pts = []
    for i in range(n + 1):
        a = i / n * math.tau
        r = radius_fn(a)
        pts.append((cx + r * math.cos(a), cy + squash * r * math.sin(a)))
    return pts


def scene1(d, t, T, x):
    cx, cy, r = W / 2, 510, 270
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=APPLE)
    d.ellipse((cx - r * 0.65, cy - r * 0.8, cx - r * 0.1, cy - r * 0.3), fill=(214, 92, 92))
    d.line((cx, cy - r, cx + 12, cy - r - 50), fill=(90, 60, 30), width=10)
    u = (t / T) * 2.4
    n = max(2, int(u * 90))
    trail = [(cx + r * 0.7 * math.cos(k / 90 * 1.9) * (1 - k / 500), cy + r * 0.55 * math.sin(k / 90 * 2.7)) for k in range(n)]
    d.line(trail, fill=ROPE, width=5)
    ant(d, *trail[-1], size=9)
    centered(d, W / 2, 70, x["title"], f_title(68), mix(BG, INK, fade(t, 0.4, 1.0)))
    centered(d, W / 2, 815, x["sub"], f_body(40), mix(BG, MUTED, fade(t, 1.5, 1.0)))


def scene2(d, t, T, x):
    title(d, x["title"], t)
    lx, rx, cy, r = 500, 1420, 480, 220
    d.ellipse((lx - r, cy - r, lx + r, cy + r), fill=APPLE)
    shrink = 1 - ease((t - T * 0.25) / (T * 0.3))
    if shrink > 0.03:
        d.ellipse((lx - 150 * shrink, cy - 100 * shrink, lx + 150 * shrink, cy + 100 * shrink), outline=ROPE, width=6)
    ant(d, lx, cy - 100 * shrink, 9)
    k = fade(t, T * 0.45)
    centered(d, lx, 730, x["good"], f_title(40), mix(BG, GREEN, k))
    k2 = fade(t, T * 0.55)
    d.ellipse((rx - 290, cy - 180, rx + 290, cy + 180), fill=DONUT)
    d.ellipse((rx - 95, cy - 55, rx + 95, cy + 55), fill=BG)
    wobble = 0.03 * math.sin(t * 9) * k2
    d.ellipse((rx - 170 * (1 + wobble), cy - 100 * (1 + wobble), rx + 170 * (1 + wobble), cy + 100 * (1 + wobble)), outline=ROPE, width=6)
    ant(d, rx + 170, cy, 9)
    centered(d, rx, 730, x["bad"], f_title(40), mix(BG, RED, k2))


def stars(d, level=1.0):
    for sx, sy, b in STARS:
        v = int(60 + 150 * b * level)
        d.ellipse((sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5), fill=(v, v, min(255, v + 25)))


def rocket_path(p):
    a = p * math.tau
    return W / 2 + 560 * math.sin(a), 470 + 250 * math.sin(2 * a) + 40 * math.cos(a)


def scene3(d, t, T, x):
    stars(d)
    title(d, x["title"], t)
    p = min(1.0, t / (T * 0.62))
    trail = [rocket_path(k / 300 * p) for k in range(int(300 * p) + 2)]
    d.line(trail, fill=ROPE, width=4)
    px, py = trail[-1]
    d.polygon([(px + 22, py), (px - 14, py - 12), (px - 14, py + 12)], fill=INK)
    centered(d, W / 2, 770, x["q"], f_body(42), mix(BG, INK, fade(t, T * 0.55)))
    centered(d, W / 2, 835, x["q2"], f_title(46), mix(BG, ORANGE, fade(t, T * 0.7)))


def scene4(d, t, T, x):
    title(d, x["title"], t)
    y = 480
    d.line((150, y, 1770, y), fill=(70, 84, 110), width=5)
    events = [(0.04, "1904", x["start"], MUTED), (0.35, "1961", x["five"], GREEN), (0.62, "1982", x["four"], GREEN)]
    for frac, year, label, color in events:
        k = fade(t, T * (0.05 + frac * 0.7))
        px = 150 + frac * 1620
        d.ellipse((px - 14, y - 14, px + 14, y + 14), fill=mix(BG, color, k))
        centered(d, px, y - 90, year, f_title(44), mix(BG, INK, k))
        centered(d, px, y + 34, label, f_body(32), mix(BG, color, k))
    k = fade(t, T * 0.68)
    px = 150 + 0.92 * 1620
    pulse = 0.5 + 0.5 * math.sin(t * 4)
    d.ellipse((px - 18, y - 18, px + 18, y + 18), fill=mix(BG, mix(RED, ORANGE, pulse), k))
    centered(d, px, y - 90, "?", f_title(58), mix(BG, ORANGE, k))
    centered(d, px, y + 34, x["three"], f_body(32), mix(BG, ORANGE, k))
    centered(d, px, y + 80, x["open"], f_body(28), mix(BG, RED, k))


def scene5(d, t, T, x):
    title(d, x["title"], t)
    tau = (t / T) * 4.2
    seeds = [0.95, 0.2, 0.7, 0.1, 0.85, 0.3, 0.6, 0.15, 0.9, 0.4]
    mean = sum(seeds) / len(seeds)
    damp = math.exp(-tau * 0.8)
    left, width = 120, 66
    for i, value in enumerate(seeds):
        v = mean + (value - mean) * damp
        d.rectangle((left + i * width, 300, left + (i + 1) * width - 4, 590), fill=mix((40, 90, 220), (235, 70, 50), v))
    centered(d, left + 5 * width, 620, x["heat"], f_body(36), INK)
    modes = [(3, 0.17, 0.4), (5, 0.12, 1.1), (7, 0.1, 2.3), (9, 0.06, 0.2)]

    def radius(a):
        r = 1.0
        for k, amp, phase in modes:
            r += amp * math.exp(-tau * (k / 4.0) ** 2) * math.cos(k * a + phase)
        return 225 * r

    points = closed_curve(1340, 445, radius)
    d.polygon(points, fill=(50, 92, 150), outline=BLUE)
    d.line(points, fill=BLUE, width=5)
    centered(d, 1340, 760, x["flow"], f_body(36), mix(BG, INK, fade(t, T * 0.2)))


def dumbbell(d, cx, cy, half, neck, ball, offset=0.0, side=0, color=(50, 92, 150)):
    """Dibuja un perfil de mancuerna. side: 0 entero, -1 solo izquierda, 1 solo derecha."""
    xs = [i / 200 * 2 - 1 for i in range(201)]
    if side:
        xs = [v for v in xs if v * side >= 0]
    top = []
    for v in xs:
        bump = math.exp(-((abs(v) - 0.62) ** 2) / (2 * 0.22**2))
        r = (neck + (ball - neck) * bump) * max(0.0, 1 - abs(v) ** 10) ** 0.5
        top.append((cx + side * offset + v * half, cy - r))
    bottom = [(px, 2 * cy - py) for px, py in top]
    d.polygon(top + bottom[::-1], fill=color, outline=BLUE)
    if side:
        capx = cx + side * offset
        capr = neck + 18
        d.pieslice((capx - capr, cy - capr, capx + capr, cy + capr), 90 if side > 0 else -90, 270 if side > 0 else 90, fill=color)


def scene6(d, t, T, x):
    title(d, x["title"], t)
    cx, cy = W / 2, 490
    cut = T * 0.62
    if t < cut:
        neck = 62 * (1 - ease(t / cut)) + 3
        ball = 215 - 25 * ease(t / cut)
        dumbbell(d, cx, cy, 720, neck, ball)
        k = fade(t, T * 0.3)
        centered(d, cx, 780, x["pinch"], f_title(40), mix(BG, ORANGE, k))
        if neck < 16:
            d.line((cx, cy - 70, cx, cy + 70), fill=RED, width=5)
    else:
        offset = 110 * ease((t - cut) / (T * 0.2))
        dumbbell(d, cx, cy, 720, 3, 190, offset, -1)
        dumbbell(d, cx, cy, 720, 3, 190, offset, 1)
        centered(d, cx, 780, x["cut"], f_title(42), mix(BG, GREEN, fade(t, cut)))


def scene7(d, t, T, x):
    title(d, x["title"], t)
    for i in range(3):
        k = fade(t, T * (0.03 + i * 0.05))
        left = 130 + i * 90
        top = 215 + i * 28
        d.rounded_rectangle((left, top, left + 220, top + 290), 10, fill=mix(BG, PANEL, k), outline=mix(BG, BLUE, k), width=3)
        for row in range(6):
            d.line((left + 26, top + 46 + row * 36, left + 194, top + 46 + row * 36), fill=mix(BG, MUTED, k * 0.7), width=4)
    items(d, 620, 240, 1180, x["items"], t, T, 40, start=0.15, span=0.45)
    k = fade(t, T * 0.76)
    d.rounded_rectangle((120, 690, W - 120, 800), 16, fill=mix(BG, PANEL, k))
    centered(d, W / 2, 720, x["prize"], f_title(38), mix(BG, ORANGE, k))


def scene8(d, t, T, x):
    title(d, x["title"], t)
    split = T * 0.5
    pieces = [(520, 450, 150), (960, 440, 180), (1400, 460, 130)]
    if t < split:
        p = t / split
        for i, (px, py, r0) in enumerate(pieces):
            factor = max(0.0, 1 - 1.15 * p * (1 + i * 0.06))
            r = r0 * math.sqrt(factor)
            if r > 1:
                d.ellipse((px - r, py - r, px + r, py + r), fill=(50, 92, 150), outline=BLUE, width=4)
        centered(d, W / 2, 770, x["fwd"], f_title(38), mix(BG, ORANGE, fade(t, 0.8)))
    else:
        p = ease((t - split) / (T - split) * 1.4)
        grow = min(1.0, p * 2)
        merge = max(0.0, (p - 0.5) * 2)
        for px, py, r0 in pieces:
            r = r0 * grow * (1 - merge * 0.6)
            qx = px + (960 - px) * merge
            qy = py + (450 - py) * merge
            d.ellipse((qx - r, qy - r, qx + r, qy + r), fill=(50, 92, 150), outline=BLUE, width=4)
        if merge > 0:
            r = 250 * merge
            d.ellipse((960 - r, 450 - r, 960 + r, 450 + r), fill=mix((50, 92, 150), GREEN, 0.35), outline=GREEN, width=5)
        centered(d, W / 2, 770, x["back"], f_title(38), mix(BG, GREEN, fade(t, split + 0.5)))


def scene9(d, t, T, x):
    title(d, x["title"], t)
    colors = [BLUE, ORANGE, RED, GREEN]
    for i, (head, body) in enumerate(x["cards"]):
        k = fade(t, T * (0.08 + i * 0.21))
        y = 170 + i * 180
        d.rounded_rectangle((120, y, W - 120, y + 160), 18, fill=mix(BG, PANEL, k))
        d.text((165, y + 22), head, font=f_title(38), fill=mix(BG, colors[i], k))
        text_block(d, 165, y + 76, body, f_body(32), mix(BG, INK, k), 1570, 6)


def scene10(d, t, T, x):
    cx, cy, r = W / 2, 400, 190
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=APPLE)
    shrink = max(0.0, 1 - t / (T * 0.45))
    if shrink > 0.03:
        d.ellipse((cx - 130 * shrink, cy - 90 * shrink, cx + 130 * shrink, cy + 90 * shrink), outline=ROPE, width=6)
    ant(d, cx, cy - 90 * shrink, 9)
    fnt = f_title(46)
    y = 625
    for line in wrap(d, x["title"], fnt, 1600):
        centered(d, W / 2, y, line, fnt, mix(BG, INK, fade(t, T * 0.5)))
        y += 58
    for i, line in enumerate(x["items"]):
        centered(d, W / 2, y + 14 + i * 50, line, f_body(30), mix(BG, MUTED, fade(t, T * (0.72 + 0.06 * i))))


DRAW = {1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7, 8: scene8, 9: scene9, 10: scene10}


def main():
    lang = sys.argv[1]
    still = "--still" in sys.argv
    only = int(sys.argv[sys.argv.index("--scene") + 1]) if "--scene" in sys.argv else None
    scenes = json.loads((PROJECT / "scenes.json").read_text(encoding="utf-8"))
    out = BASE / lang / "anim"
    out.mkdir(parents=True, exist_ok=True)
    background = Image.new("RGB", (W, H), BG)
    srt, offset, index, timeline = [], 0.0, 1, []
    for scene in scenes:
        n = scene["n"]
        spoken = wav_seconds(PROJECT / "out" / lang / f"scene_{n:02d}.wav")
        duration = spoken + PAD
        cues = sentence_cues(scene[lang], spoken)
        for start, end, text in cues:
            srt.append(f"{index}\n{fmt(offset + start)} --> {fmt(offset + end)}\n{text}\n")
            index += 1
        timeline.append({"n": n, "start": round(offset, 3), "duration": round(duration, 3)})
        offset += duration
        if only and n != only:
            continue
        if still:
            for name, moment in (("a", duration * 0.3), ("b", duration * 0.85)):
                image = background.copy()
                d = ImageDraw.Draw(image)
                DRAW[n](d, moment, duration, TEXT[lang][n])
                draw_caption(d, cues, moment)
                image.save(out / f"still_{n:02d}{name}.png")
            continue
        command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                   "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", str(out / f"scene_{n:02d}.mp4")]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        for frame in range(int(duration * FPS)):
            moment = frame / FPS
            image = background.copy()
            d = ImageDraw.Draw(image)
            DRAW[n](d, moment, duration, TEXT[lang][n])
            draw_caption(d, cues, moment)
            pipe.stdin.write(image.tobytes())
        pipe.stdin.close()
        pipe.wait()
        print(f"escena {n} lista", flush=True)
    (BASE / lang / f"poincare_{lang}.srt").write_text("\n".join(srt), encoding="utf-8")
    (BASE / lang / "timeline.json").write_text(json.dumps(timeline), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
