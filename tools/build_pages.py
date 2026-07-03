#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간다GO · PureTouch 정적 페이지 생성기.
지역/이용/확인/정책 페이지를 동일한 헤더·푸터·스키마 규격으로 생성한다.
index.html 과 central-honam/index.html 은 손으로 관리하며 이 스크립트가 덮지 않는다.

실행: python3 tools/build_pages.py
"""
import os, json, html
from reviews_data import REVIEWS, rating_value, rating_count, stars

SITE = "https://puretouch-gandago.netlify.app"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVER_VERIFY = "bf46e88651b938869e2456d58c33a8666f1ee30e"

# 전 페이지 <head> 공통 추가: 네이버 인증 + RSS 자동발견
HEAD_EXTRA = f"""  <meta name="naver-site-verification" content="{NAVER_VERIFY}" />
  <link rel="alternate" type="application/rss+xml" title="간다GO 소식" href="/rss.xml" />"""

ORG_ID = f"{SITE}/#org"
WEBSITE_ID = f"{SITE}/#website"


def org_node(with_reviews=False):
    node = {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "간다GO",
        "url": f"{SITE}/",
        "logo": f"{SITE}/assets/logo.png",
        "image": f"{SITE}/assets/og-cover.jpg",
        "telephone": "+82-508-202-4719",
        "areaServed": ["천안", "대전", "세종", "광주", "전주", "익산", "군산", "여수", "순천", "목포", "나주", "호남권"],
        "contactPoint": {"@type": "ContactPoint", "telephone": "+82-508-202-4719",
                         "contactType": "reservations", "availableLanguage": "ko"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(rating_value()),
                            "reviewCount": str(rating_count()), "bestRating": "5", "worstRating": "1"},
    }
    if with_reviews:
        node["review"] = [{
            "@type": "Review",
            "author": {"@type": "Person", "name": r["author"]},
            "datePublished": r["date"],
            "name": f'{r["type"]} 후기',
            "reviewBody": r["body"],
            "reviewRating": {"@type": "Rating", "ratingValue": str(r["rating"]),
                             "bestRating": "5", "worstRating": "1"},
        } for r in REVIEWS]
    return node


def service_node():
    return {
        "@type": "Service",
        "@id": f"{SITE}/#service",
        "name": "간다GO 출장마사지·홈타이 방문 케어",
        "serviceType": "출장마사지·홈타이 방문 안내",
        "provider": {"@id": ORG_ID},
        "areaServed": "천안·대전·세종·호남권",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(rating_value()),
                            "reviewCount": str(rating_count()), "bestRating": "5", "worstRating": "1"},
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "이용 코스",
            "itemListElement": [
                {"@type": "Offer", "name": "60분 코스", "price": "90000", "priceCurrency": "KRW"},
                {"@type": "Offer", "name": "90분 코스", "price": "150000", "priceCurrency": "KRW"},
                {"@type": "Offer", "name": "120분 코스", "price": "180000", "priceCurrency": "KRW"},
            ],
        },
    }


def reviews_html(heading="이용 후기"):
    """화면 노출용 후기 목록 (스키마와 1:1 대응)."""
    avg, cnt = rating_value(), rating_count()
    cards = []
    for r in REVIEWS:
        cards.append(
            f'<article class="review-card">'
            f'<div class="review-head"><span class="review-type">{r["type"]}</span>'
            f'<span class="review-stars" aria-label="{r["rating"]}점">{stars(r["rating"])}</span></div>'
            f'<p class="review-body">{r["body"]}</p>'
            f'<p class="review-meta">{r["author"]} · <time datetime="{r["date"]}">{r["date"].replace("-", ".")}</time></p>'
            f'</article>')
    return (f'<section class="reviews-wrap">'
            f'<div class="reviews-summary"><b>{avg}</b><span class="review-stars">{stars(round(avg))}</span>'
            f'<span class="reviews-count">이용자 후기 {cnt}건 평균</span></div>'
            f'<div class="review-grid">' + "\n".join(cards) + '</div></section>')

HEADER = """<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><span class="dot">GO</span> 간다GO</a>
    <nav class="nav" aria-label="주요 메뉴">
      <a href="/central-honam/cheonan/">천안권</a>
      <a href="/central-honam/daejeon/">대전권</a>
      <a href="/central-honam/sejong/">세종권</a>
      <a href="/central-honam/honam/">호남권</a>
      <a class="cta" href="tel:0508-202-4719">예약 문의</a>
    </nav>
  </div>
