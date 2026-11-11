# Janus System 제품 상세페이지 (전용 템플릿)

Janus System(야누스 시스템)은 수집·Edge·Historian·Studio·상태감시·미디어·공간 확장을 하나로 묶은 플랫폼이라, 일반 제품 상세(본문 + 오른쪽 박스)로는 구조를 보여 주기 어렵다. 그래서 AssetPulse 와 같은 방식으로 **Janus 제품만** 전용 상세 템플릿을 쓴다. CMS(Decap) 필드와 일반 제품 페이지는 그대로다.

## 1. 현재 CMS 구조 (조사 결과, 2026-11-11, origin/main f2d2fe5 기준)

| 항목 | 내용 |
|---|---|
| 콘텐츠 | `src/products/*.md` (Eleventy 컬렉션 `products`, `order` 오름차순). 제품 목록 `/products/`, 홈 "제품 라인업"(앞 3개), 상세 `/products/<slug>/` |
| CMS 필드 | 제품명 `title` · 제품 분류 `category` · 상세 페이지 템플릿 `template` · 표시 순서 `order` · 한줄 요약 `summary` · 대표 이미지 `image` · **대표 이미지 표시 방식 `image_fit`(이번에 추가)** · 주요 특징 `features`(문자열 목록) · 제품 사양 `specs`(항목명/내용) · 제품 카탈로그 PDF `brochure` · 상세 설명 `body`(Markdown) + 숨김 `layout: product.njk` |
| 렌더러 | `src/_includes/product.njk` → `base.njk`(헤더·푸터·메타·OG). 전용 템플릿은 레지스트리로 선택(2절) |
| 현재 제품 | AssetPulse(`data-integration-sw.md`, `template: assetpulse`, order 2), Janus(`janus-system.md`, `template: janus`, order 3). **PumpGuard(`pump-ai-diagnostics`)는 소유자가 CMS 로 삭제함(4e8cd6c) — 복원하지 않았다** |
| 사이트 검색 | 없음(정적 사이트에 검색 기능 없음). 검색 별칭(Janus/야누스) 작업 대상 아님. 페이지 본문·메타 설명에 "Janus System", "야누스 시스템"이 모두 들어 있어 외부 검색엔진에는 둘 다 노출된다 |

## 2. 전용 템플릿 트리거 (Template registry)

- 트리거: 제품 문서의 **`template: janus`** (CMS "상세 페이지 템플릿" → "Janus System 전용 템플릿").
- `src/_data/productTemplates.json` 이 `template 값 → 템플릿 파일` 매핑이다.
  ```json
  { "assetpulse": "product-assetpulse.njk", "janus": "product-janus.njk" }
  ```
- `product.njk` 는 `productTemplates[template]` 가 있으면 그 파일을 include 하고, 없음·`default`·미등록 값은 기존 일반 템플릿을 그대로 쓴다. if/else 가 제품마다 늘지 않는다. 새 전용 템플릿 = JSON 한 줄 + `admin/config.yml` 선택지 한 줄.
- 슬러그·숫자 ID 하드코딩 없음.
- 회귀: 레지스트리 도입 전후 `dist` HTML 이 바이트 단위로 같음을 확인(AssetPulse 상세·제품 목록·홈·회사소개·문의·자료실·솔루션). Janus 추가 후에도 AssetPulse 상세는 바이트 동일, 제품 목록·홈은 Janus 카드 추가분만 다르다.

## 3. 제품 카드 이미지 (cube placeholder 원인과 해결)

- 원인: `products.njk`·`index.njk` 의 카드가 `image` 가 비어 있으면 네이비 바탕 상자(cube) 아이콘을 그린다. Janus 제품 문서 자체가 없었고, 로고를 넣어도 카드가 `object-cover` 라 정사각 로고가 4:3 영역에서 잘린다.
- 해결:
  - Janus 대표 이미지에 **공식 로고**를 지정(`/images/uploads/janus-system-logo.webp`).
  - 카드 이미지 영역을 `src/_includes/product-card-media.njk` 로 공통화하고, CMS 필드 **"대표 이미지 표시 방식"(`image_fit`: `cover` 기본 / `contain` 로고)** 을 추가. `contain` 이면 흰 바탕 + 여백(p-6/p-8) + 가운데 + `object-contain` 으로 전체가 보인다. AssetPulse 등 기존 제품은 값이 없어 `cover` 그대로(출력 동일).
  - cube 아이콘은 "대표 이미지가 정말 없을 때"의 기본값으로만 남는다(덮어쓰기 아님).

