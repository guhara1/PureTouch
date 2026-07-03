#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sitemap.xml 생성기. 리포 내 모든 index.html(+루트)을 훑어 색인 페이지를 등록한다.
실행: python3 tools/build_sitemap.py [lastmod YYYY-MM-DD]
"""
import glob, os, re, sys

SITE = "https://puretouch-gandago.netlify.app"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    lastmod = sys.argv[1] if len(sys.argv) > 1 else "2026-07-03"
    os.chdir(ROOT)
    urls = []
    for f in sorted(glob.glob("**/index.html", recursive=True)) + ["index.html"]:
        html = open(f, encoding="utf-8").read()
        if re.search(r'name="robots"[^>]*noindex', html):
            continue
        d = os.path.dirname(f)
        urls.append(SITE + ("/" if not d else f"/{d}/"))
    urls = sorted(set(urls))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        depth = u[len(SITE):].count("/")
        pr = "1.0" if u == SITE + "/" else ("0.8" if depth <= 2 else ("0.7" if depth == 3 else "0.6"))
        lines.append(f"  <url><loc>{u}</loc><lastmod>{lastmod}</lastmod><priority>{pr}</priority></url>")
    lines.append("</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"sitemap.xml: {len(urls)} URLs")


if __name__ == "__main__":
    main()
