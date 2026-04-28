"""Generate placeholder icons for the BB Reminder Chrome extension.

Pure stdlib (zlib + struct) so it runs anywhere Python 3 is installed.
Produces a flat rounded-square design: indigo background, white bell-ish
circle, small red notification dot. 2x supersampled for anti-aliased edges.

Run from the repo root: python3 scripts/generate_icons.py
"""

import os
import struct
import zlib

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "icons")

BG = (79, 70, 229, 255)        # indigo  #4F46E5
FG = (255, 255, 255, 255)      # white
ACCENT = (239, 68, 68, 255)    # red     #EF4444
CLEAR = (0, 0, 0, 0)

SIZES = [16, 32, 48, 128]
SS = 2  # supersampling factor


def png_bytes(width, height, pixels):
    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data))
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)

    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            raw.extend(pixels[y * width + x])

    idat = zlib.compress(bytes(raw), 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def in_rounded_rect(px, py, w, h, r):
    if px < r and py < r:
        return (px - r) ** 2 + (py - r) ** 2 <= r * r
    if px > w - r and py < r:
        return (px - (w - r)) ** 2 + (py - r) ** 2 <= r * r
    if px < r and py > h - r:
        return (px - r) ** 2 + (py - (h - r)) ** 2 <= r * r
    if px > w - r and py > h - r:
        return (px - (w - r)) ** 2 + (py - (h - r)) ** 2 <= r * r
    return 0 <= px <= w and 0 <= py <= h


def render_raw(size):
    s = size / 128
    corner_r = 22 * s
    bell_cx, bell_cy, bell_r = 64 * s, 68 * s, 30 * s
    dot_cx, dot_cy, dot_r = 98 * s, 30 * s, 13 * s

    out = []
    for y in range(size):
        for x in range(size):
            px, py = x + 0.5, y + 0.5
            if not in_rounded_rect(px, py, size, size, corner_r):
                out.append(CLEAR)
                continue
            if (px - dot_cx) ** 2 + (py - dot_cy) ** 2 <= dot_r * dot_r:
                out.append(ACCENT)
                continue
            if (px - bell_cx) ** 2 + (py - bell_cy) ** 2 <= bell_r * bell_r:
                out.append(FG)
                continue
            out.append(BG)
    return out


def render_aa(size):
    big = render_raw(size * SS)
    out = []
    for y in range(size):
        for x in range(size):
            r = g = b = a = 0
            for dy in range(SS):
                for dx in range(SS):
                    p = big[(y * SS + dy) * (size * SS) + (x * SS + dx)]
                    r += p[0]
                    g += p[1]
                    b += p[2]
                    a += p[3]
            n = SS * SS
            out.append((r // n, g // n, b // n, a // n))
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for size in SIZES:
        pixels = render_aa(size)
        data = png_bytes(size, size, pixels)
        path = os.path.join(OUT_DIR, f"icon-{size}.png")
        with open(path, "wb") as f:
            f.write(data)
        print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