</header>"""

TG = "https://t.me/ganda_go"  # placeholder → 실제 텔레그램 핸들로 교체
TG_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
           '<path d="M21.94 4.3 18.9 19.1c-.23 1.02-.84 1.27-1.7.79l-4.7-3.47-2.27 2.18c-.25.25-.46.46-.94.46'
           'l.34-4.8 8.72-7.88c.38-.34-.08-.53-.6-.19L6.7 13.2l-4.65-1.45c-1.01-.32-1.03-1.01.21-1.5L20.6 2.9'
           'c.84-.31 1.58.2 1.34 1.4Z"/></svg>')

ASIDE = f"""<aside class="aside">
      <div class="cta-card">
        <h3 class="cta-title">지금 예약 문의</h3>
        <p class="cta-sub">천안·대전·세종·호남권 생활권별 방문 안내</p>
        <a class="btn btn-accent cta-btn" href="tel:0508-202-4719">전화 예약 0508-202-4719</a>
        <ul class="cta-price">
          <li><span>60분 코스</span><b>90,000원</b></li>
          <li><span>90분 코스</span><b>150,000원</b></li>
          <li><span>120분 코스</span><b>180,000원</b></li>
        </ul>
        <p class="cta-note">지역·예약 시간대·이동 거리에 따라 상담 시 최종 확인됩니다. 불법·선정적 서비스는 제공하지 않습니다.</p>
      </div>
    </aside>"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="/"><span class="dot">GO</span> 간다GO</a>
        <p>천안·대전·세종·호남권 생활권별 출장 케어 방문 안내. 불법·선정적 서비스는 제공하지 않습니다.</p>
        <div class="footer-biz"><p><b>상호</b> 간다GO &nbsp;·&nbsp; <b>전화예약</b> <a href="tel:0508-202-4719">0508-202-4719</a></p></div>
      </div>
      <div class="footer-col"><h4>지역 안내</h4><ul>
        <li><a href="/central-honam/cheonan/">천안권</a></li>
        <li><a href="/central-honam/daejeon/">대전권</a></li>
        <li><a href="/central-honam/sejong/">세종권</a></li>
        <li><a href="/central-honam/honam/">호남권</a></li>
      </ul></div>
      <div class="footer-col"><h4>이용 안내</h4><ul>
        <li><a href="/central-honam/reviews/">이용 후기</a></li>
        <li><a href="/central-honam/check/privacy/">개인정보 처리방침</a></li>
        <li><a href="/central-honam/check/service-policy/">불법·선정적 서비스 불가 안내</a></li>
        <li><a href="/central-honam/author/">작성자·검수자 안내</a></li>
        <li><a href="/sitemap.xml">사이트맵</a></li>
      </ul></div>
    </div>
    <div class="footer-cta">
      <a class="btn btn-accent" href="{TG}" target="_blank" rel="noopener nofollow">{TG_ICON} 웹사이트 제작문의</a>
      <a class="btn btn-accent" href="{TG}" target="_blank" rel="noopener nofollow">{TG_ICON} 제휴문의</a>
    </div>
    <div class="footer-bottom">
      <span>© 2026 간다GO. All rights reserved.</span>
      <span>상호 간다GO · 전화예약 0508-202-4719</span>
    </div>
  </div>
