#!/usr/bin/env python3
# Copyright 2026 The Leto Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.

"""Draws the background of Leto's installer window.

Leto's light "paper", with a soft graphite shade from above and a fine grain,
like the app icon, an arrow from Leto to Applications and a short
instruction. Finder draws the icons' labels in black over any background, so
the window has to be light for them to read.
Writes background.png and background@2x.png next to this script.

Usage: python3 make_background.py   (needs Pillow)
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# The window, in points. Keep in step with dmg_settings.py.
WIDTH, HEIGHT = 660, 400
APP_X, APPS_X, ICON_Y = 170, 490, 150
# Clear of Finder's path and status bars, which some people keep on for
# every window.
CAPTION_Y = 268

TOP = (247, 247, 249)
BOTTOM = (236, 236, 240)
SHADE = (196, 196, 206)
FONT = "/System/Library/Fonts/SFNS.ttf"


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def draw(scale):
    w, h = WIDTH * scale, HEIGHT * scale
    image = Image.new("RGB", (w, h))

    # A gentle vertical gradient.
    pixels = image.load()
    for y in range(h):
        row = lerp(TOP, BOTTOM, y / (h - 1))
        for x in range(w):
            pixels[x, y] = row

    # A soft shade from above, eased over its radius so it fades without
    # bands.
    glow = Image.new("L", (w, h), 0)
    glow_pixels = glow.load()
    cx, cy = w / 2, -h * 0.35
    radius = h * 1.05
    for y in range(h):
        for x in range(w):
            d = math.hypot((x - cx) / 1.35, y - cy) / radius
            if d < 1:
                glow_pixels[x, y] = round(255 * (1 - d) ** 2.4 * 0.22)
    image = Image.composite(Image.new("RGB", (w, h), SHADE), image, glow)

    # Fine grain, as on the icon.
    rng = random.Random(7)
    noise = Image.new("L", (w, h))
    noise.putdata([rng.randint(0, 255) for _ in range(w * h)])
    noise = noise.filter(ImageFilter.GaussianBlur(0.35 * scale))
    grain = Image.merge("RGB", (noise, noise, noise))
    image = Image.blend(image, grain, 0.025)

    draw = ImageDraw.Draw(image)

    # A slim arrow between the two icons.
    s = scale
    y = ICON_Y * s
    x0, x1 = (APP_X + 78) * s, (APPS_X - 78) * s
    stroke = round(2 * s)
    colour = (60, 60, 68)
    arrow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(arrow)
    # A dashed shaft that fades in toward the head.
    dash, gap = 7 * s, 6 * s
    x = x0
    while x + dash < x1 - 10 * s:
        t = (x - x0) / (x1 - x0)
        alpha = round(50 + 110 * t)
        adraw.line([(x, y), (x + dash, y)], fill=colour + (alpha,),
                   width=stroke)
        x += dash + gap
    head = 9 * s
    adraw.line([(x1 - head, y - head), (x1, y), (x1 - head, y + head)],
               fill=colour + (170,), width=stroke, joint="curve")
    for px, py in ((x1 - head, y - head), (x1, y), (x1 - head, y + head)):
        r = stroke / 2
        adraw.ellipse([px - r, py - r, px + r, py + r], fill=colour + (170,))
    image = Image.alpha_composite(image.convert("RGBA"), arrow).convert("RGB")
    draw = ImageDraw.Draw(image)

    # The instruction.
    font = ImageFont.truetype(FONT, 13 * s)
    try:
        font.set_variation_by_name("Medium")
    except Exception:
        pass
    text = "Drag Leto to Applications to install"
    box = draw.textbbox((0, 0), text, font=font)
    draw.text(((w - (box[2] - box[0])) / 2, CAPTION_Y * s), text, font=font,
              fill=(120, 120, 130))
    return image


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    draw(1).save(os.path.join(here, "background.png"), optimize=True)
    draw(2).save(os.path.join(here, "background@2x.png"), optimize=True)


if __name__ == "__main__":
    main()
