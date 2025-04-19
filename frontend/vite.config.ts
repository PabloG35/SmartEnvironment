import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: ['0367-101-9-57-65.ngrok-free.app'],
    hmr: {
      host: '0367-101-9-57-65.ngrok-free.app',
      protocol: 'wss'
    }
  }
});
