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

第 1–11 期是从聊天记录回填的，措辞没有改动。格式与链接按原消息还原；原消息在聊天记录里被截断的中段，链接是逐条查证后补回的，查不到可靠来源的条目不加链接。

## 字体

全站衬线，“现代编辑”风格（思源宋体与 Source Serif 同出 Adobe，笔画和气质相配）：

- 中文：思源宋体（Noto Serif SC），用 `@fontsource/noto-serif-sc` 的 400/700 两档，按 unicode-range 切成约百个分片自托管，页面只下载用到的字；排在本机宋体之前，Mac、Windows、Linux 观感一致。后备：Source Han Serif SC、Noto Serif CJK SC、Songti SC。
- 西文：Source Serif 4 可变字体（字重 + 光学尺寸轴，正体与斜体），拉丁子集，`public/fonts/`。
- 代码：IBM Plex Mono（400、400 斜体、700），拉丁子集，`public/fonts/`。
- 西文字体的 unicode-range 去掉了 ‘’“”—…·，这些标点由思源宋体显示为全角。
- 公式：KaTeX 用自带字体，字号调到 1.1em 与 Source Serif 的 x 字高对齐。
- 许可：均为 SIL OFL 1.1，许可文本在 `public/fonts/`。