</footer>"""


def breadcrumb_html(crumbs):
    parts = []
    for name, url in crumbs[:-1]:
        parts.append(f'<a href="{url}">{name}</a>')
    parts.append(crumbs[-1][0])
    return '<p class="breadcrumb">' + " › ".join(parts) + "</p>"


def schema_block(url, name, crumbs, faq, with_reviews=False):
    graph = [
        org_node(with_reviews=with_reviews),
        {"@type": "WebSite", "@id": WEBSITE_ID, "url": f"{SITE}/", "name": "간다GO",
         "publisher": {"@id": ORG_ID}, "inLanguage": "ko"},
        service_node(),
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": name,
         "inLanguage": "ko", "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": ORG_ID},
         "primaryImageOfPage": f"{SITE}/assets/og-cover.jpg"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u if u.startswith("/") else u}
            for i, (n, u) in enumerate(crumbs)]},
    ]
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>'


LONGTAIL_TOPICS = [
    ("이용 장소별 안내", [
        ("호텔·숙소 출장마사지 이용 기준", "/central-honam/use/hotel/"),
        ("오피스텔 홈타이 방문 안내", "/central-honam/use/officetel/"),
        ("자택 출장 케어 이용 방법", "/central-honam/use/home/"),
    ]),
    ("예약 전 확인", [
        ("심야 예약 가능 시간 확인", "/central-honam/check/time/"),
        ("아파트 공동현관 방문 확인", "/central-honam/check/apartment-access/"),
        ("외곽 지역 출장 이동비 기준", "/central-honam/check/travel-fee/"),
    ]),
    ("지역별 생활권", [
        ("천안 출장마사지 생활권 안내", "/central-honam/cheonan/"),
        ("대전 출장마사지 생활권 안내", "/central-honam/daejeon/"),
        ("세종 출장마사지 생활권 안내", "/central-honam/sejong/"),
        ("호남권 출장마사지 생활권 안내", "/central-honam/honam/"),
    ]),
    ("후기·안내", [
        ("실제 이용 후기 보기", "/central-honam/reviews/"),
        ("작성자·검수자 안내", "/central-honam/author/"),
        ("개인정보 처리방침", "/central-honam/check/privacy/"),
    ]),
]


def longtail_block(exclude_path=None):
    cols = []
    for title, links in LONGTAIL_TOPICS:
        lis = "\n".join(f'    <li><a href="{u}">{a}</a></li>' for a, u in links if u != exclude_path)
        if lis:
            cols.append(f'  <div class="link-group"><h3>{title}</h3><ul>\n{lis}\n  </ul></div>')
    return ('<section class="longtail">\n<h2>이런 주제도 함께 찾아보세요</h2>\n'
            '<div class="link-cols">\n' + "\n".join(cols) + '\n</div>\n</section>')


def faq_html(faq):
    if not faq:
        return ""
    items = ["<h2>자주 묻는 질문</h2>", '<div class="faq">']
    for i, (q, a) in enumerate(faq):
        op = " open" if i == 0 else ""
        items.append(f'<details{op}><summary>{q}</summary><p>{a}</p></details>')
    items.append("</div>")
    return "\n".join(items)


def whw_html(who, how, why):
    return f"""<div class="whw">
  <div class="info-card"><h3>Who</h3><p>{who}</p></div>
  <div class="info-card"><h3>How</h3><p>{how}</p></div>
  <div class="info-card"><h3>Why</h3><p>{why}</p></div>
