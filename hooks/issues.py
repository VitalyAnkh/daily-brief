"""MkDocs hook: 由 docs/issues/<年>/<日期>.md 的 front matter 自动生成导航、首页与归档。

每期文件必须带 front matter：
    ---
    title: 第 12 期 · 11 月 24 日
    issue: 12
    date: 2026-11-24
    ---
文件名必须是 YYYY-MM-DD.md，并与 date 一致。
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.utils.meta import get_data

WEEKDAYS = "一二三四五六日"
NAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")
_ISSUES: list[dict] = []


def _lead(body: str, min_len: int = 40) -> str:
    """取正文开头的导语段落（不含标题），作为首页摘要。"""
    out: list[str] = []
    for para in re.split(r"\n\s*\n", body.strip()):
        para = para.strip()
        if not para or para.startswith(("#", "<", "---")):
            if out:
                break
            continue
        out.append(para)
        if sum(len(p) for p in out) >= min_len:
            break
    return "\n\n".join(out)


def _load_issues(docs_dir: Path) -> list[dict]:
    issues = []
    for path in sorted((docs_dir / "issues").glob("*/*.md")):
        rel = path.relative_to(docs_dir).as_posix()
        m = NAME_RE.match(path.name)
        if not m or path.parent.name != m.group(1):
            raise PluginError(f"{rel}: 文件应命名为 issues/<年>/<YYYY-MM-DD>.md")
        body, meta = get_data(path.read_text(encoding="utf-8"))
        for key in ("title", "issue", "date"):
            if key not in meta:
                raise PluginError(f"{rel}: front matter 缺少 {key}")
        date = meta["date"]
        if isinstance(date, str):
            date = dt.date.fromisoformat(date)
        if isinstance(date, dt.datetime):
            date = date.date()
        if date.isoformat() != path.stem:
            raise PluginError(f"{rel}: date ({date}) 与文件名不一致")
        issues.append(
            {"path": rel, "title": str(meta["title"]), "issue": int(meta["issue"]),
             "date": date, "description": str(meta.get("description") or _lead(body))}
        )
    issues.sort(key=lambda i: (i["date"], i["issue"]), reverse=True)
    seen: dict[int, str] = {}
    for i in issues:
        if i["issue"] in seen:
            raise PluginError(f"期号 {i['issue']} 重复：{seen[i['issue']]} 与 {i['path']}")
        seen[i["issue"]] = i["path"]
    return issues


def on_config(config, **kwargs):
    global _ISSUES
    _ISSUES = _load_issues(Path(config["docs_dir"]))
    years: dict[int, list] = {}
    for i in _ISSUES:
        years.setdefault(i["date"].year, []).append({i["title"]: i["path"]})
    config["nav"] = [{"首页": "index.md"}, {"归档": "archive.md"}] + [
        {f"{y} 年": items} for y, items in sorted(years.items(), reverse=True)
    ]
    return config


def _fmt_date(d: dt.date) -> str:
    return f"{d.year} 年 {d.month} 月 {d.day} 日 · 星期{WEEKDAYS[d.weekday()]}"


def _link(i: dict) -> str:
    # 相对 docs/ 根目录的链接；首页与归档都在根目录，MkDocs 会转换为正确的 URL
    return f"[{i['title']}]({i['path']})"


def _archive_md() -> str:
    lines: list[str] = []
    cur = None
    for i in _ISSUES:
        key = (i["date"].year, i["date"].month)
        if key != cur:
            lines.append(f"\n## {key[0]} 年 {key[1]} 月\n")
            cur = key
        lines.append(f"- {_link(i)} <span class=\"brief-meta\">{_fmt_date(i['date'])}</span>")
    return "\n".join(lines) + "\n"


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_uri
    if src == "index.md":
        if _ISSUES:
            latest = _ISSUES[0]
            block = (
                f"## 最新一期\n\n### {_link(latest)}\n\n"
                f"<p class=\"brief-meta\">{_fmt_date(latest['date'])}</p>\n\n"
                + (f"{latest['description']}\n\n" if latest["description"] else "")
                + "## 近期\n\n"
                + "\n".join(
                    f"- {_link(i)} <span class=\"brief-meta\">{_fmt_date(i['date'])}</span>"
                    for i in _ISSUES[1:8]
                )
                + "\n\n[全部往期 →](archive.md)\n"
            )
        else:
            block = "还没有早报。\n"
        return markdown.replace("<!-- issues:home -->", block)
    if src == "archive.md":
        return markdown.replace("<!-- issues:archive -->", _archive_md())
    if src.startswith("issues/") and page.meta.get("issue"):
        d = page.meta["date"]
        if isinstance(d, str):
            d = dt.date.fromisoformat(d)
        if not page.meta.get("description"):
            page.meta["description"] = _lead(markdown)
        meta = f"<p class=\"brief-meta\">第 {page.meta['issue']} 期 · {_fmt_date(d)}</p>\n\n"
        return meta + markdown
    return markdown
