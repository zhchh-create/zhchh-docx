"""扫描所有文章：SVG数、字数、章节数、表格数、代码块数"""
import os, re, json

ROOT = r"F:\跑路资料整理\技术栈详解DouBao"
EXCLUDE = {"_shots", "_sec5_work", "_模板", "glossary", "__pycache__"}
results = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE]
    for fn in filenames:
        if not fn.endswith(".html") or fn == "index.html":
            continue
        full = os.path.join(dirpath, fn)
        try:
            with open(full, "r", encoding="utf-8") as f:
                html = f.read()
        except:
            continue

        # 提取 main 区域文本（去掉 style/script/svg）
        body = re.sub(r'<style[\s\S]*?</style>', '', html)
        body = re.sub(r'<script[\s\S]*?</script>', '', body)
        svg_count = len(re.findall(r'<svg', html))
        # 纯文本字数（去标签）
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'\s+', '', text)
        char_count = len(text)
        h2 = len(re.findall(r'<h2', html))
        h3 = len(re.findall(r'<h3', html))
        tables = len(re.findall(r'<table', html))
        code_blocks = len(re.findall(r'<pre[^>]*class="code"', html))
        # 相对路径
        rel = os.path.relpath(full, ROOT)
        results.append({
            "file": rel,
            "chars": char_count,
            "svg": svg_count,
            "h2": h2,
            "h3": h3,
            "tables": tables,
            "code": code_blocks
        })

# 按 SVG 升序 + 字数升序排
results.sort(key=lambda x: (x["svg"], x["chars"]))
print(f"{'SVG':>3} {'字数':>6} {'H2':>3} {'H3':>3} {'表':>3} {'码':>3}  文件")
print("-" * 90)
for r in results:
    print(f"{r['svg']:>3} {r['chars']:>6} {r['h2']:>3} {r['h3']:>3} {r['tables']:>3} {r['code']:>3}  {r['file']}")

print(f"\n共 {len(results)} 篇")
print(f"SVG=0 的文章: {sum(1 for r in results if r['svg']==0)} 篇")
print(f"SVG<2 的文章: {sum(1 for r in results if r['svg']<2)} 篇")
print(f"字数<3000 的文章: {sum(1 for r in results if r['chars']<3000)} 篇")
