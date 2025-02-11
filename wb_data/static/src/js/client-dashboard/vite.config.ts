import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    minify: false,
    rollupOptions: {
      output: {
        entryFileNames: "index.js",
        chunkFileNames: "[name].js",
        assetFileNames: (assetInfo) => {
          const ext = assetInfo.name.split(".").pop();
          return ext === "css" ? "index.css" : "[name].[ext]";
        },
      },
    },
  },
});
