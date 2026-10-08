# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(r"C:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")

src = root / "Fotos_proyectos" / "webp" / "perfil" / "osvaldo-vega.webp"

out_dir = root / "assets" / "seo"
out_dir.mkdir(parents=True, exist_ok=True)

out = out_dir / "osvaldo-vega-og.jpg"

W, H = 1200, 630

BG = "#F4F6F8"
TEXT = "#07111F"
SECONDARY = "#334155"
ACCENT = "#0E7490"

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# =========================================================
# FUENTES
# =========================================================

bold_candidates = [
    Path(r"C:\Windows\Fonts\OpenSans-ExtraBold.ttf"),
    Path(r"C:\Windows\Fonts\OpenSans-Bold.ttf"),
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
]

regular_candidates = [
    Path(r"C:\Windows\Fonts\OpenSans-Regular.ttf"),
    Path(r"C:\Windows\Fonts\arial.ttf"),
]

def find_font(candidates, size):
    for font_path in candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)

    raise FileNotFoundError(
        "No se encontró una fuente compatible en C:\\Windows\\Fonts"
    )

font_logo = find_font(bold_candidates, 34)
font_name = find_font(bold_candidates, 58)
font_role = find_font(bold_candidates, 28)
font_field = find_font(bold_candidates, 34)
font_domain = find_font(regular_candidates, 23)

# =========================================================
# RETRATO
# =========================================================

if not src.exists():
    raise FileNotFoundError(f"No existe la fotografía: {src}")

portrait = Image.open(src).convert("RGB")

photo_x = 820
photo_y = 55
photo_w = 300
photo_h = 520

target_ratio = photo_w / photo_h
source_ratio = portrait.width / portrait.height

if source_ratio > target_ratio:
    new_w = int(portrait.height * target_ratio)
    left = (portrait.width - new_w) // 2
    portrait = portrait.crop(
        (left, 0, left + new_w, portrait.height)
    )
else:
    new_h = int(portrait.width / target_ratio)

    # Mantener preferencia del encuadre hacia rostro/parte superior.
    top = max(
        0,
        min(
            portrait.height - new_h,
            int((portrait.height - new_h) * 0.28)
        )
    )

    portrait = portrait.crop(
        (0, top, portrait.width, top + new_h)
    )

portrait = portrait.resize(
    (photo_w, photo_h),
    Image.Resampling.LANCZOS
)

canvas.paste(portrait, (photo_x, photo_y))

# Acento visual discreto
draw.rectangle(
    (
        photo_x - 12,
        photo_y,
        photo_x - 5,
        photo_y + photo_h
    ),
    fill=ACCENT
)

# =========================================================
# TEXTOS
#
# Se usan escapes Unicode deliberadamente para evitar
# problemas de codificación de PowerShell/consola.
# =========================================================

left = 75

logo = "OVO."
name = "Osvaldo Vega Oses"
role = "Soci\u00f3logo"
line1 = "Medio Humano \u00b7 Participaci\u00f3n"
line2 = "Ciudadana \u00b7 An\u00e1lisis socio-territorial"
domain = "osvaldovega.cl"

draw.text(
    (left, 60),
    logo,
    font=font_logo,
    fill=TEXT
)

draw.text(
    (left, 145),
    name,
    font=font_name,
    fill=TEXT
)

draw.text(
    (left, 225),
    role,
    font=font_role,
    fill=ACCENT
)

draw.text(
    (left, 315),
    line1,
    font=font_field,
    fill=TEXT
)

draw.text(
    (left, 360),
    line2,
    font=font_field,
    fill=TEXT
)

draw.text(
    (left, 520),
    domain,
    font=font_domain,
    fill=SECONDARY
)

# =========================================================
# EXPORTACIÓN
# =========================================================

if out.exists():
    out.unlink()

canvas.save(
    out,
    "JPEG",
    quality=90,
    optimize=True,
    progressive=True
)

# Validación del archivo resultante
with Image.open(out) as check:
    assert check.size == (1200, 630), check.size
    assert check.format == "JPEG", check.format

print()
print("=== OG IMAGE GENERADA ===")
print(out)
print("Dimensiones: 1200 x 630 px")
print(f"Tamano archivo: {out.stat().st_size / 1024:.1f} KB")
print()
print("Textos Unicode usados:")
print(role)
print(line1)
print(line2)
print()
print("OG IMAGE: OK")
