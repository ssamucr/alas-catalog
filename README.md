# Alas — Catálogo de joyería fina

Catálogo web para **Alas**, una marca de joyería fina: los clientes exploran las piezas, las filtran por categoría,
las buscan por nombre y consultan por una pieza por WhatsApp o Instagram. Es un sitio estático y rápido, pensado para
que quien administra el negocio actualice el inventario desde un Excel, sin tocar código.

**Demo:** <https://alas-catalog.vercel.app>

## Qué incluye

- **Catálogo con 49 piezas** en 7 categorías: anillos, collares, aretes, pulseras, piercings, brazaletes y relojes.
- **Filtros por categoría** y **búsqueda difusa** (tolera errores de escritura) con [Fuse.js](https://www.fusejs.io), en un modal.
- **Página por producto** (`/productos/<nombre>`) con galería de imágenes, precio en USD, material, color y disponibilidad.
- **Contacto por pieza**: botón de WhatsApp con un mensaje ya escrito ("Me interesa el producto…, ¿está disponible?") y enlace a Instagram.
- **Piezas destacadas** en la página principal y orden configurable.
- **Imágenes optimizadas** (WebP) y precarga de páginas al pasar el cursor, para una navegación fluida.
- **Responsive**, con menú móvil.

## Tecnologías

[Astro](https://astro.build) 6 (colecciones de contenido), [Tailwind CSS](https://tailwindcss.com) 4,
[Fuse.js](https://www.fusejs.io) y [sharp](https://sharp.pixelplumbing.com); scripts en Python (pandas, Pillow) para el inventario.
Desplegado en Vercel.

## Cómo se actualiza el inventario

Cada producto es un archivo Markdown en `src/content/products/`. En lugar de editarlos a mano, se generan desde una hoja de Excel:

1. Edita la hoja `products` de `data/products.xlsx`. Columnas: `title`, `description`, `price`, `category`,
   `inStock`, `material`, `color`, `featured` y `order`.
2. Pon las fotos originales (JPG o PNG) en una carpeta `raw_images/` con el nombre del producto
   (`anillo-corazon.jpg`; para la galería, `anillo-corazon-2.jpg`, `anillo-corazon-3.jpg`…) y conviértelas a WebP:

   ```bash
   pip install Pillow
   python scripts/convert_images.py --quality 80
   ```

3. Genera los archivos de producto a partir del Excel:

   ```bash
   pip install pandas openpyxl
   python scripts/sync_products.py
   ```

## Ejecutar en local

Requiere Node.js 22.12 o superior.

```bash
pnpm install
pnpm dev        # http://localhost:4321
```

| Comando | Qué hace |
| --- | --- |
| `pnpm dev` | Servidor de desarrollo |
| `pnpm build` | Compilación de producción en `dist/` |
| `pnpm preview` | Sirve la compilación para probarla |

## Estructura

```
data/products.xlsx          Inventario (fuente de verdad)
scripts/                    Conversión de imágenes y generación de productos
src/content/products/       Un .md por producto (generados)
src/assets/images/          Fotos optimizadas en WebP
src/components/             Navbar, Hero, filtros, búsqueda, tarjetas y galería
src/pages/                  Página principal y página de producto
```
