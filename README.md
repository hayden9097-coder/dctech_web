# 디씨테크(DCTech) 홈페이지

Eleventy 정적 사이트 + Decap CMS 기반. 코드를 몰라도 관리자 페이지에서 콘텐츠를 수정할 수 있습니다.

## 페이지 구조

| 메뉴 | 주소 | 콘텐츠 파일 |
|---|---|---|
| 홈 | `/` | `src/_data/home.json` |
| 회사소개 | `/about/` | `src/_data/about.json` |
| 핵심 솔루션 | `/solutions/` | `src/_data/solutions.json` |
| 도입 사례 | `/cases/` | `src/cases/*.md` (사례별 1파일) |
| 문의 | `/contact/` | `src/_data/contact.json` |
| 공통(로고·주소·연락처) | 전체 | `src/_data/site.json` |

## 로컬에서 확인하기

```bash
npm install
npm start
```

http://localhost:8080 에서 확인할 수 있습니다.

## 배포 및 관리자 페이지 활성화

관리자 페이지(`/admin/`)는 배포 후에 동작합니다. 다음 순서로 1회 설정이 필요합니다.

1. 이 폴더를 GitHub 저장소에 올립니다 (브랜치명 `main`).
2. [Netlify](https://app.netlify.com)에서 해당 저장소를 연결해 배포합니다.
   빌드 설정은 `netlify.toml`에 이미 정의되어 있습니다.
3. Netlify 사이트 설정에서 **Identity** 기능을 켭니다.
4. Identity > Services에서 **Git Gateway**를 켭니다.
5. Identity > Invite users로 편집할 담당자의 이메일을 초대합니다.

설정이 끝나면 `https://사이트주소/admin/` 으로 접속해 로그인 후 콘텐츠를 편집할 수 있습니다.

## 관리자 페이지에서 할 수 있는 것

- 모든 페이지의 문구 수정
- 로고·파비콘 교체 및 이미지 업로드
- 연혁 항목 추가/삭제/순서 변경
- 솔루션 기능 목록 추가/삭제
- FAQ 추가/삭제
- **도입 사례 새 글 작성** (CASE 03, 04... 계속 추가 가능)
- 회사 주소·연락처·이메일 변경

관리자 페이지에서 저장하면 GitHub에 자동 반영되고, Netlify가 사이트를 다시 빌드합니다.
