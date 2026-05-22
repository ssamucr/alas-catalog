// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://alas-catalogo.samu0x.dev/',
  prefetch: {
    defaultStrategy: 'hover',
    prefetchAll: false,
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
