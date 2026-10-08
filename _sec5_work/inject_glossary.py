"""
批量给所有内容页 HTML 注入 glossary 引用。
- 子目录文件：相对路径 ../glossary/...
- 已注入过的文件跳过
- 跳过 index.html（首页无正文）和 glossary/ 目录本身
"""
import os, re, sys

ROOT = r"F:\跑路资料整理\技术栈详解DouBao"
EXCLUDE_DIRS = {"_shots", "_sec5_work", "_模板", "glossary", "__pycache__"}
EXCLUDE_FILES = {"index.html"}  # 首页无正文

css_marker = 'glossary.css'
js_marker = 'glossary-data.js'

injected = 0
skipped = 0
errors = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # 过滤排除目录
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        if fn in EXCLUDE_FILES:
            continue
        full = os.path.join(dirpath, fn)
        rel_dir = os.path.relpath(dirpath, ROOT)
        # 计算前缀
        if rel_dir == ".":
            prefix = ""
        else:
            prefix = "../"

        try:
            with open(full, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as e:
            errors.append((full, str(e)))
            continue

        # 已注入检查
        if css_marker in html and js_marker in html:
            skipped += 1
            continue

        # 1. 在 </head> 前插 CSS
        css_link = f'<link rel="stylesheet" href="{prefix}glossary/glossary.css">'
        if css_marker not in html:
            # 找到 </head>
            if "</head>" not in html:
                errors.append((full, "no </head>"))
                continue
            html = html.replace("</head>", f"{css_link}\n</head>", 1)

        # 2. 在 </body> 前插 JS
        js_tags = (
            f'<script src="{prefix}glossary/glossary-data.js"></script>\n'
            f'<script src="{prefix}glossary/glossary.js"></script>'
        )
        if js_marker not in html:
            if "</body>" not in html:
                errors.append((full, "no </body>"))
                continue
            html = html.replace("</body>", f"{js_tags}\n</body>", 1)

        try:
            with open(full, "w", encoding="utf-8") as f:
                f.write(html)
            injected += 1
        except Exception as e:
            errors.append((full, str(e)))

print(f"注入: {injected}")
print(f"跳过(已注入): {skipped}")
print(f"错误: {len(errors)}")
for e in errors:
    print("  ", e)
