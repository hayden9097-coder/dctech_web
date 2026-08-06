# 디씨테크(DCTech) 홈페이지 — 현행 구조 정리

> 이 문서는 생성형 AI에게 개선 방안 도출을 요청하기 위한 현황 정리 자료입니다.
> 작성 기준일: 2026-08-06

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 회사 | 디씨테크(DCTech) — 산업용 펌프 AI 성능평가 솔루션 B2B 기업 |
| 사업 내용 | AI 알고리즘(KNN/PCA/SVM/GA) 기반 펌프 진단, 설비 빅데이터(SQL/NoSQL), 데이터 통합·변환 SW(PI System/ODBC/OPC) |
| 타겟 고객 | 스마트팩토리 담당자, 산업설비 관리자, B2B 엔지니어·의사결정권자 |
| 사이트 목적 | 기업 신뢰도 제고 + 고객 문의(Lead) 전환 |
| 기존 사이트 | www.dctech.co.kr (구버전, 별도 운영 중) |
| 신규 사이트 | https://dctechweb.netlify.app |
| 소스 저장소 | https://github.com/hayden9097-coder/dctech_web (main 브랜치) |
| 운영 주체 | 비개발자가 콘텐츠를 직접 편집할 수 있어야 한다는 것이 핵심 요구사항 |

---

## 2. 기술 스택

### 정적 사이트 생성기
- **Eleventy (11ty) v2.0.1** — Node.js 기반 SSG
- 템플릿 엔진: **Nunjucks(.njk)** + **Markdown(.md)**
- 빌드 산출물: `dist/` (정적 HTML)
- 런타임 서버 없음 (100% 정적 사이트)

### 스타일링
- **Tailwind CSS — CDN 방식** (`https://cdn.tailwindcss.com?plugins=typography,forms`)
- 브라우저에서 런타임 JIT 컴파일 (빌드 타임 purge 없음)
- 설정은 각 HTML `<head>` 내 인라인 `tailwind.config` 스크립트로 주입
- 별도 CSS 빌드 파이프라인(PostCSS 등) **없음**

### CMS (콘텐츠 관리)
- **Decap CMS v3** (구 Netlify CMS), unpkg CDN에서 로드
- 백엔드: **GitHub** (`backend: name: github`)
- 인증: GitHub OAuth (Netlify를 OAuth 중개자로 사용, callback `https://api.netlify.com/auth/done`)
  - ※ Netlify Identity를 신규 사이트에서 제공하지 않아 Git Gateway → GitHub OAuth로 전환한 이력 있음
- 관리자 경로: `/admin/`
- 로컬 편집 지원: `local_backend: true` (`npx decap-server` 병행 실행 시)
- 미디어 업로드 경로: `public/images/uploads/` → 공개 경로 `/images/uploads/`

### 호스팅 / 배포
- **Netlify**
- 빌드 명령: `npm run build` (= `eleventy`)
- 배포 디렉토리: `dist`
- 설정 파일: `netlify.toml`

### 의존성
```json
"devDependencies": { "@11ty/eleventy": "^2.0.1" }
```
- 운영 의존성 없음. Tailwind·Decap 모두 CDN 로드.

---

## 3. 배포 파이프라인

```
[사용자 A] 로컬에서 코드 수정 → git push
                                    ↓
                        GitHub (hayden9097-coder/dctech_web, main)
                                    ↑
[사용자 B] /admin 접속 → GitHub OAuth 로그인 → 폼으로 콘텐츠 편집 → 저장
           (Decap CMS가 GitHub API로 직접 커밋)
                                    ↓
                        Netlify가 main 브랜치 push 감지
                                    ↓
                        npm run build (Eleventy) → dist/
                                    ↓
                        https://dctechweb.netlify.app 반영 (1~2분 소요)
```

- CI/CD 별도 구성 없음 (Netlify 기본 Git 연동만 사용)
- 스테이징/프리뷰 환경 별도 구성 없음 (Netlify Deploy Preview 기본값만)
- 테스트 코드 없음, 린터 없음

---

## 4. 디렉토리 구조