## 4. Janus 공식 로고

| 항목 | 내용 |
|---|---|
| 원본 | `/home/dc/dev/janus/docs/brand/janus-logo.png` (1254×1254 PNG, 흰 바탕, "Janus System" lock-up). Janus 제품의 파비콘·앱 마크가 모두 이 파일에서 나왔다(BRAND-01). 공식 SVG lock-up 은 없음(앱의 `BrandMark.tsx` 는 마크만 벡터화한 것) → 원본 PNG 사용 |
| 사이트 파일 | `public/images/uploads/janus-system-logo.webp` (800×800, 17.6KB). 원본을 축소만 했고, 원본 바탕의 254 회색을 255 흰색으로 맞춰 흰 카드에서 사각형 경계가 보이지 않게 했다. 마크·글자는 손대지 않음 |
| 카드 | contain · 가운데 · 흰 바탕 · 여백 |
| 히어로 | 네이비 히어로에서 흰 타일(88px) 안에 표시(흰 바탕용 로고라 어두운 바탕에 직접 올리지 않음) |
| alt | 히어로: "{제품명} 로고"(현재 "Janus System 산업 데이터 통합 플랫폼 로고"), 카드: 제품명 |

## 5. 디자인 시안 비교 (Taste)

5개 시안을 같은 콘텐츠·같은 헤더/푸터 기준으로 비교했다(5점 만점). Taste draw(`saas`, technical, product-ui, `--keep palette,type`)는 `product-performs` / `quiet-instrument` / `dense-tiles` 를 냈고, 이 중 "제품 화면이 일하는 모습을 보여 준다"는 `product-performs` 의 원칙만 받아들였다(HTML 로 가짜 UI 를 그리는 부분은 요구사항상 제외 — 실제 화면 캡처만 사용).

| 기준 | A Enterprise Platform | **B Industrial Data Flow** | C Studio-focused | D Physical AI Ready | E Minimal Enterprise |
|---|---|---|---|---|---|
| Brand Fit | 5 | **5** | 4 | 3 | 4 |
| Industrial Feel | 4 | **5** | 3 | 3 | 2 |
| Product Understanding | 4 | **5** | 3 | 3 | 3 |
| Screenshot Utilization | 3 | **4** | 2 | 2 | 2 |
| Technical Credibility | 4 | **5** | 4 | 2 | 3 |
| CMS Compatibility | 5 | **5** | 5 | 5 | 5 |
| Responsive | 4 | **4** | 4 | 4 | 5 |
| Catalog Consistency | 5 | **5** | 4 | 3 | 3 |
| 합계 | 34 | **38** | 29 | 25 | 27 |

- A: 히어로 → 구조도 → Studio → Historian → 모듈. 정돈됐지만 "현장 데이터가 어디서 와서 어디로 가는지"가 늦게 나온다.
- **B(선정)**: 장비 → Edge → Protocol Studio → Historian → UI Studio → 상태감시/미디어 → 공간/Physical AI → 구성도 → 도입. 페이지 순서 자체가 Janus 의 데이터 경로라 처음 보는 사람이 9개 질문(무엇·수집·Edge·Protocol Studio·Historian·UI Studio·확장·Physical AI·설치)에 순서대로 답을 얻는다. AssetPulse 페이지(단색 네이비 히어로, 흰/연회색/네이비 띠)와 같은 계열이다.
- C: Protocol Studio + UI Studio 중심. 차별점은 크지만 깨끗한 Studio 화면이 몇 장 뿐이라 화면이 작아지고, Historian·Edge 가 묻힌다.
- D: 미디어·공간·로봇 강조. 공간·LiDAR·로봇이 PARTIAL/연동 기반이라 과장 위험이 가장 크다.
- E: 흰 바탕 + 큰 스크린샷. 큰 대시보드 실화면(깨끗한 데이터)이 없어 성립하지 않는다.

이 페이지의 아이디어 문장: **"Janus 가 실제로 데이터를 옮기는 경로(현장 장비 → Edge → Central → 화면)가 페이지의 척추가 된다."** 섹션마다 그 경로의 한 정거장이고, 각 정거장은 그 단계의 실제 화면 또는 구성도로 증명한다.

