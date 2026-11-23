#!/usr/bin/env bash
# 新增（或覆盖）一期早报，然后提交并推送；GitHub Actions 会自动重建网站。
#
# 用法：
#   scripts/add-issue.sh <YYYY-MM-DD> <期号> <正文.md> [--force] [--no-push]
#
#   <正文.md>  早报正文（Markdown）。可以自带 front matter；没有的话脚本会补上：
#                title: 第 <期号> 期 · <月> 月 <日> 日
#                issue: <期号>
#                date: <YYYY-MM-DD>
#              正文里不必写一级标题，页面会用 title 作标题。
#   --force    同一天的文件已存在时覆盖（默认拒绝）。
#   --no-push  只提交，不推送。
#
# 页面地址：https://brief.vitalyr.com/issues/<YYYY>/<YYYY-MM-DD>/
set -euo pipefail

usage() { sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
[[ $# -ge 3 ]] || usage
date="$1"; issue="$2"; src="$3"; shift 3
force=0; push=1
for arg in "$@"; do
  case "$arg" in
    --force) force=1 ;;
    --no-push) push=0 ;;
    *) usage ;;
  esac
done

[[ "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "日期格式应为 YYYY-MM-DD：$date" >&2; exit 1; }
date -d "$date" +%F >/dev/null 2>&1 || { echo "无效日期：$date" >&2; exit 1; }
[[ "$issue" =~ ^[1-9][0-9]*$ ]] || { echo "期号应为正整数：$issue" >&2; exit 1; }
[[ -s "$src" ]] || { echo "找不到正文文件或文件为空：$src" >&2; exit 1; }

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
year="${date:0:4}"
dest="src/content/issues/$year/$date.md"

if [[ -e "$dest" && $force -ne 1 ]]; then
  echo "$dest 已存在；如需覆盖请加 --force" >&2; exit 1
fi
if dup=$(grep -lE "^issue:[[:space:]]*${issue}[[:space:]]*$" src/content/issues/*/*.md 2>/dev/null | grep -vx "$dest"); then
  echo "期号 $issue 已被占用：$dup" >&2; exit 1
fi

git pull --ff-only --quiet || { echo "git pull 失败，请先处理本地分支" >&2; exit 1; }

mkdir -p "src/content/issues/$year"
tmp="$(mktemp)"
if head -n1 "$src" | grep -qx -- '---'; then
  fm="$(awk 'NR==1{next} /^---$/{exit} {print}' "$src")"
  grep -qE "^date:[[:space:]]*['\"]?${date}['\"]?[[:space:]]*$" <<<"$fm" || { echo "正文 front matter 的 date 与参数 $date 不一致" >&2; exit 1; }
  grep -qE "^issue:[[:space:]]*${issue}[[:space:]]*$" <<<"$fm" || { echo "正文 front matter 的 issue 与参数 $issue 不一致" >&2; exit 1; }
  cp "$src" "$tmp"
else
  month=$((10#${date:5:2})); day=$((10#${date:8:2}))
  {
    printf -- '---\ntitle: 第 %s 期 · %s 月 %s 日\nissue: %s\ndate: %s\n---\n\n' "$issue" "$month" "$day" "$issue" "$date"
    cat "$src"
  } > "$tmp"
fi
mv "$tmp" "$dest"
chmod 644 "$dest"

# 依赖已装好时先完整构建一遍（类型检查 + 构建 + 搜索索引），避免把坏文件推上去
if [[ -d node_modules ]]; then
  if ! ASTRO_TELEMETRY_DISABLED=1 npm run --silent build >/tmp/daily-brief-build.log 2>&1; then
    tail -n 30 /tmp/daily-brief-build.log >&2
    echo "构建失败，已写入 $dest 但未提交；修好后重跑（加 --force）" >&2; exit 1
  fi
else
  echo "提示：没有 node_modules，跳过本地构建校验（CI 仍会完整构建）。可先运行 npm ci" >&2
fi

git add "$dest"
if git diff --cached --quiet; then
  echo "内容没有变化，未提交。"
else
  git commit --quiet -m "第 ${issue} 期：${date}"
  if [[ $push -eq 1 ]]; then git push --quiet; fi
fi
echo "https://brief.vitalyr.com/issues/$year/$date/"
