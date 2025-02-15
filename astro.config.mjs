// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import yaml from "@rollup/plugin-yaml";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

// https://astro.build/config
export default defineConfig({
  base: process.env.BASE ?? "/",
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
  vite: {
    plugins: [yaml()],
    esbuild: {
      keepNames: true,
    },
    build: {
      assetsInlineLimit: 0,
    },
  },
});