## 6. 페이지 구성과 CMS 매핑

| 순서 | 섹션 (id) | 내용 | 데이터 |
|---|---|---|---|
| 1 | Hero | 로고 타일, h1, 소개 문장, CTA(소개서·문의·시스템 구성 보기), 제품명·분류, 그 아래 전체 폭 실제 관제 대시보드 화면(`hero.img.wide: true`; false 면 예전처럼 오른쪽 5칸) | CMS: `image`, `title`, `category`, `brochure` / janus.json `hero` |
| 2 | 하나의 플랫폼에서 하는 일 (`#features`) | 8개 핵심 가치 | **CMS `features`** (`featureItems` 필터: " — " 앞 제목/뒤 설명) + CMS `summary` |
| 3 | 수집 (`#collect`) | 프로토콜 5그룹 | janus.json `collect` |
| 4 | Janus Edge (`#edge`) | 흐름(현장→Edge→Central), 4개 역할, Edge 콘솔 장비 시험·초기 설정 화면 | janus.json `edge` |
| 5 | Protocol Studio (`#protocol-studio`) | 4단계 묶음 + 소스 마법사 화면 | janus.json `studio` |
| 6 | Historian (`#historian`) | 원시값·계산값·현재값·추세·집계·이력 조회/내보내기 + 다중 펜 추세 실화면(`historian.image`) | janus.json `historian` |
| 7 | UI Studio (`#ui-studio`) | 10개 기능 + 테마 카탈로그(`ui.catalog`) + 위젯 목록 화면 2장 | janus.json `ui` |
| 8 | 상태감시·알람 (`#condition`) | 두 블록, 블록마다 실화면(`blocks[].image`: 파형/FFT, 알람 현황) | janus.json `condition` |
| 9 | 미디어 (`#media`) | 기능 목록 + Edge 콘솔 카메라 시험 화면 | janus.json `media` |
| 10 | 공간·Physical AI (`#physical-ai`) | 배치도 실화면(`spatial.image`) + 감지→수집→분석→표시→판단→제어, 확장 구조/연동 기반 표현, 제어 범위 안내 | janus.json `spatial` |
| 11 | 시스템 구성 (`#architecture`) | FIELD / EDGE / CENTRAL / CLIENT SVG(데스크톱), 같은 내용의 세로 목록(모바일) | janus.json `arch` |
| 12 | 도입 형태 (`#deployment`) | On-Premise · Edge+Central · 폐쇄망 · 모듈형, 적용 분야 | janus.json `deploy` |
| 13 | 제품 사양 (`#specs`) | 제품명·분류 + 사양 표 | **CMS `title`, `category`, `specs`** |
| 14 | 상세 제품 소개 (`#detail`) | Markdown 본문 | **CMS `body`** |
| 15 | 문의 | 소개서(있을 때만)·문의하기(`/contact/`) | CMS `brochure` / janus.json `cta` |

- 메타: `<title>` = CMS 제품명, description = CMS 한줄 요약, OG 이미지 = CMS 대표 이미지(`base.njk` 기존 구조 그대로).
- 카탈로그 PDF: `brochure` 가 비어 있으면 다운로드 버튼을 **만들지 않는다**(dead button 없음). PDF 를 CMS 에 올리면 히어로·하단에 "제품 소개서 다운로드"(`download` 속성)가 생기고 "문의하기"는 보조 버튼으로 바뀐다. 자료실의 "Janus System 데이터 통합/변환/관제 SW 소개서" 항목은 파일이 비어 있는 그대로 두었다.
- 문의: 기존 `/contact/` 재사용(새 문의 시스템 없음).
- 고정 문구는 `src/_data/janus.json` 에 있어 코드 없이 고칠 수 있다(CMS 편집 화면에는 노출하지 않음 — AssetPulse 와 같은 방식).

