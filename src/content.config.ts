import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// 每期一个文件：src/content/issues/<年>/<YYYY-MM-DD>.md
// id 即相对路径去掉 .md，例如 "2026/2026-11-23"，页面地址 /issues/2026/2026-11-23/
const issues = defineCollection({
  loader: glob({
    pattern: '*/*.md',
    base: './src/content/issues',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    title: z.string().min(1),
    issue: z.number().int().positive(),
    date: z.coerce.date(),
    description: z.string().optional(),
  }),
});

export const collections = { issues };
