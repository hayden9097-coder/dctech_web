# AssetPulse 제품 상세페이지 (전용 템플릿)

AssetPulse 는 소프트웨어 플랫폼이라 일반 제품 상세(텍스트 + 오른쪽 박스)로는 기능과 화면을 보여주기 어렵다. 그래서 **AssetPulse 제품만** 화면 중심의 전용 상세 템플릿을 쓴다. 디지털 콘텐츠 관리자(Decap CMS)의 기존 필드와 일반 제품 페이지는 그대로다.

## 1. 현재 CMS 구조 (조사 결과)

| 항목 | 내용 |
|---|---|
| 콘텐츠 파일 | `src/products/*.md` (Eleventy 컬렉션 `products`, 제품 목록·홈 카드·상세 자동 생성) |
| CMS 필드 | 제품명(`title`) · 제품 분류(`category`) · 표시 순서(`order`) · 한줄 요약(`summary`) · 대표 이미지(`image`) · 주요 특징(`features`, 문자열 목록) · 제품 사양(`specs`, 항목명/내용 목록) · 제품 카탈로그 PDF(`brochure`) · 상세 설명(`body`, Markdown) + 숨김 `layout: product.njk` |
| 렌더러 | `src/_includes/product.njk` (일반 템플릿) → `base.njk`(헤더·푸터). Tailwind(`tailwind.config.js`, 네이비/테크블루, Pretendard) |
| AssetPulse 문서 | 파일 이름이 `data-integration-sw.md` 로 남아 있다(옛 제품 이름). 그래서 **슬러그로 식별하지 않는다**(주소 `/products/data-integration-sw/` 도 그대로 유지) |

## 2. 전용 템플릿을 고르는 방법 (Trigger)

제품 문서의 **`template: assetpulse`** 값이다.

- `src/_includes/product.njk` 가 `template == "assetpulse"` 이면 `product-assetpulse.njk` 를 포함하고, 아니면 기존 일반 템플릿을 **그대로** 쓴다. 다른 제품은 영향이 없다(PumpGuard 페이지는 공백을 제외하고 바이트 단위로 동일함을 빌드 결과 대조로 확인).
- CMS 에는 선택 필드 **"상세 페이지 템플릿"**(기본 템플릿 / AssetPulse 전용 템플릿)을 추가했다(`admin/config.yml`). 비어 있거나 `default` 이면 일반 템플릿. 필수 아님.
- DB ID·슬러그 같은 하드코딩은 없다.

## 3. CMS 필드가 전용 페이지에 반영되는 곳

| CMS 필드 | 전용 페이지에서 | 
|---|---|
| 제품명 | 히어로 이미지 캡션, 제품 사양 표 첫 행, 브라우저 제목·SNS 미리보기 |
| 제품 분류 | 제품 사양 표 둘째 행 |
| 한줄 요약 | "상세 제품 소개" 섹션 첫 문장, 메타 설명(검색·공유) |
| 대표 이미지 | 히어로 로고 마크(현재 AssetPulse 로고) |
| 주요 특징 | "주요 특징" 카드(아래 4절) |
| 제품 사양 | 제품 사양 표(깔끔한 `<table>`) |
| 제품 카탈로그 PDF | 히어로 "제품 소개서 다운로드" · 하단 "제품 카탈로그 다운로드". 비어 있으면 자료실(`/downloads/`)로 연결 |
| 상세 설명 | "상세 제품 소개" 섹션(전체 레이아웃이 아니라 보조 콘텐츠) |

검증: 임시 복사본에서 모든 CMS 필드를 바꿔 빌드한 뒤 8개 항목(제품명·한줄 요약·대표 이미지·주요 특징·제품 사양·PDF·상세 설명·`<title>`)이 모두 반영됨을 확인했다.

## 4. "주요 특징" 렌더링 (DB 구조 변경 없음)

CMS 데이터는 문자열 목록 그대로 둔다. 렌더링 시 `featureItems` 필터(`eleventy.config.js`)가 다음을 한다.

- **괄호가 닫히지 않은 항목은 다음 항목과 합친다.** (현재 데이터에서 "…(속도/가속도 스펙트럼" 과 "RMS·Peak·Kurtosis 등 … 자동 산출)" 가 두 줄로 갈라져 있었다 → 한 카드로 정리)
- ` — ` / ` – ` / `: ` 가 있으면 앞은 제목, 뒤는 설명으로 나눠 카드에 표시한다. 없으면 문장 전체가 제목이다.
- 항목 수가 달라도 2열 카드로 흐른다.