```
dctech_web_home/
├── eleventy.config.js        # Eleventy 설정 (컬렉션, 커스텀 필터)
├── netlify.toml              # 배포 설정
├── package.json
├── .gitignore                # node_modules/, dist/, .cache/
├── admin/
│   ├── index.html            # Decap CMS 진입점
│   └── config.yml            # CMS 컬렉션·필드 정의 (핵심 파일)
├── public/                   # 정적 자산 (빌드 시 루트로 복사)
│   └── images/
│       ├── dctech-logo.png
│       └── uploads/          # CMS 업로드 파일
│           └── dctech_favicon.png
└── src/
    ├── _data/                # 전역 데이터 (JSON) — 고정 페이지 콘텐츠
    │   ├── site.json         # 회사명·로고·주소·연락처 (전 페이지 공통)
    │   ├── home.json
    │   ├── about.json
    │   ├── solutions.json
    │   ├── downloads.json
    │   └── contact.json
    ├── _includes/            # 레이아웃
    │   ├── base.njk          # 공통 레이아웃 (헤더/푸터/head)
    │   ├── product.njk       # 제품 상세 레이아웃
    │   ├── post.njk          # 소식 상세 레이아웃
    │   └── case.njk          # 도입사례 상세 레이아웃
    ├── index.njk             # 홈
    ├── about.njk             # 회사소개
    ├── products.njk          # 제품 목록
    ├── solutions.njk         # 핵심 솔루션
    ├── cases.njk             # 도입사례 목록
    ├── downloads.njk         # 자료실
    ├── news.njk              # 소식 목록
    ├── contact.njk           # 문의
    ├── products/             # 제품 상세 (Markdown, CMS로 추가 가능)
    │   ├── pump-ai-diagnostics.md
    │   └── data-integration-sw.md
    ├── news/                 # 소식 게시글 (Markdown, CMS로 추가 가능)
    │   ├── 2026-hello.md
    │   └── pump-ai-release.md
    └── cases/                # 도입사례 (Markdown, CMS로 추가 가능)
        ├── cooling-pump.md
        └── feedwater-pump.md
```

### Eleventy 커스텀 설정 (`eleventy.config.js`)
- `public/` → 사이트 루트로 passthrough copy
- `admin/` → 그대로 passthrough copy
- 컬렉션 3종:
  - `cases` — `order` 필드 오름차순 정렬
  - `products` — `order` 필드 오름차순 정렬
  - `news` — `date` 내림차순 (최신순)
- 커스텀 필터 3종:
  - `date` — `2026-07-31` → `2026.07.31`
  - `limit(n)` — 배열 앞 n개
  - `json`

---

## 5. 페이지 / 라우팅 구조

총 **14개 HTML 페이지** 생성 (고정 8 + 상세 6)

| 메뉴 | URL | 템플릿 | 콘텐츠 소스 | CMS 글 추가 |
|---|---|---|---|---|
| 홈 | `/` | index.njk | `_data/home.json` + products/news 컬렉션 | — |
| 회사소개 | `/about/` | about.njk | `_data/about.json` | — |
| 제품소개 | `/products/` | products.njk | `products/*.md` | ✅ |
| ↳ 제품 상세 | `/products/{slug}/` | product.njk | 개별 md | ✅ |
| 핵심 솔루션 | `/solutions/` | solutions.njk | `_data/solutions.json` | — |
| 도입 사례 | `/cases/` | cases.njk | `cases/*.md` | ✅ |
| ↳ 사례 상세 | `/cases/{slug}/` | case.njk | 개별 md | ✅ |
| 자료실 | `/downloads/` | downloads.njk | `_data/downloads.json` | ✅ (목록 항목) |
| 소식 | `/news/` | news.njk | `news/*.md` | ✅ |
| ↳ 소식 상세 | `/news/{slug}/` | post.njk | 개별 md | ✅ |
| 문의 | `/contact/` | contact.njk | `_data/contact.json` | — |
| 관리자 | `/admin/` | (Decap CMS SPA) | — | — |

### 페이지별 섹션 구성

**홈** — 히어로(카피+CTA 2종+통계 3지표) → 소개문 → 하이라이트 카드 6개 → 제품 라인업(최대 3) → 최근 소식(최대 4) → CTA 배너

**회사소개** — 페이지 히어로 → 소개문 + 비전 인용구 → 핵심가치 4카드 → 연혁 타임라인(7항목, 실제 회사 연혁 반영)

**핵심 솔루션** — 히어로 → 기술 3종 상세(각각 좌측 설명 + 우측 다크카드 기능목록) → 진단 프로세스 4단계 → CTA

