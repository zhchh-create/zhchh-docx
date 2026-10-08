import os, re, io

root = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解"
dirs = ["07_后端开发", "08_数据库与建模"]
out_dir = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解\_sec5_work"
os.makedirs(out_dir, exist_ok=True)

for d in dirs:
    p = os.path.join(root, d)
    for fn in sorted(os.listdir(p)):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(p, fn)
        with io.open(fp, encoding="utf-8") as f:
            html = f.read()
        m = re.search(r'<section id="sec5".*?(?=<section id="sec6")', html, re.S)
        toc = re.search(r'<li><a href="#sec5">([^<]*)</a></li>', html)
        tag = "".join(re.findall(r"【(.*?)】", fn))
        out = os.path.join(out_dir, fn.replace(".html", ".txt"))
        with io.open(out, "w", encoding="utf-8") as f:
            f.write("FILE: %s/%s\n" % (d, fn))
            f.write("DEPTH: %s\n" % tag)
            f.write("TOC sec5 text: %s\n" % (toc.group(1) if toc else "??"))
            f.write("=" * 60 + "\n")
            f.write(m.group(0).strip() if m else "!! sec5 NOT FOUND !!")
            f.write("\n")
print("done")
