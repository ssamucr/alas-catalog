"""
convert_images.py
Converts JPEG/PNG images from /raw_images to optimized WebP
and places them in /public/products/.

Usage:
    python scripts/convert_images.py [--quality 75]
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow no está instalado. Ejecuta: pip install Pillow")


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
DEFAULT_QUALITY = 75 # 80-85 es un buen balance calidad/tamaño para WebP


def convert_image(src: Path, dest: Path, quality: int) -> None:
    """Convierte una imagen a WebP y la guarda en dest."""
    with Image.open(src) as img:
        # Convertir RGBA → RGB si el destino no soporta transparencia (JPEG source)
        # Para WebP se puede mantener RGBA, pero normalizamos modos raros.
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "transparency" in img.info else "RGB")
        img.save(dest, format="WEBP", quality=quality, method=6)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convierte imágenes a WebP optimizado.")
    parser.add_argument(
        "--quality",
        type=int,
        default=DEFAULT_QUALITY,
        metavar="N",
        help=f"Calidad WebP 1-100 (defecto: {DEFAULT_QUALITY})",
    )
    args = parser.parse_args()

    if not (1 <= args.quality <= 100):
        sys.exit("--quality debe estar entre 1 y 100.")

    project_root = Path(__file__).parent.parent.resolve()
    input_dir = project_root / "raw_images"
    output_dir = project_root / "public" / "products"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        sys.exit(f"Carpeta de origen no encontrada: {input_dir}")

    sources = [
        f for f in input_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not sources:
        print(f"No se encontraron imágenes JPEG/PNG en: {input_dir}")
        return

    converted = 0
    errors = 0

    for src in sorted(sources):
        dest = output_dir / f"{src.stem}.webp"
        try:
            convert_image(src, dest, args.quality)
            src_kb = src.stat().st_size / 1024
            dest_kb = dest.stat().st_size / 1024
            saving = (1 - dest_kb / src_kb) * 100 if src_kb else 0
            print(f"  [OK]  {src.name}  →  {dest.name}  ({src_kb:.0f} KB → {dest_kb:.0f} KB, -{saving:.0f}%)")
            converted += 1
        except Exception as exc:
            print(f"  [ERR] {src.name}: {exc}")
            errors += 1

    print(f"\nListo. Convertidas: {converted} | Errores: {errors}")
    print(f"Destino: {output_dir}")


if __name__ == "__main__":
    main()
