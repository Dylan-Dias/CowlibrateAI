import vercel from '@sveltejs/adapter-vercel';
import { sveltePreprocess } from 'svelte-preprocess';
import { fileURLToPath, URL } from 'node:url';

const config = {
  preprocess: sveltePreprocess(),
  kit: {
    adapter: vercel(),  // <-- This must be here, NOT adapter-auto
    alias: {
      $components: fileURLToPath(new URL('./src/lib/components', import.meta.url)),
      $Login: fileURLToPath(new URL('./src/lib/routes/Login', import.meta.url)),
      $ResetPassword: fileURLToPath(new URL('./src/lib/routes/ResetPassword', import.meta.url)),
    }
  }
};

export default config;
