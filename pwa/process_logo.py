#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Détoure le logo officiel, prépare les variantes et les icônes PWA."""

import os
import shutil
from PIL import Image, ImageDraw, ImageFilter

SRC = r"C:\Users\othni\.dsh\attachments\v1\objects\c7\c7983a29b8fc155172d1e9fbf50ee83d22e0f2b929a69b689786fb575f8121b0"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

DARK = (16, 11, 9)


def cutout(img):
    """Rend transparent le fond blanc connecté aux bords."""
    rgb = img.convert("RGB")
    # le JPEG d'origine a un liseré noir de 2-3 px sur tout le pourtour
    rgb = rgb.crop((6, 6, rgb.width - 6, rgb.height - 6))
    w, h = rgb.size
    px = rgb.load()

    # masque des pixels quasi blancs
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 240 and g > 240 and b > 240:
                mp[x, y] = 255

    # on ne garde que la zone blanche reliée au bord (coin haut-gauche)
    ImageDraw.floodfill(mask, (2, 2), 128, thresh=14)
    mpx = mask.load()

    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if mpx[x, y] == 128:
                ap[x, y] = 0

    alpha = alpha.filter(ImageFilter.MinFilter(3))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))

    out = rgb.convert("RGBA")
    out.putalpha(alpha)

    # désempâtement du blanc sur les pixels de bord
    op = out.load()
    for y in range(h):
        for x in range(w):
            a = op[x, y][3]
            if 0 < a < 250:
                k = a / 255.0
                r, g, b = op[x, y][:3]
                r = max(0, min(255, int((r - 255 * (1 - k)) / max(k, 0.05))))
                g = max(0, min(255, int((g - 255 * (1 - k)) / max(k, 0.05))))
                b = max(0, min(255, int((b - 255 * (1 - k)) / max(k, 0.05))))
                op[x, y] = (r, g, b, a)

    return out


def trim(img, pad_ratio=0.02):
    bbox = img.split()[-1].getbbox()
    if not bbox:
        return img
    pad = int(max(img.size) * pad_ratio)
    bbox = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
            min(bbox[2] + pad, img.width), min(bbox[3] + pad, img.height))
    return img.crop(bbox)


def on_dark(img, size, glow=True):
    """Compose le logo sur un fond charbon avec halo."""
    canvas = Image.new("RGBA", (size, size), DARK + (255,))

    if glow:
        g = Image.new("L", (size, size), 0)
        dg = ImageDraw.Draw(g)
        r = int(size * 0.55)
        for i in range(24, 0, -1):
            k = i / 24
            dg.ellipse([size / 2 - r * k, size * 0.54 - r * k,
                        size / 2 + r * k, size * 0.54 + r * k],
                       fill=int(62 * (1 - k) ** 1.4))
        layer = Image.new("RGBA", (size, size), (193, 18, 31, 255))
        layer.putalpha(g)
        canvas = Image.alpha_composite(canvas, layer)

        g2 = Image.new("L", (size, size), 0)
        d2 = ImageDraw.Draw(g2)
        r2 = int(size * 0.34)
        d2.ellipse([size / 2 - r2, size * 0.56 - r2, size / 2 + r2, size * 0.56 + r2], fill=42)
        l2 = Image.new("RGBA", (size, size), (247, 183, 51, 255))
        l2.putalpha(g2.filter(ImageFilter.GaussianBlur(size * 0.05)))
        canvas = Image.alpha_composite(canvas, l2)

    inner = int(size * 0.84)
    logo = img.copy()
    logo.thumbnail((inner, inner), Image.LANCZOS)
    canvas.alpha_composite(logo, ((size - logo.width) // 2, (size - logo.height) // 2))
    return canvas


def save_opt(img, path, colors=220):
    """PNG quantifié : 6× plus léger, indispensable en 3G."""
    q = img.convert("RGBA").quantize(colors=colors, method=Image.FASTOCTREE,
                                     dither=Image.FLOYDSTEINBERG)
    q.save(path, optimize=True)
    print(path, os.path.getsize(path) // 1024, "Ko")


def main():
    src = Image.open(SRC)
    cut = trim(cutout(src), 0.015)
    save_opt(cut, os.path.join(OUT, "logo.png"))

    # variante réduite pour le header / footer (même visuel, plus léger)
    mark = cut.copy()
    mark.thumbnail((460, 460), Image.LANCZOS)
    save_opt(mark, os.path.join(OUT, "logo-mark.png"))

    # icônes PWA
    for size in (512, 192):
        save_opt(on_dark(cut, size), os.path.join(OUT, f"icon-{size}.png"))

    mask_icon = Image.new("RGBA", (512, 512), DARK + (255,))
    logo = cut.copy()
    logo.thumbnail((330, 330), Image.LANCZOS)
    mask_icon.alpha_composite(logo, ((512 - logo.width) // 2, (512 - logo.height) // 2))
    save_opt(mask_icon, os.path.join(OUT, "icon-maskable-512.png"))

    save_opt(on_dark(cut, 180), os.path.join(OUT, "apple-touch-icon.png"))

    shutil.copyfile(SRC, os.path.join(OUT, "logo-source.jpg"))
    print("ok")


main()