**CMS 반영 검증**: 저장소 사본(scratch)에서 Janus 문서의 10개 필드(제품명·분류·순서·한줄 요약·대표 이미지·표시 방식·주요 특징·제품 사양·PDF·상세 설명)를 바꿔 빌드 → 상세·목록·`<title>` 에 모두 반영됨을 확인하고 사본을 삭제했다(제품명 8곳, 분류 2, 요약 4, 이미지 3, 특징 제목/설명 각 1, 사양 1, PDF 버튼 2, 본문 1; 순서 0 → 목록 맨 앞; 표시 방식 cover → 카드 object-cover). Decap 편집 화면 자체는 GitHub 로그인(또는 `decap-server`)이 필요해 실행하지 않았다. `admin/config.yml` 은 정상 파싱되고(`/admin/` 로그인 화면까지 오류 없음), Janus 문서의 모든 front matter 키가 CMS 필드로 정의되어 있어 CMS 저장 시 누락되지 않는다.

## 7. 화면 이미지 (Screenshot inventory)

모두 **실제 Janus UI** 캡처를 잘라 낸 것이다. 그려 넣은 UI·mock 없음. 내부 주소·호스트명·계정·`QA/test/sample/demo` 문자열이 보이지 않게 잘랐다.

| 파일 (`public/images/janus/`) | 원본 화면 | 크기 | 출처 |
|---|---|---|---|
| `ui-studio-theme-catalog.webp` | UI Studio › 애플리케이션 설정 › 테마 › 테마 카탈로그(9개) | 554×542 | 랩 Central 0.31.0(127.0.0.1:28081), 쓰기 차단 스크립트로 읽기 전용 접속 |
| `protocol-studio-wizard.webp` (+`-800`) | Protocol Studio › 소스 마법사 1단계(원본 유형). 이름/코드 입력값은 저장하지 않음 | 1128×364 | 랩 Central |
| `ui-studio-widgets-value.webp`, `ui-studio-widgets-chart.webp` | UI Studio 편집기 › 위젯 목록(값·상태 / 차트) | 282×326, 282×324 | 랩 Central |
| `edge-field-test.webp` (+`-800`) | Edge 콘솔 › 장비 시험(Modbus Unit ID 찾기, 읽기 전용) | 1145×472 | 임시 로컬 Edge 콘솔 |
| `edge-setup.webp` | Edge 콘솔 › 초기 설정 10단계 | 678×293 | 임시 로컬 Edge 콘솔 |
| `edge-camera-test.webp` (+`-800`) | Edge 콘솔 › 카메라 시험 › 카메라 시운전 순서 9단계 | 910×470 | 임시 로컬 Edge 콘솔 |
| `dashboard-overview.webp` (+`-800`) — **히어로** | 사용자 화면(USER) › UI Studio 로 만든 앱 "1공장 설비 관제" › 설비 현황 페이지: 값 카드 3개·알람 카운터·베어링 진동 24시간 추세(주의선 4.5)·주의 설비·게이지·공급/환수 온도 추세·최근 알람. 왼쪽 앱 메뉴와 상단 셸은 잘라 냄 | 1600×1045 | 발표용 로컬 인스턴스 |
| `historian-trend.webp` (+`-800`) — Historian | 같은 앱 › 추세 분석 페이지: 다중 펜 트렌드(2호기 베어링 진동·온도·모터 전류, 3축, 최근 24시간) + 24시간 평균·최소/최대·평균 온도·1시간 변화율 집계 카드 | 1600×879 | 발표용 로컬 인스턴스 |
| `condition-fft.webp` (+`-800`) — 상태감시 블록 | 관리자 › 설비 상태감시 › 냉각수 순환펌프 2호기 › 신호 분석: 분석 완료 파형의 시간 파형 + FFT 스펙트럼 + 베어링 결함 주파수 표시선(6309 베어링) | 1100×1041 | 발표용 로컬 인스턴스 |
| `alarm-list.webp` (+`-800`) — 알람 블록 | 관리자 › 알람 현황(열린 알람 전체): 발생·미확인 / 발생·확인됨(확인자·시각) / 복귀·미확인, 심각도, 태그, 유형(HI·HIHI·LO), 발생 값·시각. 왼쪽 관리 메뉴는 잘라 냄 | 1400×476 | 발표용 로컬 인스턴스 |
| `spatial-map.webp` (+`-800`) — 공간·Physical AI | 사용자 화면 › 배치도 페이지: MAP_2D 위젯(공간 패키지, LOCAL_CARTESIAN 지도, 배경 타일 없음) 구역 7개·고정 설비 4대·지게차 1대 위치 + 주의 설비·알람 | 1600×870 | 발표용 로컬 인스턴스 |
| `ui-studio-theme-catalog.webp` | (위치 이동) 히어로 → UI Studio 섹션 오른쪽 위 | 554×542 | 랩 Central |

