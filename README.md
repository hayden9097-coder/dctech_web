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

관리자 페이지(`/admin/`)는 **GitHub 계정으로 로그인**하는 방식입니다.
배포 후 아래 1회 설정이 필요합니다.

### 1. Netlify에 배포

[Netlify](https://app.netlify.com)에서 `dctech_web` 저장소를 연결해 배포합니다.
빌드 설정(`npm run build` → `dist`)은 `netlify.toml`에 이미 정의되어 있습니다.

### 2. GitHub OAuth App 생성

GitHub > Settings > Developer settings > **OAuth Apps** > New OAuth App

| 항목 | 값 |
|---|---|
| Application name | DCTech CMS (자유롭게) |
| Homepage URL | 배포된 사이트 주소 |
| Authorization callback URL | `https://api.netlify.com/auth/done` |

생성 후 **Client ID**를 확인하고, **Client Secret**을 발급받아 둡니다.

### 3. Netlify에 OAuth provider 등록

Netlify 사이트 > Site configuration > **Access & security** > OAuth >
**Install provider** > GitHub 선택 후 위의 Client ID / Client Secret 입력

설정이 끝나면 `https://사이트주소/admin/` 접속 → "Login with GitHub" 클릭 →
GitHub 계정으로 로그인하면 콘텐츠를 편집할 수 있습니다.

> 저장소에 쓰기 권한이 있는 GitHub 계정이면 누구나 편집할 수 있습니다.
> 편집자를 추가하려면 GitHub 저장소의 Collaborator로 초대하세요.

## 로컬에서 관리자 화면 미리 써보기

배포/OAuth 설정 없이 내 컴퓨터에서 바로 편집해 볼 수 있습니다.
터미널 두 개를 열어 각각 실행하세요.

```bash
npx decap-server
```

```bash
npm start
```

http://localhost:8080/admin/ 으로 접속하면 로그인 없이 편집할 수 있고,
저장하면 로컬 파일이 직접 수정됩니다.

## 관리자 페이지에서 할 수 있는 것

- 모든 페이지의 문구 수정
- 로고·파비콘 교체 및 이미지 업로드
- 연혁 항목 추가/삭제/순서 변경
- 솔루션 기능 목록 추가/삭제
- FAQ 추가/삭제
- **도입 사례 새 글 작성** (CASE 03, 04... 계속 추가 가능)
- 회사 주소·연락처·이메일 변경

관리자 페이지에서 저장하면 GitHub에 자동 반영되고, Netlify가 사이트를 다시 빌드합니다.
