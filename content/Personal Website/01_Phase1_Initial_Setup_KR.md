# [Phase 1] chaeyul.uk 초기 웹 서버 구축 및 핵심 기능 (Initial Setup)

**프로젝트 개요**: 본 프로젝트는 프리미엄 미디어(사진, 동영상, 오디오) 관리 및 스트리밍을 위한 전용 웹 서버 구축을 목적으로 합니다. 고화질 미디어 보관에 최적화된 UI와 안전한 데이터 관리를 위한 백엔드 구조를 갖추고 있습니다.

## 📌 1. 인프라 운영 및 관리 아키텍처

### Docker Compose 환경
- **Frontend**: Node.js (Express) - 포트 80/443 매핑, 정적 파일 제공 및 리버스 프록시, API Rate Limiting 서버
- **Backend**: Python (FastAPI) - REST API 서버 및 미디어/페이지 관리 비즈니스 로직
- **Database**: PostgreSQL 15 - 메타데이터 및 계정 정보 영구 저장소
- **Infrastructure**: Cloudflare Proxy & Linux 환경으로 외부 접속 관리 및 SSL 오프로딩

## 🌟 2. 주요 구축 기능 (Core Features)

### 사용자 도메인 및 가족 공동 브랜딩
- 메인 도메인(`chaeyul.uk`) 설정 및 IP 접속 원천 차단으로 보안 강화.
- 사이트 이름을 `CHAEEUN & CHAEYUL`로 업데이트하고 대시보드 내 동적 설정 가능하도록 개선.

### 관리자 대시보드 및 CMS 고도화
- 관리자 페이지 내에서 내장 에디터를 통해 HTML/CSS 코드를 즉시 변경하고 사이트에 실시간 반영(CMS).
- `settings.json`을 통한 네비게이션 및 디자인 영속화.
- 사이드바 기반 네비게이션 및 통합 대시보드 요약 시스템.
- 2단계 구글 OTP 인증(2FA) 도입으로 관리자 로그인 보안 엔터프라이즈 수준으로 강화.

### 유튜브 독어 학습관 (German Study Center)
- 유튜브 API를 통한 실시간 독어/영어 자막 추출 및 클릭 시 사전 조회 기능 도입.
- 개인 맞춤형 구간 반복 시스템 및 브라우저 영속화 적용.
- TTS(Text-to-Speech) 및 자동 번역, 모바일 백그라운드 재생 지원 설계.

### 미디어 갤러리 (Masonry Style)
- CSS Columns를 활용한 고품격 갤러리 레이아웃 구축.
- 사진 EXIF 분석 후 연도별 자동 분류 필터 제공, 비디오 호버 미리보기 시스템.

## 🛠 3. 장애 조치 내역 (Troubleshooting)

- **로그인 모달 충돌 이슈**: `id="loginModal"` 내부 CSS의 충돌(`display: flex` / `none`)을 제거하고 자바스크립트로만 상태를 제어하여 로딩 시 화면을 가리는 현상 해결.
- **백엔드 DB 누락 이슈**: `migrate.py` 마이그레이션 스크립트를 통해 누락된 열 추가 (예: `telegram_chat_id`).
- **무차별 대입(Brute Force) 공격 방어**: 단순 API 차단을 넘어 프론트엔드 Node.js단에 `express-rate-limit`을 도입하여 1차 방어선 구축 및 Real IP 확보.

---
> [!NOTE]
> 본 문서는 V3/V4 등 대규모 확장 모듈이 적용되기 전의 **초기 서버 아키텍처와 코어 시스템(March 초반부 기준)**을 정리한 Phase 1 기록입니다. 이후 고도화 내역은 다음 Phase 문서에서 다뤄집니다.
