import { getCollection, type CollectionEntry } from 'astro:content';

export type Issue = CollectionEntry<'issues'>;

const WEEKDAYS = '日一二三四五六';
const ID_RE = /^(\d{4})\/(\d{4}-\d{2}-\d{2})$/;

/** 日期按 UTC 解析（front matter 写的是 YYYY-MM-DD），统一用 UTC 字段取年月日。 */
export function isoDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

export function fmtDate(d: Date): string {
  return `${d.getUTCFullYear()} 年 ${d.getUTCMonth() + 1} 月 ${d.getUTCDate()} 日 · 星期${WEEKDAYS[d.getUTCDay()]}`;
}

export function issueUrl(entry: Issue): string {
  return `/issues/${entry.id}/`;
}

/** 正文开头的导语（跳过标题），作摘要用。 */
export function lead(entry: Issue, minLen = 40): string {
  if (entry.data.description) return entry.data.description;
  const out: string[] = [];
  for (const raw of (entry.body ?? '').trim().split(/\n\s*\n/)) {
    const p = raw.trim();
    if (!p || p.startsWith('#') || p.startsWith('<')) {
      if (out.length) break;
      continue;
    }
    out.push(p.replace(/\*\*|\\\*/g, (m) => (m === '\\*' ? '*' : '')).replace(/\$[^$]*\$/g, (m) => m.slice(1, -1)));
    if (out.join('').length >= minLen) break;
  }
  return out.join(' ');
}

let cache: Issue[] | undefined;

/** 全部期次，新到旧；同时校验文件名、日期与期号。 */
export async function getIssues(): Promise<Issue[]> {
  if (cache) return cache;
  const all = await getCollection('issues');
  const seen = new Map<number, string>();
  for (const e of all) {
    const m = ID_RE.exec(e.id);
    if (!m) throw new Error(`${e.id}: 文件应放在 src/content/issues/<年>/<YYYY-MM-DD>.md`);
    if (m[2] !== isoDate(e.data.date) || m[1] !== m[2].slice(0, 4))
      throw new Error(`${e.id}: front matter 的 date (${isoDate(e.data.date)}) 与文件名不一致`);
    const dup = seen.get(e.data.issue);
    if (dup) throw new Error(`期号 ${e.data.issue} 重复：${dup} 与 ${e.id}`);
    seen.set(e.data.issue, e.id);
  }
  cache = all.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf() || b.data.issue - a.data.issue);
  return cache;
}