</div>"""


def related_html(links):
    if not links:
        return ""
    lis = "\n".join(f'<li><a href="{u}">{a}</a></li>' for a, u in links)
    return f'<h2>관련 지역 보기</h2>\n<div class="link-group"><ul>\n{lis}\n</ul></div>'


def _admin_tree(path):
    """권역 메인 페이지에 시→구→동 링크 트리를 주입한다."""
    try:
        from regions_data import CITIES, HONAM_CITIES
    except ImportError:
        return ""
    for city in CITIES:
        if city["path"] != path:
            continue
        if city["gus"]:
            lines = []
            for gu in city["gus"]:
                gu_url = city["path"] + gu["slug"] + "/"
                dongs = " · ".join(f'<a href="{gu_url + d["slug"] + "/"}">{d["name"]}</a>' for d in gu["dongs"])
                lines.append(f'  <li><b><a href="{gu_url}">{gu["name"]}</a></b><br />{dongs}</li>')
            return ("\n<h2>행정구·행정동별 안내</h2>\n"
                    "<p>내 위치의 구와 동을 선택하면 해당 생활권의 이용 기준을 자세히 확인할 수 있습니다. "
                    "숫자 분동(1동·2동 등)은 대표 동 하나로 안내합니다.</p>\n<ul>\n" + "\n".join(lines) + "\n</ul>")
        dongs = " · ".join(f'<a href="{city["path"] + d["slug"] + "/"}">{d["name"]}</a>' for d in city["dongs"])
        return ("\n<h2>행정동·읍면별 안내</h2>\n"
                "<p>내 위치의 동·읍면을 선택하면 해당 생활권의 이용 기준을 자세히 확인할 수 있습니다. "
                "숫자 분동은 대표 동 하나로 안내합니다.</p>\n<ul>\n  <li>" + dongs + "</li>\n</ul>")
    if path == "/central-honam/honam/":
        lines = []
        for city in HONAM_CITIES:
            cnt = sum(len(g["dongs"]) for g in city["gus"]) if city.get("gus") else len(city["dongs"])
            lines.append(f'  <li><b><a href="{city["path"]}">{city["name"]}</a></b> — {city["intro"]}. 행정동 {cnt}곳 안내</li>')
        return ("\n<h2>도시별 행정동 안내</h2>\n"
                "<p>호남권은 시 단위 페이지에서 행정구·행정동별 개별 안내로 이어집니다. 내 도시를 선택하세요.</p>\n<ul>\n"
                + "\n".join(lines) + "\n</ul>")
    return ""


def render(page):
    url = SITE + page["path"]
    # 방침: noindex 미사용. 모든 페이지는 index, follow 로 고정한다.
    robots = "index, follow, max-image-preview:large"
    crumbs = page["crumbs"]
    faq = page.get("faq", [])
    with_reviews = bool(page.get("reviews"))
    body = page["body"] + _admin_tree(page["path"])
    if with_reviews:
        body += "\n" + reviews_html()
    if page.get("whw"):
        body += "\n" + whw_html(*page["whw"])
    body += "\n" + faq_html(faq)
    body += "\n" + related_html(page.get("related", []))
    body += "\n" + longtail_block(exclude_path=page["path"])
    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page['title']}</title>
  <meta name="description" content="{page['desc']}" />
  <link rel="canonical" href="{page.get('canonical', url)}" />
  <meta name="robots" content="{robots}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="간다GO" />
  <meta property="og:title" content="{page['title']}" />
  <meta property="og:description" content="{page['desc']}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/assets/og-cover.jpg" />
  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png" />
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
  <link rel="preload" as="image" href="/assets/hero.webp" fetchpriority="high" />
{HEAD_EXTRA}
  <link rel="stylesheet" href="/css/tokens.css" />
  <link rel="stylesheet" href="/css/style.css" />
  {schema_block(url, page['h1'], crumbs, faq, with_reviews=with_reviews)}
</head>
<body>
{HEADER}
<section class="hero hero-sub">
  <div class="wrap">
    {breadcrumb_html(crumbs)}
    <h1>{page['h1']}</h1>
  </div>
</section>
<main class="section">
  <div class="wrap">
    <div class="article-layout">
      <article class="article-main prose">
{body}
      </article>
      {ASIDE}
    </div>
  </div>
</main>
{FOOTER}
</body>
</html>
"""
    out_dir = os.path.join(ROOT, page["path"].strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    return url, robots


# ---- content imported from pages_content.py ----
from pages_content import PAGES  # noqa: E402

if __name__ == "__main__":
    written = []
    for p in PAGES:
        written.append(render(p))
    for u, r in written:
        flag = "noindex" if "noindex" in r else "index"
        print(f"[{flag}] {u}")
    print(f"\n총 {len(written)}개 페이지 생성 완료.")
