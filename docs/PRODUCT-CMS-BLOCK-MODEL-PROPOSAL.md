# 제품 상세 블록형 콘텐츠 모델 제안 (제안만 — 이번 배포 범위 아님)

현재 전용 상세 템플릿(AssetPulse, Janus)은 "CMS 기본 필드 + 템플릿 + 고정 문구 JSON(`src/_data/<제품>.json`)" 구조다. 섹션 구성·순서·고정 문구는 개발자가 바꾼다. 마케팅 담당자가 CMS 에서 섹션까지 다루려면 블록형 모델이 필요하다.

## 제안 모델 (Decap `list` + `types`)

```yaml
- label: "페이지 블록"
  name: "blocks"
  widget: "list"
  required: false
  types:
    - { name: hero,        fields: [제목, 소개 문장, 이미지(+alt), 버튼 2개(문구·주소)] }
    - { name: feature_grid, fields: [제목, 항목 목록(제목·설명)] }
    - { name: image_text,  fields: [제목, 본문, 불릿, 이미지(+alt·캡션), 이미지 위치(좌/우), 배경(흰/연회색/네이비)] }
    - { name: screenshot_set, fields: [제목, 이미지 목록(파일·alt·캡션), 배치(1·2·3열)] }
    - { name: flow,        fields: [제목, 단계 목록(제목·설명)] }
    - { name: architecture, fields: [제목, 층 목록(키·제목·항목)] }   # SVG 는 템플릿이 그림
    - { name: spec_table,  fields: [제목] }                         # 기존 specs 재사용
    - { name: cta,         fields: [제목, 본문, 버튼] }
```

## 호환 규칙

- `blocks` 가 없으면 지금처럼 `template`(레지스트리) → 전용 템플릿, 그것도 없으면 일반 템플릿.
- `blocks` 가 있으면 블록 렌더러(`product-blocks.njk`)가 블록 순서대로 그린다. 기존 `features`·`specs`·`brochure`·`body` 는 블록 안에서 그대로 참조.
- 이미지 블록은 alt 를 필수로 둔다(접근성). 업로드 경로는 기존 `media_folder`.
- `features` 를 `{제목, 설명}` 두 칸 목록으로 바꾸면 `featureItems` 의 구분자(" — ") 규칙이 필요 없어진다.

## 이행 순서(안)

1. 블록 렌더러와 블록 4종(hero, image_text, screenshot_set, cta)만 먼저 → 새 제품 1개로 시험.
2. `src/_data/janus.json`·`assetpulse.json` 의 문구를 블록으로 옮기는 변환 스크립트(출력 HTML 비교로 회귀 확인).
3. 전용 템플릿은 블록 이행이 끝난 뒤 정리.

이번 Janus 작업에는 적용하지 않았다.