**제품소개** — 히어로 → 제품 카드 그리드(3열) → CTA
**제품 상세** — 히어로 → 좌측 본문(Markdown) + 우측 사이드바(주요특징 / 사양표 / 카탈로그 PDF 다운로드 / 문의 CTA)

**도입 사례** — 히어로 → 사례 카드 2열
**사례 상세** — 히어로 → 도입 전/후 지표 대비 카드 → 본문(배경/과제/접근/결과)

**자료실** — 히어로 → 자료 목록(파일 있으면 다운로드 버튼, 없으면 "준비중") → 자료요청 CTA

**소식** — 히어로 → 게시글 리스트(분류 뱃지 + 날짜 + 썸네일 + 요약)
**소식 상세** — 히어로 → 썸네일 → 본문 → 첨부파일 다운로드

**문의** — 히어로 → 좌측 연락처 3종 + FAQ 아코디언 / 우측 문의 폼

---

## 6. CMS 편집 구조 (`admin/config.yml`)

총 **9개 컬렉션**

| 컬렉션 | 타입 | 대상 파일 | 편집 가능 항목 |
|---|---|---|---|
| 사이트 설정 | 단일 파일 | `_data/site.json` | 회사명, 로고, 파비콘, 메타설명, 주소, 전화 2종, 이메일, 저작권연도 |
| 홈 페이지 | 단일 파일 | `_data/home.json` | 히어로 카피, CTA 버튼 텍스트·링크, 통계지표(리스트), 하이라이트 카드(리스트), CTA 배너 |
| 회사소개 페이지 | 단일 파일 | `_data/about.json` | 타이틀, 소개문, 인용구, 핵심가치(리스트), 연혁(리스트) |
| 솔루션 페이지 | 단일 파일 | `_data/solutions.json` | 기술 3종(제목/요약/상세/기능목록), 프로세스 4단계 |
| 문의 페이지 | 단일 파일 | `_data/contact.json` | 타이틀, 안내문, 개인정보문구, FAQ(리스트) |
| 자료실 | 단일 파일 | `_data/downloads.json` | 자료 목록(자료명/설명/분류/파일업로드/형식표시) |
| 제품소개 | 폴더(다건) | `src/products/` | 제품명, 분류, 순서, 요약, 대표이미지, 주요특징, 사양표, 카탈로그 PDF, 본문(MD) |
| 소식 | 폴더(다건) | `src/news/` | 제목, 분류(select 5종), 작성일, 요약, 썸네일, 첨부파일, 본문(MD) |
| 도입 사례 | 폴더(다건) | `src/cases/` | 제목, 태그, 순서, 요약, 도입전/후 지표(리스트), 본문(MD) |

- 위젯 사용: `string`, `text`, `number`, `select`, `datetime`, `image`, `file`, `list`, `markdown`, `hidden`
- 모든 라벨이 한국어로 작성되어 비개발자 접근성 고려됨

---

## 7. 디자인 시스템

### 컬러 (Tailwind 확장 토큰)
```js
navy:     { 950: '#050b18', 900: '#0a1730', 800: '#0f2247', 700: '#153161' }
techblue: { 500: '#2f7dfa', 400: '#5b9bff', 300: '#8ec0ff' }
```
- 신뢰감(네이비) + 혁신(테크블루) 컨셉
- 보조: Tailwind 기본 `slate` 계열

### 타이포그래피
- `fontFamily.sans`: `Pretendard` → `Noto Sans KR` → `system-ui` → `sans-serif`
- ※ **웹폰트 로드 링크 없음** — 사용자 PC에 미설치 시 시스템 폰트로 대체됨

### 레이아웃 패턴
- 고정 헤더: `fixed`, 높이 `h-16`, `bg-navy-950/90` + `backdrop-blur`, 본문 `pt-16`
- 컨테이너: 주로 `max-w-7xl`, 상세형 페이지는 `max-w-3xl~5xl`, 좌우 `px-6 lg:px-8`
- 섹션 리듬: 다크(navy) ↔ 라이트(white/slate-50) 교차 배치
- 카드: `rounded-2xl` + `border` + `card-hover`(호버 시 -6px 상승 + 그림자)
- 히어로 배경: `gradient-hero`(radial+linear 그라디언트) + `grid-overlay`(40px 격자 패턴)
- 반응형 분기점: **lg(1024px)** — 이상은 데스크톱 내비, 미만은 햄버거 메뉴
- 버튼: 주 CTA `bg-techblue-500`, 보조 CTA `bg-white/5 + border`

