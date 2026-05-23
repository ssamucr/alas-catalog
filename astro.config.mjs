// @ts-check
import { defineConfig, sharpImageService } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://alas-catalogo.samu0x.dev/',
  image: {
    service: sharpImageService(),
  },
  prefetch: {
    defaultStrategy: 'hover',
    prefetchAll: false,
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
