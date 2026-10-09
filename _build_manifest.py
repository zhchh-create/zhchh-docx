#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描知识库目录，生成 assets/manifest.js"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "assets")
os.makedirs(OUT_DIR, exist_ok=True)

CATS = []
for name in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, name)
    if os.path.isdir(full) and re.match(r"^\d+_", name):
        CATS.append((name, full))

# 分类展示名（去掉前缀数字）和图标 emoji / 描述
CAT_META = {
    "01_前端基础":      ("前端基础",   "🎨", "HTML5 / CSS3 / JavaScript / TypeScript / 浏览器原理 / HTTP"),
    "02_前端框架与状态管理": ("框架与状态", "⚛️", "Vue / React / 组件化 / Pinia / Redux / 微前端 / SSR"),
    "03_数据可视化":    ("数据可视化", "📊", "ECharts / AntV G6 / Three.js / Canvas / SVG / 大屏"),
    "04_实时通信":      ("实时通信",   "📡", "WebSocket / SSE / WebRTC / Janus / 音视频协议"),
    "05_前端常用工具库": ("工具库",     "🧰", "Axios / vxe-table / JsPlumb / Monaco / VueUse / Lodash"),
    "06_前端工程化与工具链": ("工程化",   "⚙️", "Vite / Webpack / Git / ESLint / 测试 / Monorepo"),
    "07_后端开发":      ("后端开发",   "☕", "Java / Spring / Spring Boot / MyBatis / RESTful / JWT"),
    "08_数据库与建模":   ("数据库",     "🗄️", "MySQL / Redis / Oracle / ES / MongoDB / 分库分表"),
    "09_DevOps部署与运维": ("DevOps",    "🚀", "Nginx / Docker / K8s / CI-CD / Linux / 监控"),
    "10_研发流程与AI辅助": ("研发与AI",  "🤖", "敏捷 / 代码评审 / AI 编程 / RAG / 技术选型"),
    "11_全面学习":      ("体系精讲",   "🎯", "6 篇体系化长文，快速建立全栈知识地图"),
}

def depth_of(fname: str) -> str:
    if "深入" in fname: return "deep"
    if "标准" in fname: return "std"
    if "基础" in fname: return "basic"
    return "std"

def pretty_title(fname: str) -> str:
    # 01_HTML5与CSS3【深入】 -> HTML5 与 CSS3
    s = fname
    s = re.sub(r"\.[hH][tT][mM][lL]$", "", s)
    s = re.sub(r"^\d+_", "", s)
    s = re.sub(r"【(深入|标准|基础)】", "", s)
    s = s.replace("_", " · ")
    return s.strip()

manifest = {"cats": [], "total": 0}
for cname, cdir in CATS:
    arts = []
    for fn in sorted(os.listdir(cdir)):
        if not fn.lower().endswith(".html"): continue
        # 读 title
        title = None
        try:
            with open(os.path.join(cdir, fn), "r", encoding="utf-8", errors="ignore") as f:
                head = f.read(2000)
            m = re.search(r"<title>([^<]+)</title>", head)
            if m:
                title = m.group(1).replace("｜全栈技术知识库", "").strip()
        except Exception:
            pass
        if not title:
            title = pretty_title(fn)
        arts.append({
            "t": title,
            "f": fn,
            "u": f"{cname}/{fn}",
            "d": depth_of(fn),
        })
    disp, icon, desc = CAT_META.get(cname, (cname, "📁", ""))
    manifest["cats"].append({
        "key": cname,
        "name": disp,
        "icon": icon,
        "desc": desc,
        "arts": arts,
    })
    manifest["total"] += len(arts)

out = "// 自动生成的知识库清单，请勿手动编辑\nwindow.KB_MANIFEST = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n"
out_path = os.path.join(OUT_DIR, "manifest.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)

print(f"OK: {manifest['total']} articles, {len(manifest['cats'])} categories -> {out_path}")
for c in manifest["cats"]:
    print(f"  {c['icon']} {c['name']}: {len(c['arts'])}")