- 임시 로컬 Edge 콘솔: 이미 빌드된 `edge-console` 바이너리를 빈 상태 폴더(`~/.cache/janus-webshot/elc-state`)와 빈 루프백 포트(127.0.0.1:28697)로 띄우고, 부트스트랩 시험 계정으로 로그인해 캡처한 뒤 해당 PID 만 종료했다. 사용자의 Edge 콘솔(28643)과 랩 서비스는 건드리지 않았다.
- 랩 Central 은 쓰기 요청(POST/PUT/PATCH/DELETE)을 막는 init 스크립트로 접속했고, 끝에 로그아웃했다. 프레젠테이션용 데이터는 만들지 않았다(아래 9절).
- 최적화: WebP(q84–90), 넓은 이미지는 800w 변형 + `srcset/sizes`, 모든 화면에 `width/height`·`loading="lazy"`·`decoding="async"`. 페이지 이미지 합계는 12절 참고.

### 7-1. 발표용 데이터와 캡처 환경 (2026-11-11)

- **어디서**: 랩(.88 Central·.86 Edge)과 사용자 서비스는 건드리지 않았다. Janus 저장소(HEAD 738f9c06, 릴리스 0.31.1)에서 바이너리만 `~/.cache/janus-present/bin` 으로 빌드하고(저장소 무변경), 웹 화면은 같은 0.31.1 릴리스의 `share/web` 사본을 썼다. 전용 DB 컨테이너 `janus-present-pg`(`timescale/timescaledb:2.30.1-pg18`, 루프백 임의 포트, 볼륨 `janus-present-pgdata`) + `cmd/migrate up` + Core(`JANUS_ENV=development`, 루프백 임의 포트). 작업이 끝난 뒤 컨테이너·볼륨·프로세스·비밀값 파일을 모두 지웠다.
- **어떻게**: 모두 제품의 공개 API/화면으로 만들었다(DB 직접 수정 없음, 실 장비 쓰기·제어 명령·실 카메라 없음). 초기 설정 API로 관리자 생성(TOTP 2단계 인증 등록) → Admin API 로 사이트 "1공장", 구역 2, 설비 5(냉각수 순환펌프 1·2호기, 냉각탑 송풍기, 보일러 급수펌프, 지게차 1호), 단위 8, 태그 32 → 알람 규칙 17(HI·HIHI·LO) → 상태감시 측정 포인트 11, 베어링 6309 지정, 진동 파형 5건 업로드 → 제품의 상태감시 분석 작업기(릴리스 `share/calc`, 전용 CALC_SERVER 인스턴스 토큰)로 FFT·진단 → 공간 패키지 설치, 배치도(지도 1, 버전 승격, 구역 7, 설비 엔티티 4 + 지게차 엔티티 1, 속도 규칙 1) → UI Studio 앱 "1공장 설비 관제"(4페이지) 게시 → 사용자 계정 "현장 운전원"(USER 역할 + 1공장 접근).
- **값**: Core 의 Standard Telemetry v1 수집 리스너(`/ingest/v1/telemetry`, 상태감시 CM-1 시험의 `cm-feed.py` 와 같은 경로)로 3일치 이력(60초, 최근 8시간은 10초) + 5초 주기 실시간 값을 보냈다. 값은 하루 부하 곡선 + 느린 변동 + 잡음 모델이고, 2호기 베어링 진동이 40시간에 걸쳐 오르는 이상 진행, 급수펌프 베어링 온도 상승, 일시 압력 저하·송풍기 진동 상승(발생 후 복귀)을 넣었다. 플래그 0(시뮬레이터 표시 없음)으로 보냈기 때문에 화면에 "시뮬레이터 데이터" 배지가 없다 — **실제 현장 값이 아니므로 페이지의 새 화면 캡션마다 "(소개용 예시 데이터)"를 붙였다.**
- **왜 protosim/Direct runtime 이 아닌가**: protosim Modbus 는 삼각파 램프만 만들어 추세가 톱니 모양이 되고, `cmd/simulator` 는 SIMULATED 플래그가 붙어 화면에 시뮬레이터 배지·배너가 뜬다. 그래서 같은 수집 계약(Standard Telemetry v1)의 리스너 경로를 썼다.
- **캡처**: agent-browser 전용 세션(`janus-present-shot` 사용자, `janus-present-admin` 관리자), 1440 CSS px · 2배율 · 라이트 테마. 로그인은 API 로 받은 세션 쿠키를 0600 파일로 넣었다(비밀번호를 명령줄에 쓰지 않음). 주소창·IP·포트·계정 아이디·토큰·`QA/test/sample/demo/temp/localhost` 문자열이 화면에 없음을 확인했다(표시되는 사용자 이름은 표시명 "현장 운전원"/"운영 관리자", 사이트는 "PLANT1 · 1공장").

