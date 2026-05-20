import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const products = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/products' }),
  schema: z.object({
    /** Nombre del producto */
    title: z.string(),
    /** Descripción corta visible en tarjeta y página */
    description: z.string(),
    /** Precio en pesos / moneda local */
    price: z.number(),
    /** Categoría del producto */
    category: z.enum(['Anillos', 'Collares', 'Aretes', 'Pulseras', 'Piercings']),
    /** URL o path de la imagen principal */
    image: z.string(),
    /** Imágenes adicionales para galería */
    gallery: z.array(z.string()).optional(),
    /** Disponibilidad */
    inStock: z.boolean().default(true),
    /** Material principal */
    material: z.string().optional(),
    /** Color */
    color: z.string().optional(),
    /** Aparece destacado en la página principal */
    featured: z.boolean().default(false),
    /** Orden de aparición (menor = primero) */
    order: z.number().default(0),
  }),
});

export const collections = { products };
