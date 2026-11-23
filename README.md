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

全站衬线（代码除外），“古典书卷”风格：

- 中文：思源宋体（Noto Serif SC），用 `@fontsource/noto-serif-sc` 的 400/700 两档，按 unicode-range 切成约百个分片自托管，页面只下载用到的字；排在本机宋体之前，各平台观感一致。后备：Source Han Serif SC、Noto Serif CJK SC、Songti SC。
- 西文：EB Garamond 可变字体（wght 400–800，正体与斜体，真正的半粗/粗体），取自 [google/fonts](https://github.com/google/fonts/tree/main/ofl/ebgaramond)，用 fonttools 子集化为拉丁 + 拉丁扩展 A，保留 onum/lnum/tnum/smcp 等特性。`size-adjust: 112%` 补偿 Garamond 偏小的 x 字高，让夹在中文里的西文不显矮。
- 代码：JetBrains Mono 可变字体（取自 [google/fonts](https://github.com/google/fonts/tree/main/ofl/jetbrainsmono)，同样子集化），字号 0.82em。
- 数字：全站用齐线数字（lnum），日期另加等宽数字（tnum）以便列表对齐。正文里的数字多是日期、型号和数量，Garamond 的旧式数字 1 形如小写 ı，夹在汉字中间难认，所以旧式数字（onum）只用于斜体西文。
- 西文字体的 unicode-range 去掉了 ‘’“”—…·，这些标点由思源宋体显示为全角。
- 公式：KaTeX 用自带字体，字号 1.04em，与放大后的 Garamond 小写字母齐平。
- 文件：`public/fonts/` 下 `eb-garamond-roman.woff2`（约 83 KB）、`eb-garamond-italic.woff2`（约 88 KB）、`jetbrains-mono.woff2`（约 42 KB）；许可均为 SIL OFL 1.1，许可文本同在该目录。
- 重新子集化：`pyftsubset 'EBGaramond[wght].ttf' --unicodes=<src/styles/fonts.css 里的 unicode-range> --layout-features='kern,liga,clig,calt,ccmp,locl,mark,mkmk,onum,lnum,tnum,pnum,smcp,c2sc,case,frac,numr,dnom,sups,subs,zero' --flavor=woff2 --output-file=eb-garamond-roman.woff2`，斜体与 JetBrains Mono 同理。