## 8. Fact-check (Janus 저장소 기준, 2026-11-11, HEAD 6b5e51ee / 릴리스 0.31.0; 화면 추가분은 HEAD 738f9c06 / 릴리스 0.31.1)

내부 분류: IMPLEMENTED(소프트웨어 구현·시험 완료) / PARTIAL / PLANNED. 페이지에서는 IMPLEMENTED 만 "지원/제공/합니다"로 쓰고, PARTIAL·PLANNED 는 "확장 구조 / 연동 기반 / 확장할 수 있습니다"로 썼다. 주의: 모든 드라이버·장치 기능은 시뮬레이터 기준 검증이고 현장 장비 검증(Phase 8 HW)은 대기 중 — 그래서 "현장 검증 완료" 류 표현은 쓰지 않았다.

| 페이지 문구 | 분류 | 근거 |
|---|---|---|
| Modbus TCP / RTU | IMPLEMENTED | `backend/internal/acquisition/protocol/modbus` |
| RS-232 / RS-485, 사용자 정의 ASCII·바이너리 | IMPLEMENTED | `protocol/custom`, `transport/serial*` (Linux) |
| OPC UA | IMPLEMENTED | `protocol/opcua` |
| MQTT **구독** | IMPLEMENTED(구독만) | `protocol/mqtt` — 발행 없음, 그래서 "MQTT 구독" |
| HTTP API **주기 조회** | PARTIAL(폴링만) | `protocol/httpapi` — webhook/push 없음, 그래서 "주기 조회" |
| LoRa P2P · LoRaWAN, 셀룰러 모뎀(AT) | IMPLEMENTED | `protocol/lora`, `protocol/at`, `protocol/cellular` |
| RTSP · ONVIF · HTTP 카메라 | IMPLEMENTED | `internal/media/{rtsp,onvif,httpcam}` (ONVIF 검색은 지정 주소 방식) |
| GPS · GNSS | PARTIAL | NMEA 파서 구현, Protocol Studio 의 GPS 카드는 공간 패키지 활성 시에만 → "공간·지도 확장과 함께 구성" |
| OPC DA, BACnet, S7, EtherNet/IP, SNMP | 없음 | 페이지에 쓰지 않음 |
| Edge 수집·변환·태그 매핑 | IMPLEMENTED | `acquisition/{conversion,mapping,host}` |
| 저장 후 전송(끊겨도 보관 후 오래된 순 재전송) | IMPLEMENTED(소프트웨어) | `internal/edge/outbox`, TestDurableOutboxResendsOldestFirst |
| 설정 동기화, 현장 변경 제안 → Central 승인 | IMPLEMENTED | `internal/edge/configcache`, Edge 콘솔 작업 설정/Central 제안 |
| Edge 콘솔 진단(소스·네트워크·로그·패킷 수집·장비 읽기 시험·카메라 시험) | IMPLEMENTED | `features/edge-console/pages/*`, 진단 작업 PACKET_CAPTURE / SERIAL_MONITOR / MODBUS_SCAN |
| Protocol Studio 단계 마법사(연결·드라이버·파서·소스 포인트·변환·태그 매핑·테스트·검증·배포) | IMPLEMENTED | 실화면 11단계, `docs/code-index/protocol-studio.md` |
| Historian 원시값·현재값·추세·집계(평균·최소·최대·합계·개수)·CSV/Excel 내보내기 | IMPLEMENTED | `docs/code-index/historian.md` |
| 계산 태그 | IMPLEMENTED | Protocol Studio 계산 + 계산 서버 |
| 장기 보관 | PARTIAL(일 단위 보존, 압축/연속 집계 없음) | "장기 보관 최적화" 류 표현을 쓰지 않음 |
| UI Studio: 페이지 빌더·그리드/자유 배치·탭/컨테이너·뷰 템플릿·뷰 삽입/반복 뷰·데이터 연결·메뉴·테마·게시/버전, 위젯 60종 이상 | IMPLEMENTED | `contracts/ui/widget-catalog.v1.json` 67종, FINAL-REPORT-CAMERA-FGIH |
| 알람(상한·하한·대역·편차·변화율·조건식)·확인·보류·메모·이벤트·보고서, 메일·웹훅 알림 | IMPLEMENTED | P0-3 보고서, `core/notify` (SMS 없음 → 쓰지 않음) |
| 상태감시: 측정 포인트 판정·건전성·데이터 품질·파형·FFT·포락선·베어링 결함 주파수·보고서 | IMPLEMENTED(소프트웨어) | CM-REPORT, CM-B23-REPORT. 파형은 업로드 입력, 실시간 진동 센서 드라이버 없음 → "센서 실시간 파형" 표현 안 함 |
| 미디어: RTSP·ONVIF·H.264/H.265 수집·녹화·HTTPS/RTSPS·스냅샷·이벤트 녹화·미디어 위젯 | IMPLEMENTED | CAMERA-DEPLOYMENT-REPORT(0.27.0). H.265 브라우저 재생은 환경 의존 → "재생 지원"을 따로 강조하지 않음 |
| 공간·지도(지도·구역·이동 경로) | PARTIAL(시뮬레이터 E2E, 기본 미설치 패키지) | "확장 모듈"로 표현 |
| 배치도 화면(MAP_2D: 구역·설비·이동 장비 위치) | IMPLEMENTED(소프트웨어, 공간 패키지 설치 시) | 발표용 인스턴스에서 패키지 설치 → 지도·버전 승격·구역·엔티티(태그 바인딩 위치)를 API 로 만들고 USER 화면에서 캡처. 캡션은 "확장 모듈"로 유지, 실 GPS/UWB 위치 장치 검증은 없음 |
| 대시보드·다중 펜 추세·집계 카드·알람 현황·파형/FFT 화면 | IMPLEMENTED | 발표용 인스턴스(0.31.1 바이너리/웹)에서 실제 화면 캡처, 값은 소개용 예시 데이터(캡션 표기) |
| LiDAR · Radar · 로봇 · AGV · 사람 위치 | PARTIAL(계약·시뮬레이터·2D 위젯) | "연동 기반", "확장할 수 있습니다" |
| Physical AI 분석 | PLANNED | "향후 … 확장할 수 있습니다" |
| 감독 제어(태그 쓰기: 권한·미리보기·확인) | IMPLEMENTED(시뮬레이터) | P0-1 보고서. 실 PLC 쓰기 미검증 → "감독 제어 범위"로만 표현 |
| 로봇 자동 제어, 안전 인터록 | PLANNED / 제공 안 함 | 페이지에 "대신하지 않습니다"로 명시 |
| 모듈형 구성(패키지 단위 켜고 끔) | IMPLEMENTED | `core/packages`, 관리 화면 "패키지" |
| On-Premise, Edge + Central, 폐쇄망·오프라인 설치 패키지 | IMPLEMENTED | `docs/operations/install.md`, `edge-install.md` |
| 설치 환경: Central Ubuntu x86_64, Edge Linux amd64/arm64 | IMPLEMENTED | install.md §1, edge-install.md (Windows 미지원 → 쓰지 않음) |
| 보안: 역할 권한·사이트 범위·감사·관리자 2단계 인증 | IMPLEMENTED | auth/security 보고서 (OIDC 는 PARTIAL, LDAP PLANNED → 쓰지 않음) |
| HA(이중화) | PARTIAL | 페이지에 쓰지 않음 |

