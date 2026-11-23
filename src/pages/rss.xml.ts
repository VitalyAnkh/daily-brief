import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getIssues, issueUrl, lead } from '../lib/issues';

export async function GET(context: APIContext) {
  const issues = await getIssues();
  return rss({
    title: '每日阅读早报',
    description: '写给虚宝的每日阅读早报',
    site: context.site!,
    trailingSlash: true,
    customData: '<language>zh-CN</language>',
    items: issues.slice(0, 30).map((e) => ({
      title: e.data.title,
      // 早报每天北京时间 8 点左右送出
      pubDate: new Date(`${e.data.date.toISOString().slice(0, 10)}T08:00:00+08:00`),
      description: lead(e),
      link: issueUrl(e),
    })),
  });
}
