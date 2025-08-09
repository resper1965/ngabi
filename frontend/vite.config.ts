import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, './src'),
    },
  },
  server: {
    allowedHosts: [
      'ngabi.ness.tec.br',
      'api.ngabi.ness.tec.br',
      'n8n.ngabi.ness.tec.br',
      'localhost',
      '127.0.0.1'
    ],
    host: '0.0.0.0',
    port: 3000
  }
})
