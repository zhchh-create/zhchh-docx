# -*- coding: utf-8 -*-
import io, os, re
ROOT = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解"
bad = []
for d in ["07_后端开发", "08_数据库与建模"]:
    p = os.path.join(ROOT, d)
    for fn in sorted(os.listdir(p)):
        if not fn.endswith(".html"): continue
        fp = os.path.join(p, fn)
        s = io.open(fp, encoding="utf-8").read()
        secs = len(re.findall(r'<section id="sec\d"', s))
        kb = os.path.getsize(fp) / 1024
        has_real = "实战项目经验（真实项目落地）" in s
        has_demo = "实战项目经验（自学 + 自建 Demo）" in s
        toc_ok = ('href="#sec5">实战项目经验' in s)
        old_left = "使用案例（真实项目落地）" in s
        flags = []
        if secs != 7: flags.append("secs=%d" % secs)
        if kb < 15: flags.append("size=%.1fKB" % kb)
        if not (has_real or has_demo): flags.append("no-new-h2")
        if not toc_ok: flags.append("toc-not-updated")
        if old_left: flags.append("old-text-left")
        status = "OK " if not flags else "BAD"
        print("%s %s/%s  secs=%d %.1fKB  %s" % (status, d, fn, secs, kb, ",".join(flags)))
        if flags: bad.append(fn)
print("BAD count:", len(bad))
