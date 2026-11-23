# 每日阅读早报

写给虚宝的每日阅读早报。网站：<https://brief.vitalyr.com/> · RSS：<https://brief.vitalyr.com/rss.xml>

用 [Astro](https://astro.build) 构建：内容集合存放每一期，[Pagefind](https://pagefind.app) 做中文全文搜索，remark-math + rehype-katex 渲染公式，推送到 `main` 后由 GitHub Actions 发布到 GitHub Pages。

- 每期一个文件：`src/content/issues/<年>/<YYYY-MM-DD>.md`，front matter 含 `title`、`issue`（期号）、`date`，可选 `description`。
- 页面地址：`https://brief.vitalyr.com/issues/<年>/<YYYY-MM-DD>/`
- 首页、归档、RSS、站点地图都根据 front matter 自动生成；文件名与日期不一致或期号重复时构建会报错。

## 新增一期

```bash
npm ci                                                  # 第一次用时装依赖
scripts/add-issue.sh 2026-11-24 12 /path/to/brief.md    # 补 front matter、构建校验、提交、推送
```

## 本地预览

```bash
npm ci
npm run dev        # 开发预览（搜索需先 npm run build，再 npm run preview）
```

第 1–11 期是从聊天记录回填的，措辞没有改动。分段照原样还原，原消息里的链接没能保留下来。

## 字体

全站衬线，仿论文排版：

- 西文：Latin Modern Roman（正、斜、粗、粗斜），代码用 Latin Modern Mono。取自 CTAN `lm` 的 OTF，用 fonttools 子集化为 woff2，放在 `public/fonts/lm/`（共约 160 KB，GUST Font License）。
- 中文：本机宋体优先（Songti SC、STSong），否则加载 `@fontsource/noto-serif-sc`（思源宋体）的 unicode-range 分片，只下载页面用到的字；再往后是 Noto Serif CJK SC、Source Han Serif SC、SimSun。
- 公式：KaTeX 自带 Computer Modern 系字体，与 Latin Modern 同源。
