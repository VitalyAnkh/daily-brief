# 每日阅读早报

写给虚宝的每日阅读早报，网站：<https://brief.vitalyr.com/>（RSS：`/feed_rss_created.xml`）。

- 每期一个文件：`docs/issues/<年>/<YYYY-MM-DD>.md`，front matter 含 `title`、`issue`（期号）、`date`。
- 页面地址：`https://brief.vitalyr.com/issues/<年>/<YYYY-MM-DD>/`。
- 首页、归档、导航由 `hooks/issues.py` 根据 front matter 自动生成，不用手改。
- 推送到 `main` 后，GitHub Actions 用 MkDocs Material 构建并发布到 GitHub Pages。

## 新增一期

```bash
scripts/add-issue.sh 2026-11-24 12 /path/to/brief.md   # 补 front matter、校验、提交、推送
```

## 本地预览

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

第 1–11 期由聊天记录回填，原文措辞未改；排版是按原有分段还原的，原消息里的链接没有保留下来。
