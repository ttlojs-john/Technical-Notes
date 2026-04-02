# [Phase 2] chaeyul.uk 2차 고도화 (Secondary Enhancements)

**업데이트 기간**: 2026년 3월 12일 ~ 3월 14일

**프로젝트 개요**: Phase 2에서는 대규모 학습 데이터를 효율적으로 처리하기 위한 캐시 시스템과 학습자 중심의 게임화(Gamification) 요소, 그리고 UI/UX의 글로벌 테마 동기화에 초점을 맞추었습니다.

## 🌟 1. 주요 고도화 기능 (Secondary Features)

### Smart Dictionary & Hybrid Cache 시스템 구축
- **스마트 사전**: AI 기반 맥락 분석을 통해 단어의 의미/예문을 동적으로 추천하고, 사용자 단어장과 연동되는 고성능 검색 파이프라인 최적화.
- **하이브리드 다중 계층 캐시**: Redis 등 인메모리(L1)와 Disk/DB(L2)를 분리 조합하여 데이터 조회 응답 속도를 10ms 이하로 단축. `hybrid_cache_hits_total` 등 커스텀 메트릭을 통한 실시간 Prometheus 감시 연동.

### 퀴즈 시스템 전면 개편 (Smart Quiz Center)
- 기존 학습 페이지를 4대 게임 모드로 다각화 확장.
  - 🧠 클래식 (단어 뜻 맞추기 - 4지선다)
  - ⌨️ 스펠링 전문가 모드 (한국어 힌트 기반 독일어 직접 타이핑)
  - ✏️ 빈칸 채우기 (회화 문항 기반)
  - 💬 회화 문장 전체 퀴즈
- Glassmorphism 기반의 프리미엄 디자인 적용으로 시각적 퀄리티 상승.

### 글로벌 테마 동기화 (Unified Theme System)
- `localStorage`의 `theme` 단일 키를 활용한 `/js/theme.js` 공통 모듈화 완성.
- 메인, 퀴즈 페이지뿐 아니라 30개 이상의 서브 Lesson 파일 전체에 걸친 즉각적이고 깜빡임 없는 주야간(Light/Dark) 테마 동기화 스크립트 작성 완비.

### 텔레그램 연동 및 회화 문장 관리 (CMS 2.0)
- 텔레그램 알림 시스템을 관리자 메뉴 내에서 독립된 탭으로 분리하여 수정/이력/즉시 발송 등 개별 조작 효율화.
- 사용자가 업로드한 CSV 파일을 통해 수십 개의 회화 문장을 일괄 다이렉트 맵핑 (동적 컬럼 헤더 매칭 알고리즘 적용).

## 🛠 2. 주요 장애 조치 (Troubleshooting)

- **SQLAlchemy Schema Mismatch (DB)**: FastAPI Pydantic 모델에 추가된 새 컬럼(`situation`, `pronunciation`)이 물리적 DB에 자동 마이그레이션 되지 않는 이슈 발생 (`UndefinedColumn`). `ALTER TABLE` 직접 제어로 해결하였으며 향후 Alembic 도입 필요성 규명.
- **다크 모드 적용 누락 (Theme Racing Issue)**: `replace_file_content` 도구 한계 및 인라인 코드의 한계로 인해 Lesson 페이지 간 함수 미적용 문제가 나타났으나, 공통 스크립트 모듈 한 개로 일괄 대체하여 근본적 충돌 파훼 완료.
- **사용자 모달 표시 불량 (Z-Index)**: 통계 모달 창이 부모 요소 클리핑(`transform` 박스)에 갇히는 문제를 막기 위해 코드를 `<body>` 직계로 이관하고 `position: fixed` 및 절대 우위 인덱싱을 고정하여 가시성 문제 돌파.
