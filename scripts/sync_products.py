"""
excel_to_md.py
Reads products.xlsx and generates one .md file per row in the "products" sheet.
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert a title string to a safe filename slug."""
    # Normalize unicode characters (e.g. accented letters → base letter)
    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    # Replace spaces and non-alphanumeric characters with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    return text


def bool_value(value) -> str:
    """Return 'true' or 'false' string for boolean-like values."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return "true" if bool(value) else "false"
    if isinstance(value, str):
        return "true" if value.strip().lower() in ("true", "1", "yes", "si", "sí") else "false"
    return "false"


def str_value(value) -> str:
    """Return a clean string, handling NaN/None gracefully."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def build_frontmatter(row: pd.Series) -> str:
    """Build the YAML frontmatter block from a DataFrame row."""
    lines = [
        "---",
        f'title: "{str_value(row["title"])}"',
        f'description: "{str_value(row["description"])}"',
        f'price: {str_value(row["price"])}',
        f'category: "{str_value(row["category"])}"',
        f'image: "{str_value(row["image"])}"',
        f'inStock: {bool_value(row["inStock"])}',
        f'material: "{str_value(row["material"])}"',
        f'color: "{str_value(row["color"])}"',
        f'featured: {bool_value(row["featured"])}',
        f'order: {str_value(row["order"])}',
        "---",
    ]
    return "\n".join(lines)


def build_md_content(row: pd.Series) -> str:
    """Combine frontmatter + body into a complete Markdown document."""
    frontmatter = build_frontmatter(row)
    body = "" if pd.isna(row["body"]) else str(row["body"])
    # Interpret literal \n sequences as real newlines (preserve * as-is)
    body = body.replace("\\n", "\n")
    # Ensure a single blank line separates frontmatter from body
    return f"{frontmatter}\n\n{body}\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    script_dir = Path(__file__).parent.resolve()
    excel_path = script_dir / "products.xlsx"

    if not excel_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {excel_path}")

    print(f"Leyendo: {excel_path}")
    df = pd.read_excel(excel_path, sheet_name="products", engine="openpyxl", dtype=str)

    # Coerce boolean columns after reading as str
    for bool_col in ("inStock", "featured"):
        if bool_col not in df.columns:
            raise ValueError(f"Columna requerida no encontrada en el Excel: '{bool_col}'")

    required_columns = {
        "title", "description", "price", "category", "image",
        "inStock", "material", "color", "featured", "order", "body",
    }
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Columnas faltantes en la hoja 'products': {missing}")

    created = 0
    skipped = 0

    for idx, row in df.iterrows():
        title = str_value(row["title"])
        if not title:
            print(f"  [SKIP] Fila {idx + 2}: título vacío, se omite.")
            skipped += 1
            continue

        slug = slugify(title)
        if not slug:
            print(f"  [SKIP] Fila {idx + 2}: no se pudo generar slug para '{title}', se omite.")
            skipped += 1
            continue

        filename = script_dir / f"{slug}.md"
        content = build_md_content(row)

        filename.write_text(content, encoding="utf-8")
        print(f"  [OK]   {filename.name}")
        created += 1

    print(f"\nListo. Archivos creados: {created} | Omitidos: {skipped}")


if __name__ == "__main__":
    main()
