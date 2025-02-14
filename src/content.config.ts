import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({
    pattern: ["**/*.{md,mdx}", "!**/README.md"],
    base: "src/content/blog",
  }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
    author: z.string().or(z.string().array()),
    draft: z.boolean().optional(),
    tags: z.string().array().optional(),
    ctf_id: z.string().optional(),
  }),
});

const events = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "src/content/events",
  }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
  }),
});

const pages = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "src/content/pages",
  }),
  schema: z.object({ title: z.string() }),
});

export const collections = { blog, events, pages };