향후 CMS 개선: 특징을 `제목` / `설명` 두 칸 목록으로 바꾸면 구분자 규칙이 필요 없다(7절).

## 5. 페이지 흐름과 파일

Hero(로고·큰 제목·대시보드) → 핵심 가치(흐름 + 6대 기능) → 통합 자산 관리 → 센서 연결 → 실시간 상태감시 → 측정·분석(Waveform/FFT/이력) → 알람·정비 → 시스템 구조 + 도입 형태 → 제품 사양 → 주요 특징 → 상세 제품 소개 → 카탈로그 다운로드·문의.

| 파일 | 역할 |
|---|---|
| `src/_includes/product-assetpulse.njk` | 전용 템플릿 |
| `src/_data/assetpulse.json` | 고정 문구(히어로·6대 기능·섹션 설명·구조·도입 형태)와 화면 이미지 설명(alt) — 코드 없이 수정 가능 |
| `public/images/assetpulse/*.webp` | 실제 AssetPulse 화면(카탈로그용 데모 현장 "제1생산공장") |
| `public/images/uploads/assetpulse-catalog.pdf` | 제품 소개서(7쪽, CMS 의 PDF 필드에 지정) |
| `design/assetpulse-catalog/catalog.html` | 소개서 원본(브라우저로 열어 PDF 로 저장: `agent-browser pdf`) |
| `design/assetpulse-concepts/` | 시안 5종 생성기·화면(참고용, 사이트에 배포되지 않음) |

화면 이미지는 mock 이 아니라 **실제 AssetPulse UI** 이다. 촬영한 데이터셋 구성과 재현 방법은 AssetPulse 저장소의 `docs/catalog/CATALOG_DEMO_DATASET.md` 와 `CATALOG_SCREENSHOT_CHECKLIST.md` 에 있다. 내부 주소(83/84 등)와 개발용 문자열(`test`·`demo`·`sample` 등)은 화면에도 문구에도 없다.

## 6. 디자인 시안 비교 (Taste)

실제 홈페이지 header/footer 를 그대로 쓴 5개 시안(`design/assetpulse-concepts/screens/*.jpg`, 모바일 포함)을 같은 내용으로 만들어 비교했다(5점 만점, 육안 평가).

| 기준 | A SaaS Product | **B Industrial Solution** | C Product Story | D Technical Platform | E Minimal Enterprise |
|---|---|---|---|---|---|
| 브랜드 적합성 | 3 | **5** | 3 | 4 | 3 |
| 산업 제품 느낌 | 3 | **5** | 3 | 4 | 2 |
| AssetPulse 기능 전달 | 4 | **5** | 5 | 4 | 4 |
| 스크린샷 활용성 | 5 | **4** | 4 | 2 | 5 |
| 모바일 반응형(가로 넘침 0 은 공통) | 4 | **4** | 3(가장 긺) | 4 | 4 |
| 기존 홈페이지 일관성 | 3 | **5** | 3 | 3 | 3 |
| 카탈로그 연계성 | 4 | **5** | 4 | 3 | 3 |
| 합계 | 26 | **33** | 25 | 24 | 24 |

- A: 흰 히어로 + 큰 대시보드. 깔끔하나 기존 제품 페이지의 네이비 히어로와 달라 보인다.
- **B(선정)**: 네이비 히어로 + 실제 대시보드 → 흰/네이비 띠 교차. 기존 제품 히어로 계열이라 가장 일관되고, 첫 화면부터 운영 중인 UI 가 보인다.
- C: 챕터형. 흐름은 좋으나 페이지가 가장 길고 화면이 상대적으로 작아진다.
- D: 구조도 우선. 기술 전달은 좋지만 화면 비중이 낮아 카탈로그와 연결이 약하다.
- E: 미니멀. 화면은 크게 쓰지만 산업용 제품 느낌이 약하다.

구현은 B 를 기반으로 하되, 사용자 요청(과도한 그라데이션 금지)과 Taste 의견에 따라 히어로의 격자·그라데이션을 빼고 **단색 네이비**로 했으며, 히어로 제목을 크게(56~60px) 키우고 대시보드를 전폭으로 배치했다.

