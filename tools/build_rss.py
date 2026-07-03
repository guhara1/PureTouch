#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rss.xml 생성기. 네이버 서치어드바이저 RSS 제출 + 구글(피드=사이트맵 허용)용.
색인 우선순위가 높은 페이지(메인·허브·후기·시/구)를 앞에 배치한다.
실행: python3 tools/build_rss.py [YYYY-MM-DD]
"""
import glob, os, re, sys, html

SITE = "https://puretouch-gandago.netlify.app"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def rfc822(datestr):
    y, m, d = map(int, datestr.split("-"))
    # 요일 계산(Zeller 불필요) — datetime 미사용 환경 대비 간이 계산
    import datetime
    wd = datetime.date(y, m, d).weekday()
    return f"{WDAYS[wd]}, {d:02d} {MONTHS[m-1]} {y} 09:00:00 +0900"


def depth(url):
    return url[len(SITE):].strip("/").count("/")


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-07-03"
    os.chdir(ROOT)
    items = []
    seen = set()
    for f in sorted(glob.glob("**/index.html", recursive=True)) + ["index.html"]:
        htmlt = open(f, encoding="utf-8").read()
        if re.search(r'name="robots"[^>]*noindex', htmlt):
            continue
        d = os.path.dirname(f)
        url = SITE + ("/" if not d else f"/{d}/")
        if url in seen:
            continue
        seen.add(url)
        title = re.search(r"<title>(.*?)</title>", htmlt, re.S)
        desc = re.search(r'<meta name="description" content="([^"]*)"', htmlt)
        items.append({
            "url": url,
            "title": html.escape((title.group(1) if title else "간다GO").strip()),
            "desc": html.escape((desc.group(1) if desc else "").strip()),
        })
    # 우선순위: 얕은 depth 먼저(메인·허브·시), 그다음 알파벳
    items.sort(key=lambda x: (depth(x["url"]), x["url"]))
    pub = rfc822(date)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
           '  <channel>',
           '    <title>간다GO 출장마사지·홈타이 지역 안내</title>',
           f'    <link>{SITE}/</link>',
           '    <description>천안·대전·세종·호남권 생활권별 출장 케어 방문 안내</description>',
           '    <language>ko</language>',
           f'    <lastBuildDate>{pub}</lastBuildDate>',
           f'    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml" />']
    for it in items:
        out += ['    <item>',
                f'      <title>{it["title"]}</title>',
                f'      <link>{it["url"]}</link>',
                f'      <guid isPermaLink="true">{it["url"]}</guid>',
                f'      <description>{it["desc"]}</description>',
                f'      <pubDate>{pub}</pubDate>',
                '    </item>']
    out += ['  </channel>', '</rss>']
    open("rss.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"rss.xml: {len(items)} items")


if __name__ == "__main__":
    main()
