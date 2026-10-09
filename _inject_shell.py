#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量给每篇文章注入知识库外壳（app.css + app.js）"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

HEAD_INJECT = '<link rel="stylesheet" href="../assets/app.css">\n'
BODY_INJECT = '<script src="../assets/app.js"></' + 'script>\n'

patched = 0
skipped = 0
errors = []

for cname in sorted(os.listdir(ROOT)):
    cdir = os.path.join(ROOT, cname)
    if not (os.path.isdir(cdir) and re.match(r"^\d+_", cname)):
        continue
    for fn in sorted(os.listdir(cdir)):
        if not fn.lower().endswith(".html"):
            continue
        fp = os.path.join(cdir, fn)
        try:
            with open(fp, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as e:
            errors.append(f"READ {fp}: {e}")
            continue

        if "app.css" in html and "app.js" in html:
            skipped += 1
            continue

        # 注入 head
        if "</head>" in html and "app.css" not in html:
            html = html.replace("</head>", HEAD_INJECT + "</head>", 1)
        # 注入 body
        if "</body>" in html and "app.js" not in html:
            html = html.replace("</body>", BODY_INJECT + "</body>", 1)
        elif "</html>" in html and "app.js" not in html:
            # 某些文件可能没有 </body>
            html = html.replace("</html>", BODY_INJECT + "</html>", 1)

        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
            patched += 1
        except Exception as e:
            errors.append(f"WRITE {fp}: {e}")

print(f"Patched: {patched}, Skipped(already): {skipped}, Errors: {len(errors)}")
for e in errors:
    print(" ", e)
