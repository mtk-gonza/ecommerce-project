import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      // ✅ Path alias @ → src/
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  
  server: {
    port: 5173,
    open: true,  // Abrir navegador automáticamente
    proxy: {
      // ✅ Proxy para evitar CORS en desarrollo (opcional)
      '/api': {
        target: 'http://localhost:3050',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});