표기: "Janus System / 야누스 시스템 / Janus Central / Janus Edge / Protocol Studio / UI Studio / Historian". "자누스"는 홈페이지 소스·데이터·CMS 설정·업로드 PDF 텍스트·Janus 저장소 어디에도 없다(전수 검색 0건). 내부 기술명(Kafka, TimescaleDB, BadgerDB, 포트, IP, 마이그레이션 등)은 페이지에 없다.

## 9. 알려진 한계와 후속

- **실화면 범위(해결, 2026-11-11)**: 대시보드(히어로)·Historian 추세·상태감시 파형/FFT·알람·배치도를 발표용 로컬 인스턴스의 실제 화면으로 넣었다(7-1절). 값은 소개용 예시 데이터이고 캡션에 그렇게 적었다.
- 배치도 위젯은 구역·엔티티 이름 대신 코드(PUMP-ROOM, P-101 등)를 라벨로 그린다(제품 동작). 그래서 코드를 읽기 쉬운 영문 약어로 정했다.
- 미디어 섹션은 실 카메라가 없어 기존 Edge 콘솔 카메라 시험 화면을 그대로 둔다(라이브 영상 캡처 없음).
- 상태감시 진단 목록은 합성 파형이라 "전동체 결함"도 함께 판정됐다. 페이지에는 진단 목록이 아니라 파형·FFT·결함 주파수 표시만 잘라 넣었다.
- 카탈로그 PDF 없음 → 다운로드 버튼 숨김. 소개서가 준비되면 CMS "제품 카탈로그(PDF)"에 올리면 된다(자료실 항목도 함께 갱신).
- 표시 순서는 3(AssetPulse 다음). Janus 를 앞에 두려면 CMS 에서 순서만 바꾸면 된다.
- Taste 검사기 잔여(AssetPulse 와 동일, 사이트 공통): 헤더/푸터 구분선(hairline), 헤더 드롭다운의 reduced-motion 숨김, 모션 없음(사이트 전체가 모션을 쓰지 않음), 헤더 글자 대비/11px 글자, 실사진·영상 없음(이 제품의 그림은 실제 UI 화면), 카드형 블록 5줄 경고.

