---
layout: product.njk
title: Janus System 산업 데이터 통합 플랫폼
category: 데이터 통합 · 관제 소프트웨어
template: janus
order: 3
summary: 산업 현장의 장비·센서·카메라 데이터를 Edge와 Central에서 수집·저장하고, Protocol Studio와 UI Studio로 연결과 관제 화면을 직접 구성하는 산업 데이터 통합 플랫폼
image: /images/uploads/janus-system-logo.webp
image_fit: contain
brochure: ""
features:
  - 다양한 산업 프로토콜 수집 — Modbus, OPC UA, MQTT, 직렬 통신, HTTP API, LoRa, 셀룰러 모뎀 데이터를 하나의 수집 흐름으로 받습니다
  - Edge 현장 수집 — 현장 Edge가 수집·변환·태그 매핑을 맡고, Central과 연결이 끊겨도 데이터를 보관했다가 다시 보냅니다
  - 산업용 Historian — 원시값·현재값·추세·집계를 같은 태그 기준으로 저장하고 조회합니다
  - Protocol Studio — 연결, 파서, 변환, 태그 매핑, 시험, 배포를 단계별 마법사로 구성합니다
  - UI Studio — 60종 이상의 위젯으로 관제 화면을 만들고 버전으로 관리해 게시합니다
  - 알람 · 이벤트 — 상한·하한·대역·편차·변화율·조건식 알람과 확인·이력·알림을 관리합니다
  - 상태감시 · 미디어 — 진동 파형·FFT 분석과 카메라 스냅샷·녹화를 같은 플랫폼에서 다룹니다
  - 공간 · Physical AI 확장 — 위치·지도·로봇 데이터를 연결할 수 있는 확장 구조를 갖추고 있습니다
specs:
  - label: 제품 형태
    value: 산업 데이터 통합 플랫폼(소프트웨어)
  - label: 구성
    value: Janus Central(서버) · Janus Edge(현장) · 웹 브라우저
  - label: 운영 형태
    value: On-Premise 설치, 폐쇄망 운영 가능(오프라인 설치 패키지)
  - label: 수집
    value: Modbus TCP/RTU · OPC UA · MQTT · RS-232/485 직렬 · HTTP API · LoRa · 셀룰러 모뎀 · 카메라(RTSP/ONVIF)
  - label: 저장
    value: Historian — 원시값 · 현재값 · 집계 · 계산 태그 · CSV/Excel 내보내기
  - label: 시각화
    value: 웹 관제 화면 · UI Studio(위젯 60종 이상, 게시·버전 관리)
  - label: 현장 도구
    value: Protocol Studio · Edge 콘솔(장비 시험 · 카메라 시험 · 진단)
  - label: 알람
    value: 상한·하한·대역·편차·변화율·조건식 알람, 확인·보류, 이벤트 기록, 메일·웹훅 알림
  - label: 확장
    value: 상태감시 · 미디어 · 보고서 · 공간/지도(패키지 단위), Physical AI 연동 기반
  - label: 보안
    value: 역할 기반 권한 · 사이트 범위 · 감사 기록 · 관리자 2단계 인증
  - label: 설치 환경
    value: Central — Ubuntu Linux(x86_64), Edge — Linux(amd64 · arm64)
---
## 제품 개요

Janus System(야누스 시스템)은 공장과 시험 현장의 PLC, 계측기, 센서, 무선 모듈, 카메라 데이터를 한 곳으로 모으는 산업 데이터 통합 플랫폼입니다. 현장에 둔 Janus Edge 또는 서버의 직접 수집으로 데이터를 받아 Historian에 저장하고, 관리자는 Protocol Studio로 수집을, UI Studio로 관제 화면을 직접 구성합니다.

## 이런 현장에 적합합니다

- 장비마다 통신 방식이 달라 데이터를 한 화면에서 보기 어려운 공장
- 시험·연구 장비의 측정값을 기간별로 저장하고 다시 꺼내 봐야 하는 현장
- 인터넷 연결 없이 내부망에서 운영해야 하는 산업 현장
- 통신이 불안정한 원격 설비의 데이터를 빠짐없이 모아야 하는 현장
- 설비 상태감시와 카메라 영상을 같은 관제 화면에서 보고 싶은 조직

## 도입 효과

장비별로 흩어져 있던 데이터가 같은 태그 체계로 저장되어, 현재 상태와 과거 추세를 같은 화면에서 확인할 수 있습니다. 수집 구성과 관제 화면을 관리자가 직접 바꿀 수 있어, 장비가 늘거나 공정이 바뀌어도 별도 개발 없이 화면과 수집 범위를 넓혀 갈 수 있습니다.
