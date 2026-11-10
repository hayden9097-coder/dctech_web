#!/usr/bin/env python3
"""AssetPulse 제품 상세페이지 시안 5종 생성기. 실제 홈페이지의 header/footer 를 빌드 결과(dist)에서 그대로 가져온다.
실행: (저장소 루트에서) npm run build && python3 design/assetpulse-concepts/build_concepts.py
결과: dist/concepts/{a..e}.html + dist/css/concepts.css (dist 는 git 제외)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from content import *

src = open(os.path.join(ROOT, "dist/products/data-integration-sw/index.html"), encoding="utf-8").read()
head_end = src.index("<header")
HEAD = src[:head_end].replace('/css/main.css', '/css/concepts.css')
HEADER = src[head_end: src.index("</header>") + 9]
FOOT = src[src.index("<footer"): src.index("</footer>") + 9]
SCRIPT = src[src.index("</footer>") + 9:]

def shot(name, alt, cls="", w=None):
    return f'<img src="{IMG}{name}.webp" alt="{alt}" class="block w-full h-auto rounded-xl border border-slate-200 {cls}" loading="lazy">'

def feats(cols="md:grid-cols-3", tone="plain"):
    items = "".join(f'<div class="{ "bg-slate-50" if tone=="plain" else "bg-white border border-slate-200"} rounded-xl p-6"><h3 class="text-lg font-bold text-navy-900">{t}</h3><p class="mt-2 text-slate-600 leading-relaxed">{d}</p></div>' for t, d in FEATURES)
    return f'<div class="grid gap-4 {cols}">{items}</div>'

def ctas(dark=False):
    b2 = "border-white/40 text-white hover:bg-white/10" if dark else "border-navy-900/20 text-navy-900 hover:bg-slate-50"
    return f'<div class="mt-8 flex flex-wrap gap-3"><a href="/downloads/" class="inline-flex items-center bg-techblue-500 hover:bg-techblue-400 text-white font-bold px-6 py-3.5 rounded-lg">제품 소개서 다운로드</a><a href="/contact/" class="inline-flex items-center border-2 {b2} font-bold px-6 py-3 rounded-lg">문의하기</a></div>'

def row(h, p, img, flip=False, bg="bg-white", extra=""):
    t = f'<div class="lg:col-span-4 flex flex-col justify-center"><h2 class="text-2xl md:text-3xl font-extrabold text-navy-900 leading-snug">{h}</h2><p class="mt-4 text-slate-600 leading-relaxed">{p}</p>{extra}</div>'
    i = f'<div class="lg:col-span-8">{img}</div>'
    return f'<section class="{bg} py-16 md:py-24"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-10 items-center">{i + t if flip else t + i}</div></section>'

def flow(dark=False):
    c = "bg-white/10 text-white" if dark else "bg-techblue-50 text-navy-900"
    items = '<span class="text-techblue-400 hidden md:inline">→</span>'.join(f'<span class="{c} rounded-lg px-4 py-3 font-semibold text-sm text-center">{x}</span>' for x in FLOW)
    return f'<div class="flex flex-wrap md:flex-nowrap items-center justify-center gap-3">{items}</div>'

def arch(horizontal=True):
    arrow = '<div class="self-center text-techblue-500 text-xl hidden md:block">→</div>'
    cells = [f'<div class="bg-white border border-slate-200 rounded-xl p-5 flex-1 min-w-[180px]"><p class="font-bold text-navy-900">{a}</p><p class="mt-1 text-sm text-slate-500">{b}</p></div>' for a, b in ARCH]
    return '<div class="flex flex-col md:flex-row gap-3 md:items-stretch">' + arrow.join(cells) + '</div>'

def specs():
    r = "".join(f'<tr class="border-t border-slate-200"><th class="py-3.5 pr-6 text-left font-medium text-slate-500 w-40 align-top">{a}</th><td class="py-3.5 text-navy-900 font-medium">{b}</td></tr>' for a, b in SPECS)
    return f'<table class="w-full text-[15px]"><tbody>{r}</tbody></table>'

def deploy():
    return '<div class="grid md:grid-cols-3 gap-4">' + "".join(f'<div class="bg-slate-50 rounded-xl p-6"><h3 class="font-bold text-navy-900 text-lg">{a}</h3><p class="mt-2 text-slate-600">{b}</p></div>' for a, b in DEPLOY) + "</div>"

def sect(h, inner, bg="bg-white", sub=None):
    s = f'<p class="mt-3 text-slate-600 max-w-2xl">{sub}</p>' if sub else ""
    return f'<section class="{bg} py-16 md:py-24"><div class="max-w-7xl mx-auto px-6 lg:px-8"><h2 class="text-2xl md:text-3xl font-extrabold text-navy-900 mb-2">{h}</h2>{s}<div class="mt-10">{inner}</div></div></section>'

def cta_band():
    return f'<section class="bg-navy-900 py-16"><div class="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col md:flex-row md:items-center md:justify-between gap-6"><div><h2 class="text-2xl md:text-3xl font-extrabold text-white">우리 현장에 맞는 구성을 안내해 드립니다</h2><p class="mt-2 text-slate-300">설비 환경과 센서 종류에 맞춰 도입 방법을 상담해 드립니다.</p></div>{ctas(True).replace("mt-8","")}</div></section>'

def page(name, body):
    out = os.path.join(ROOT, "dist/concepts"); os.makedirs(out, exist_ok=True)
    html = HEAD.replace("<title>", "<title>[시안 %s] " % name.upper(), 1) + HEADER + '\n<main id="main" class="pt-16">' + body + "</main>\n" + FOOT + SCRIPT
    open(os.path.join(out, name + ".html"), "w", encoding="utf-8").write(html)

# A. SaaS Product — 흰 히어로 + 큰 대시보드 화면이 히어로 아래로 걸친다
page("a", f'''<section class="bg-white pt-16 md:pt-24"><div class="max-w-7xl mx-auto px-6 lg:px-8 text-center">
<img src="/images/uploads/chatgpt-image-2026년-6월-20일-오전-07_53_27.png" alt="AssetPulse" class="mx-auto h-16 w-16 object-contain">
<h1 class="mt-6 text-3xl md:text-5xl font-extrabold text-navy-900 leading-tight">{HERO_H}</h1>
<p class="mt-5 text-slate-600 max-w-3xl mx-auto leading-relaxed">{HERO_P}</p>{ctas().replace("flex-wrap","flex-wrap justify-center")}
</div><div class="mt-14 bg-slate-50 pt-10"><div class="max-w-6xl mx-auto px-6 lg:px-8">{shot("dashboard","AssetPulse 대시보드","-mb-px rounded-b-none")}</div></div></section>
{sect("핵심 기능", feats(), "bg-white")}
{row(ASSET_H, ASSET_P, shot("asset-tree","자산 트리"), bg="bg-slate-50")}
{row(ANA_H, ANA_P, shot("waveform","파형"), flip=True)}
{row(ALM_H, ALM_P, shot("alarms","알람"), bg="bg-slate-50")}
{sect("시스템 구성", arch(), "bg-white")}
{sect("제품 사양", specs(), "bg-slate-50")}
{cta_band()}''')

# B. Industrial Solution — 네이비 히어로(기존 제품 히어로 계열) + 한 화면 가득 UI, 네이비/흰 띠 교차
page("b", f'''<section class="page-hero grid-overlay pt-16 md:pt-24 pb-16"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-10 items-center">
<div class="lg:col-span-5"><h1 class="text-3xl md:text-5xl font-extrabold text-white leading-tight">{HERO_H}</h1><p class="mt-5 text-slate-300 leading-relaxed">{HERO_P}</p>{ctas(True)}</div>
<div class="lg:col-span-7">{shot("dashboard","AssetPulse 대시보드","border-white/20")}</div></div></section>
<section class="bg-white py-14"><div class="max-w-7xl mx-auto px-6 lg:px-8"><p class="text-center text-slate-500 mb-6">펌프 · 모터 · 팬 · 압축기 등 회전설비의 상태를 현장에서 알람·정비까지 연결합니다</p>{flow()}</div></section>
{sect("핵심 기능", feats("md:grid-cols-3","card"), "bg-slate-50")}
<section class="bg-navy-900 py-16 md:py-24"><div class="max-w-7xl mx-auto px-6 lg:px-8 grid lg:grid-cols-12 gap-10 items-center"><div class="lg:col-span-5"><h2 class="text-2xl md:text-3xl font-extrabold text-white leading-snug">{SENSOR_H}</h2><p class="mt-4 text-slate-300 leading-relaxed">{SENSOR_P}</p></div><div class="lg:col-span-7">{shot("sensors","디바이스와 센서","border-white/20")}</div></div></section>
{row(ASSET_H, ASSET_P, shot("asset-tree","자산 트리"))}
{row(ANA_H, ANA_P, shot("fft","FFT"), flip=True, bg="bg-slate-50")}
{sect("도입 형태", deploy(), "bg-white")}
{sect("제품 사양", specs(), "bg-slate-50")}
{cta_band()}''')

# C. Product Story — 챕터 흐름: 자산 → 센서 → 분석 → 정비. 각 챕터가 한 화면 전체를 쓴다
def chapter(n, h, p, img, bg):
    return f'<section class="{bg} py-16 md:py-28"><div class="max-w-7xl mx-auto px-6 lg:px-8"><div class="grid lg:grid-cols-12 gap-8 items-end"><div class="lg:col-span-7"><h2 class="text-3xl md:text-4xl font-extrabold text-navy-900 leading-snug">{h}</h2></div><div class="lg:col-span-5"><p class="text-slate-600 leading-relaxed">{p}</p></div></div><div class="mt-10">{img}</div></div></section>'
page("c", f'''<section class="bg-white pt-16 md:pt-24 pb-12"><div class="max-w-7xl mx-auto px-6 lg:px-8"><div class="grid lg:grid-cols-12 gap-8 items-end"><div class="lg:col-span-8"><h1 class="text-4xl md:text-6xl font-extrabold text-navy-900 leading-tight">{HERO_H}</h1></div><div class="lg:col-span-4"><p class="text-slate-600 leading-relaxed">{HERO_P}</p>{ctas()}</div></div>
<div class="mt-12">{flow()}</div></div></section>
{chapter(1, ASSET_H, ASSET_P, shot("asset-tree","자산 트리"), "bg-slate-50")}
{chapter(2, SENSOR_H, SENSOR_P, shot("sensors","센서 목록"), "bg-white")}
{chapter(3, ANA_H, ANA_P, '<div class="grid md:grid-cols-2 gap-4">'+shot("waveform","파형")+shot("fft","FFT")+'</div>', "bg-slate-50")}
{chapter(4, ALM_H, ALM_P, '<div class="grid md:grid-cols-2 gap-4">'+shot("alarms","알람")+shot("tasks","작업")+'</div>', "bg-white")}
{sect("핵심 기능", feats(), "bg-slate-50")}
{sect("제품 사양", specs(), "bg-white")}
{cta_band()}''')

# D. Technical Platform — 구조도 먼저, 기능 표, 화면은 탭형 갤러리처럼 2×2
page("d", f'''<section class="bg-slate-50 pt-16 md:pt-24 pb-16"><div class="max-w-7xl mx-auto px-6 lg:px-8"><div class="grid lg:grid-cols-12 gap-10 items-center"><div class="lg:col-span-6"><h1 class="text-3xl md:text-5xl font-extrabold text-navy-900 leading-tight">{HERO_H}</h1><p class="mt-5 text-slate-600 leading-relaxed">{HERO_P}</p>{ctas()}</div><div class="lg:col-span-6">{shot("network","네트워크 상태")}</div></div></div></section>
{sect("시스템 구조", arch() + '<div class="mt-8">' + deploy() + '</div>', "bg-white")}
{sect("기능 구성", '<div class="overflow-x-auto"><table class="w-full text-[15px]"><tbody>' + "".join(f'<tr class="border-t border-slate-200"><th class="py-4 pr-6 text-left text-navy-900 w-56 align-top">{a}</th><td class="py-4 text-slate-600">{b}</td></tr>' for a,b in FEATURES) + '</tbody></table></div>', "bg-slate-50")}
{sect("화면으로 보는 플랫폼", '<div class="grid md:grid-cols-2 gap-6">'+shot("dashboard","대시보드")+shot("asset-tree","자산 트리")+shot("fft","FFT")+shot("tasks","작업 일정")+'</div>', "bg-white")}
{sect("제품 사양", specs(), "bg-slate-50")}
{cta_band()}''')

# E. Minimal Enterprise — 흰 바탕, 큰 글자, 섹션마다 화면 하나
page("e", f'''<section class="bg-white pt-20 md:pt-32 pb-16"><div class="max-w-7xl mx-auto px-6 lg:px-8"><h1 class="text-4xl md:text-7xl font-extrabold text-navy-900 leading-[1.1] max-w-4xl">{HERO_H}</h1><p class="mt-8 text-lg text-slate-600 max-w-2xl leading-relaxed">{HERO_P}</p>{ctas()}</div></section>
<section class="bg-white pb-20"><div class="max-w-7xl mx-auto px-6 lg:px-8">{shot("dashboard","AssetPulse 대시보드")}</div></section>
{row(ASSET_H, ASSET_P, shot("asset-tree","자산 트리"), bg="bg-slate-50")}
{row(SENSOR_H, SENSOR_P, shot("sensors","센서"), flip=True)}
{row(ANA_H, ANA_P, shot("trend","추세"), bg="bg-slate-50")}
{row(ALM_H, ALM_P, shot("alarms","알람"), flip=True)}
{sect("제품 사양", specs(), "bg-slate-50")}
{cta_band()}''')

# 스타일 빌드(시안 전용 CSS: 시안 HTML 과 사이트 소스를 함께 스캔)
cfg = os.path.join(HERE, "tailwind.concepts.config.js")
subprocess.run(["npx", "tailwindcss", "-c", cfg, "-i", os.path.join(ROOT, "src/styles/main.css"), "-o", os.path.join(ROOT, "dist/css/concepts.css"), "--minify"], cwd=ROOT, check=True, stderr=subprocess.DEVNULL)
print("ok")