## 7. 향후 CMS 확장 제안 (이번 범위 아님)

지금은 "전용 템플릿 + 고정 문구 JSON" 이다. 마케팅 담당자가 구조까지 직접 바꾸려면 블록 기반 콘텐츠 모델이 필요하다. 제안:

```yaml
blocks:            # Decap list widget (types)
  - type: hero            # 제목, 부제, 이미지, 버튼 2개
  - type: feature_grid    # 항목: 제목, 설명 (n개)
  - type: image_text      # 이미지, 제목, 본문, 불릿, 좌/우, 배경색(흰/연회색/네이비)
  - type: screenshot_set  # 이미지 목록: 파일, alt, 캡션, 배치(1·2·3열)
  - type: flow            # 단계 목록
  - type: architecture    # 노드 목록(제목, 설명)
  - type: spec_table      # 기존 specs 재사용
  - type: cta             # 제목, 본문, 버튼
```

- 기존 `features` 도 `{제목, 설명}` 목록으로 옮기면 4절의 구분자 규칙이 필요 없다.
- 이미지는 CMS 업로드 + alt/캡션 필수로 두면 접근성을 지킬 수 있다.
- 일반 제품은 `blocks` 가 없으면 기존 템플릿을 쓴다(이번 방식과 같은 호환 규칙).

## 8. 검증 요약

| 항목 | 결과 |
|---|---|
| 반응형 1920 / 1600 / 1366 / 태블릿 768 / 모바일 390 | 가로 넘침 0, 이미지 12개 모두 로드, 제목 2줄 이하 (`design/assetpulse-product-page/screens/`) |
| 일반 제품 회귀 | PumpGuard 상세는 공백 제외 동일, 제품 목록·홈·회사소개 HTML 동일 |
| CMS 수정 반영 | 필드 8개 모두 반영 |
| PDF | `/images/uploads/assetpulse-catalog.pdf` 200, `application/pdf`, 히어로·하단 두 버튼에 `download` 지정 |
| 브라우저(agent-browser) | 제품 목록 → AssetPulse 상세 이동, h1 1개, 문의 링크, 섹션 순서, 이미지 확대 링크(새 탭) 구성 확인 |
| Taste 검사기 | 3 FAIL · 6 WARN — 아래 |

Taste 검사기 잔여 항목(모두 사이트 공통 요소이거나 의도한 선택):

- FAIL `hairline`, `reduced-hidden`: 기존 헤더/푸터의 구분선과 드롭다운 메뉴 — 이 템플릿의 요소가 아니다.
- FAIL `still-page`(움직이는 요소 0개): 기존 사이트가 모션을 쓰지 않아 일관성을 위해 넣지 않았다.
- WARN `card-rows`: 6대 기능 카드는 요청 사항(카드 또는 아이콘 형태)이다.
- WARN `contrast`: 남은 항목은 기존 헤더 메뉴. 이 페이지의 파란 버튼은 대비 5:1 이상으로 어둡게 했다.
- WARN `no-real-pictures`/`no-footage`: 이 제품의 그림은 실제 UI 화면이다. 현장 사진·영상은 아직 확보한 것이 없다.

## 9. 알려진 한계와 권장 후속

- **CMS 사양 문구**: "클라우드 운영 DB", "클라우드 대시보드(웹 기반) 하이브리드" 등 기존 문구가 그대로 표에 나온다. 전용 페이지의 "도입 형태"(On-Premise)와 어긋나므로 사양 표를 CMS 에서 정리하길 권한다(예: 제품 형태 / 구성 / 주요 대상 / 수집 방식 / 분석 / 운영).
- **BLE**: "Bluetooth(BLE)" 는 게이트웨이가 센서에 연결해 수집하는 방식으로만 적었다(상시 무인 주기 수집은 쓰지 않음).
- **오프라인 설치**: "설치·업데이트용 오프라인 패키지"는 서버/게이트웨이 1.0.0-rc1 설치 패키지 기준이다(릴리스 후보).
- 현장 사진·영상이 생기면 히어로에 함께 쓸 수 있다.
- 화면 이미지는 데모 현장의 어느 시점 캡처이다. 제품 UI 가 바뀌면 카탈로그 체크리스트 순서로 다시 촬영한다.
- 개발 시 로컬 확인: `npm run build` 후 `dist/` 를 정적 서버로 열면 된다(`npm start` 도 가능).
