import { defineCollection, z } from "astro:content";
import { glob, file } from "astro/loaders";

const blog = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "src/content/blog",
  }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
  }),
});

const pages = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "src/content/pages",
  }),
  schema: z.object({ title: z.string() }),
});

export const collections = { blog, pages };
