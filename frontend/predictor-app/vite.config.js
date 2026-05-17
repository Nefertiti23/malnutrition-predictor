import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// This tells Vite how to cleanly parse and translate .vue files
export default defineConfig({
  plugins: [vue()],
})