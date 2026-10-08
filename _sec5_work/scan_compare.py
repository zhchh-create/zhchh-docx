import os, re, json

root = r"F:\跑路资料整理\技术栈详解DouBao"
results = []

for dirpath, dirs, files in os.walk(root):
    # 跳过 _shots、_sec5_work、glossary 等目录
    if "_shots" in dirpath or "_sec5_work" in dirpath or "glossary" in dirpath:
        continue
    for f in files:
        if not f.endswith(".html"):
            continue
        path = os.path.join(dirpath, f)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except:
            continue
        
        # 找 h3 标题里带"对比"、"vs"的
        h3_matches = re.findall(r'<h3>([^<]*(?:对比|vs|VS|区别|差异)[^<]*)</h3>', content)
        
        # 找已有 diagram 数量
        diagram_count = content.count('class="diagram"')
        
        # 找 table 数量（表格也算一种对比，但已经是可视化了）
        table_count = content.count('<table>')
        
        if h3_matches:
            rel_path = os.path.relpath(path, root)
            results.append({
                "file": rel_path,
                "diagrams": diagram_count,
                "tables": table_count,
                "compare_h3s": h3_matches
            })

# 按文件排序
results.sort(key=lambda x: x["file"])

print(f"共找到 {len(results)} 篇文章有对比类 h3 标题\n")
for r in results:
    print(f"【{r['file']}】 已有图:{r['diagrams']} 表格:{r['tables']}")
    for h in r["compare_h3s"]:
        print(f"  - {h}")
    print()