## 10. 배포 메모

- 배포 경로: GitHub `origin/main` 에 push → Netlify 가 `npm run build` 후 `dist` 를 게시(`netlify.toml`). 별도 수동 배포 절차·운영 서버 파일 복사 없음. CMS 데이터도 같은 저장소의 Markdown/JSON 이라 별도 DB 백업 대상이 없다.
- **이번 작업은 push 하지 않았다** — 운영 배포에는 push 가 필수 단계이므로 사용자 정책에 따라 로컬 커밋까지만 하고 중단했다. 배포하려면 사용자가 `git push origin main` 을 실행한다.
- 롤백: Netlify 의 이전 배포 "Publish deploy" 또는 `git revert <커밋들>` 후 push.
- 배포 후 확인: `/products/`(Janus 카드 로고), `/products/janus-system/`(이미지 10개·콘솔 오류 0), `/products/data-integration-sw/`, `/`(홈 제품 라인업), `/contact/`, 모바일 390px.
- 로컬 확인: `npm run build` 후 `dist/` 를 정적 서버로 연다(예: `python3 -m http.server 8093 --bind 127.0.0.1 --directory dist`). Eleventy 는 `dist` 를 비우지 않으므로 삭제된 페이지를 확인할 때는 `rm -rf dist` 후 빌드한다.

## 11. 파일

| 파일 | 역할 |
|---|---|
| `src/_data/productTemplates.json` | template 값 → 전용 템플릿 매핑 |
| `src/_includes/product.njk` | 레지스트리로 전용/일반 템플릿 선택 |
| `src/_includes/product-janus.njk` | Janus 전용 템플릿 |
| `src/_includes/product-card-media.njk` | 제품 카드 이미지 영역(목록·홈 공통, cover/contain) |
| `src/_data/janus.json` | 전용 템플릿 고정 문구·이미지 alt/캡션/크기 |
| `src/products/janus-system.md` | Janus CMS 제품 문서 |
| `public/images/janus/*.webp` | 실제 Janus 화면(12장 + 800w 변형) |
| `public/images/uploads/janus-system-logo.webp` | 공식 로고(대표 이미지) |
| `admin/config.yml` | 템플릿 선택지 `janus`, `image_fit` 필드 |
| `docs/PRODUCT-CMS-BLOCK-MODEL-PROPOSAL.md` | 블록형 제품 콘텐츠 제안(이번 범위 아님) |
