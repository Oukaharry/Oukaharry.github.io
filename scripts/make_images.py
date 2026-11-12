#!/usr/bin/env python3
"""Raster favicon and Open Graph image. Stdlib-adjacent: Pillow is a local build tool."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

GREEN = (14, 92, 74)
INK = (244, 239, 230)
PAPER = (22, 20, 15)
COPPER = (224, 162, 122)
MUTED = (195, 187, 174)


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def draw_mark(canvas, box):
    """HO monogram inside a square box (x, y, size)."""
    x, y, size = box
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x, y, x + size, y + size), radius=int(size * 0.22), fill=GREEN)
    # H
    h_left = x + size * 0.16
    h_top = y + size * 0.24
    h_bot = y + size * 0.76
    stem = size * 0.075
    mid = y + size * 0.47
    gap = size * 0.11
    draw.rectangle((h_left, h_top, h_left + stem, h_bot), fill=INK)
    right = h_left + stem + gap
    draw.rectangle((right, h_top, right + stem, h_bot), fill=INK)
    draw.rectangle((h_left, mid, right + stem, mid + stem * 0.85), fill=INK)
    # O
    cx = x + size * 0.74
    cy = y + size * 0.50
    r = size * 0.16
    width = max(2, int(size * 0.055))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=width)


def icon(size, radius_ratio=0.22):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    plate = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_mark(plate, (0, 0, size - 1))
    # draw_mark already paints a rounded plate; crop to exact size
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mark = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_mark(mark, (0, 0, size - 1))
    return mark


def make_icons():
    mark = icon(512)
    mark.resize((180, 180), Image.Resampling.LANCZOS).save(ASSETS / "apple-touch-icon.png")
    mark.resize((32, 32), Image.Resampling.LANCZOS).save(ASSETS / "favicon-32.png")
    small = mark.resize((16, 16), Image.Resampling.LANCZOS)
    small.save(ASSETS / "favicon-16.png")
    # ICO needs a real file; Pillow accepts PNG-backed sizes.
    mark.resize((32, 32), Image.Resampling.LANCZOS).save(
        ASSETS / "favicon.ico", sizes=[(16, 16), (32, 32)]
    )


def make_og():
    width, height = 1200, 630
    img = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 22, height), fill=GREEN)

    serif = font("/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf", 68)
    serif_small = font("/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf", 64)
    sans = font("/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf", 28)
    sans_reg = font("/usr/share/fonts/truetype/macos/Inter-Regular.ttf", 28)
    mono = font("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 22)

    draw.text((88, 120), "SOFTWARE DEVELOPER", font=sans, fill=COPPER)
    draw.text((88, 180), "Harrison Odhiambo", font=serif, fill=INK)
    draw.text((88, 258), "Ouka", font=serif_small, fill=INK)
    draw.text((88, 360), "Harry Ouka   ·   Ouka Harry", font=sans_reg, fill=MUTED)
    draw.text((88, 420), "Nairobi, Kenya", font=sans_reg, fill=INK)
    draw.text((88, 530), "oukaharry.github.io", font=mono, fill=COPPER)

    # Mark in the corner
    badge = icon(168)
    img.paste(badge, (940, 80), badge)
    img.save(ASSETS / "og.png", optimize=True)


if __name__ == "__main__":
    make_icons()
    make_og()
    print("wrote icons and og.png")
