// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { unified } from '@astrojs/markdown-remark';

export default defineConfig({
  site: 'https://brief.vitalyr.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap()],
  markdown: {
    // 用 unified（remark/rehype）管线，以便 remark-math + rehype-katex 在构建时渲染公式
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [[rehypeKatex, { throwOnError: false, strict: 'ignore' }]],
    }),
  },
});
