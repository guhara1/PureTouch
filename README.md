# 간다GO · PureTouch

천안·대전·세종·호남권 출장 케어 **지역 안내형** 정적 사이트.
상호 **간다GO** / 전화예약 **0508-202-4719**.

## 구조

```
index.html                      # 메인 (히어로 · 요금 · 지역 내부링크 · FAQ)
robots.txt / sitemap.xml
css/tokens.css                  # 프리미엄 팔레트 디자인 토큰 (Pretendard)
css/style.css                   # 컴포넌트 오버레이 · 레이아웃
central-honam/                  # 지역 안내 허브 + 22개 하위 페이지
  cheonan|daejeon|sejong|honam/ # 권역 메인
  area/…                        # 광역 생활권
  use/…                         # 이용 장소
  check/…                       # 예약 전 확인 · 개인정보 · 서비스 정책
  author/                       # 작성자·검수자 안내
tools/build_pages.py            # 지역/정책 페이지 생성기 (권역 메인에 행정 트리 자동 주입)
tools/pages_content.py          # 페이지별 콘텐츠 (여기만 수정)
tools/regions_data.py           # 행정구역 계층 데이터 (시→구→행정동, 대표동 통합)
tools/build_regions.py          # 행정동 개별 페이지 생성기 (205개)
tools/build_sitemap.py          # sitemap.xml 생성기
```

행정구역 페이지: 천안(2구 20동)·대전(5구 43동)·세종(20동/읍면)·호남 13개 시(구·동 178곳).
숫자 분동(1동·2동·3동)은 대표동 1개로 통합. 동 추가는 `regions_data.py` 수정 후
`python3 tools/build_regions.py && python3 tools/build_sitemap.py` 실행.

## 페이지 추가·수정

`tools/pages_content.py` 의 `PAGES` 를 편집한 뒤:

```bash
python3 tools/build_pages.py     # 페이지 재생성 (index.html, central-honam/index.html 은 손 관리)
```

`sitemap.xml` 은 noindex 를 제외하고 색인 대상만 포함합니다. 새 페이지 추가 후 재생성하세요.

## SEO 원칙 (구글 정책 준수)

- **E-E-A-T** — 작성자·검수자 안내, 개인정보 처리방침, 연락처 명시.
- **도어웨이 금지** — 지역명만 바꾼 복붙·출구별·노선별 페이지를 만들지 않음. 생활권 차이가 뚜렷한 페이지만 색인.
- **스키마** — WebPage / WebSite / Organization / BreadcrumbList / FAQPage / Service / ImageObject 만 사용.
  실제 매장 주소가 없으므로 `LocalBusiness`, 후기 없는 `Review`·`AggregateRating` 은 **사용하지 않음**.
- **메타 디스크립션** — 전 페이지 80자 이내.
- **롱테일 내부링크** — 이용 상황이 들어간 앵커텍스트 사용 ("천안 불당·두정 오피스텔 이용 전 확인" 등).
- **선호 썸네일** — `og:image` + schema `primaryImageOfPage` 로 지정.

## 남은 작업 (교체·확장)

- [ ] **텔레그램 핸들** — 푸터 `제작문의`·`제휴문의` 버튼은 현재 `https://t.me/ganda_go` **플레이스홀더**.
      `css/style.css` 가 아닌 각 HTML 및 `tools/build_pages.py` 의 `TG` 상수를 실제 핸들로 교체.
- [ ] **히어로 배경 이미지** — `assets/hero.jpg` 를 추가하면 자동으로 히어로 배경에 표시됨.
      가독성 스크림(어두운 오버레이)이 이미 깔려 있어 밝은 글씨 시인성이 유지된다.
      경로/투명도 조정은 `css/tokens.css` 의 `--hero-bg`, `css/style.css` 의 `.hero::before opacity`.
- [ ] `assets/og-cover.jpg`, `assets/logo.png` 실제 이미지 추가 (현재 경로만 지정됨).
- [ ] 도메인 확정 후 `SITE`(canonical/OG/sitemap)의 `gandago.co.kr` 교체.
- [ ] 지시서 1차-B/1차-C 확장(동별·읍면동, 산단·혁신도시 상세)은 `pages_content.py` 에 추가.
      **noindex 는 사용하지 않는다.** 모든 페이지는 `index, follow` 로 유지하며,
      본문이 얇은 지역은 페이지를 만들지 말고 상위 생활권 페이지로 통합하거나 canonical 처리한다.