### 아이콘
- 인라인 SVG (Heroicons 계열 stroke 아이콘) 직접 삽입, 아이콘 라이브러리 미사용

---

## 8. 현재 알려진 제약 및 미완성 항목

### 기능적 결함
1. **문의 폼이 실제로 동작하지 않음** — `<form>`에 `action`이나 Netlify Forms 속성(`data-netlify`)이 없어 제출해도 아무 데도 전송되지 않음. **가장 시급한 문제** (사이트 목적이 Lead 확보인데 폼이 무동작)
2. 자료실의 PDF가 전부 미업로드 상태 → 3개 항목 모두 "준비중" 표시
3. 제품·소식·사례 콘텐츠가 대부분 샘플 데이터 (실제 검증된 내용 아님)

### 콘텐츠 신뢰성
4. 홈 히어로의 통계 지표(**98.4% 진단정확도, -32% 비용절감**)는 근거 없이 작성된 플레이스홀더 카피 — 실제 수치로 교체 또는 삭제 필요
5. 도입 사례 2건은 가상 시나리오 (하단에 "예시" 고지 문구는 있음)

### 성능
6. **Tailwind CDN 런타임 컴파일** — 프로덕션 비권장 방식. 초기 렌더 지연(FOUC), 불필요한 JS 실행, 미사용 CSS 미제거
7. 웹폰트 미로드로 의도한 타이포그래피(Pretendard) 미적용 가능성
8. 이미지 최적화 파이프라인 없음 (수동 리사이즈만 수행)

### SEO / 분석
9. **Open Graph / Twitter Card 메타태그 없음** — 카톡·링크드인 공유 시 미리보기 없음
10. `sitemap.xml`, `robots.txt` 없음
11. 404 페이지 없음
12. 웹 분석 도구(GA4 등) 미설치 — 유입·전환 측정 불가
13. 구조화 데이터(JSON-LD Organization/Product) 없음

### 운영
14. 테스트·린터·CI 없음
15. 접근성(a11y) 검증 미실시 — 폼 label 연결, 색 대비, 키보드 내비게이션 등 미확인
16. 다국어(영문) 미지원 — B2B 수출 고려 시 필요할 수 있음

### 진행 중 (미커밋)
17. 기존 사이트(dctech.co.kr)에서 가져온 이미지들이 `public/images/`에 다운로드만 된 상태이며 아직 페이지에 반영되지 않음
   - `solution-diagram.jpg` (1800×814, 190KB) — PUMP 성능평가 솔루션 전체 흐름도
   - `tech_01.png` (설비 진단 대시보드), `tech_02.png` (진동 스펙트럼 분석), `tech_03.png` (데이터 통합 개념도)
   - `organizationalchart.png` (조직도)
   - `solution_01.png` (6.7MB 원본), `solution-diagram.png` (1.3MB) — 정리 대상

---

## 9. 생성형 AI에게 요청할 사항 (예시 프롬프트)

위 내용을 붙여넣은 뒤 아래와 같이 질문하면 좋습니다.

```
위는 우리 회사(B2B 산업용 AI 솔루션) 홈페이지의 현행 구조입니다.
다음 관점에서 개선 방안을 우선순위와 함께 제안해 주세요.

1. [전환율] B2B 리드 확보 관점에서 정보 구조와 CTA 배치의 문제점과 개선안
2. [기술] Tailwind CDN, 이미지 최적화, 빌드 파이프라인 등 성능 개선 로드맵
3. [SEO] 검색 유입 확보를 위해 지금 당장 해야 할 것과 중기 과제
4. [콘텐츠] 산업 설비 담당자가 신뢰할 만한 콘텐츠 전략 (어떤 페이지·글을 추가해야 하는가)
5. [운영] 비개발자가 지속 운영 가능한 구조를 유지하면서 확장하는 방법

각 항목마다 '왜 문제인지 → 어떻게 바꿀지 → 예상 효과'를 구체적으로 써 주시고,
투입 대비 효과가 큰 순서로 정렬해 주세요.
```

---

## 부록: 주요 명령어

```bash
npm start          # 로컬 개발 서버 (Eleventy --serve)
npm run build      # 프로덕션 빌드 → dist/
npx decap-server   # CMS 로컬 편집 프록시 (npm start와 함께 실행)
```
