"""
make_icon.py — generates icon.ico for ExtraDataGenerator.
Draws a trash bin throwing out 0s and 1s.
"""

from pathlib import Path


def _pillow_icon(path: Path) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False

    import math

    SIZE = 256
    img  = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d    = ImageDraw.Draw(img)

    # ── bin body ──────────────────────────────────────────────────────────────
    # Trapezoid: slightly narrower at top, wider at bottom
    bx1, bx2 = 62, 178      # top-left / top-right x of body
    bx3, bx4 = 54, 186      # bottom-left / bottom-right x
    by1 = 110                # top y of body
    by2 = 220                # bottom y of body

    body_pts = [(bx1, by1), (bx2, by1), (bx4, by2), (bx3, by2)]
    d.polygon(body_pts, fill=(80, 90, 105, 255))
    d.polygon(body_pts, outline=(130, 145, 165, 255), width=3)

    # Vertical ribs on bin
    for frac in [0.33, 0.67]:
        rx = int(bx1 + frac * (bx2 - bx1))
        bx_bot = int(bx3 + frac * (bx4 - bx3))
        d.line([(rx, by1 + 6), (bx_bot, by2 - 6)],
               fill=(110, 125, 145, 255), width=3)

    # Horizontal lines on bin
    for frac in [0.35, 0.65]:
        ly = int(by1 + frac * (by2 - by1))
        lx_left  = int(bx1 + frac * (bx3 - bx1))
        lx_right = int(bx2 + frac * (bx4 - bx2))
        d.line([(lx_left + 4, ly), (lx_right - 4, ly)],
               fill=(110, 125, 145, 220), width=2)

    # ── bin lid ───────────────────────────────────────────────────────────────
    lid_x1, lid_x2 = 52, 188
    lid_y1, lid_y2 = 95, 112
    d.rounded_rectangle([lid_x1, lid_y1, lid_x2, lid_y2], radius=6,
                        fill=(100, 112, 128, 255),
                        outline=(140, 155, 175, 255), width=3)

    # Lid handle (small rect in centre)
    hx1, hx2 = 108, 142
    hy1, hy2 = 82, 97
    d.rounded_rectangle([hx1, hy1, hx2, hy2], radius=5,
                        fill=(100, 112, 128, 255),
                        outline=(140, 155, 175, 255), width=3)

    # ── flying 0s and 1s ejected from the top ────────────────────────────────
    # Each tuple: (x, y, char, size, angle, alpha)
    bits = [
        # left arc — going up-left
        (88,  74, "0", 22, -25, 255),
        (62,  52, "1", 18, -40, 230),
        (42,  34, "0", 14, -55, 180),
        (28,  22, "1", 11, -65, 120),
        # right arc — going up-right
        (148, 68, "1", 22,  20, 255),
        (174, 48, "0", 18,  38, 230),
        (196, 32, "1", 14,  52, 180),
        (212, 20, "0", 11,  62, 120),
        # centre — going straight up
        (116, 60, "1", 20,   5, 240),
        (122, 38, "0", 16,  -8, 190),
    ]

    for (bx, by, char, sz, angle_deg, alpha) in bits:
        # Create a small sub-image for each character so we can rotate it
        pad   = sz + 4
        ci    = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
        cd    = ImageDraw.Draw(ci)

        # Try to load a font; fall back to default
        try:
            fnt = ImageFont.truetype("arial.ttf", sz)
        except Exception:
            try:
                fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
            except Exception:
                fnt = ImageFont.load_default()

        # Amber/gold colour for bits, slightly dimmed by alpha
        col = (255, 220, 60, alpha)
        cd.text((pad - sz // 3, pad - sz // 2), char, font=fnt, fill=col)

        rot = ci.rotate(angle_deg, expand=False)
        img.paste(rot, (bx - pad, by - pad), rot)

    # ── motion-blur lines showing trajectory ──────────────────────────────────
    arc_col = (220, 170, 0, 90)
    # Left arc
    for t in range(8):
        frac  = t / 7
        ax    = int(120 - 90 * frac)
        ay    = int(100 - 80 * frac - 20 * (frac ** 2))
        r     = max(1, 4 - t // 2)
        d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=arc_col)
    # Right arc
    for t in range(8):
        frac  = t / 7
        ax    = int(136 + 90 * frac)
        ay    = int(100 - 80 * frac - 20 * (frac ** 2))
        r     = max(1, 4 - t // 2)
        d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=arc_col)

    img.save(str(path), format="ICO",
             sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (256, 256)])
    return True


def _fallback_icon(path: Path) -> None:
    """Minimal valid 16×16 ICO — pure Python, no dependencies."""
    import struct

    def bmp_16x16(fg=(255, 255, 255), bg=(27, 94, 166)):
        pixels = []
        for y in range(16):
            row = []
            for x in range(16):
                inside = 2 <= x <= 13 and 2 <= y <= 13
                row.extend(list(fg if inside else bg) + [255])
            pixels.append(row)

        w, h      = 16, 16
        bpp       = 32
        row_bytes = w * 4
        dib = struct.pack("<IiiHHIIiiII",
                          40, w, h * 2, 1, bpp, 0,
                          row_bytes * h * 2, 0, 0, 0, 0)
        xor_rows = b""
        for row in reversed(pixels):
            for px in row:
                xor_rows += struct.pack("BBBB", px[2], px[1], px[0], px[3])
        and_rows = b"\x00" * (((w + 31) // 32) * 4 * h)
        return dib + xor_rows + and_rows

    bmp  = bmp_16x16()
    ico  = struct.pack("<HHH", 0, 1, 1)
    ico += struct.pack("<BBBBHHIi", 16, 16, 0, 0, 1, 32, len(bmp), 6 + 16)
    ico += bmp
    path.write_bytes(ico)


if __name__ == "__main__":
    out = Path("icon.ico")
    if _pillow_icon(out):
        print(f"icon.ico written (Pillow, multi-resolution)  →  {out}")
    else:
        _fallback_icon(out)
        print(f"icon.ico written (fallback 16×16)  →  {out}")
