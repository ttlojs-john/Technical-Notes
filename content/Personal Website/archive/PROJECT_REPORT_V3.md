# [3차 업데이트 보고서] chaeyul.uk 프로젝트 시스템 고도화 및 V3.0 파이프라인 구축 (KR/EN)

**기준 기간**: 2026년 3월 15일 ~ 3월 21일
**최종 업데이트**: 2026년 3월 21일

---

## [KOREAN VERSION - 한국어]

## 1. 개요
본 보고서는 2026년 3월 15일부터 21일까지 수행된 `chaeyul.uk` 웹 서버 프로젝트의 3차 업데이트 내역을 다룹니다. 이번 업데이트에서는 시스템의 안정성 강화, 새로운 학습 기능(플래시카드) 도입, V3.0 스마트 자막 파이프라인 구축, 그리고 최종적으로 **지능형 인프라 감시 및 보안 자동 복구 시스템**과 **글로벌 현지화(Localization) 엔진**이 완성되었습니다.

---

## 2. 날짜별 작업 내역

### 📅 3월 15일: 텔레그램 스케줄러 안정화 및 장애 복구
- **비동기 이벤트 루프 버그 수정**: `apscheduler` 객체를 FastAPI의 `startup` 루프 내부로 이동하여 백엔드 프로세스와의 동기화 이슈 해결.
- **DB 데드락(Deadlock) 방지**: 스케줄러가 비정상적으로 DB 세션을 점유하던 문제를 해결하여 로그인 실패 및 서비스 중단 현상 원천 차단.
- **API 예외 처리 강화**: 텔레그램 외부 API 호출 시 타임아웃(Timeout) 및 에러 핸들링 로직을 추가하여 네트워크 지연 시 시스템 마비 방지.

### 📅 3월 16일: 플래시카드(Flashcards) 학습 시스템 통합
- **3D 인터랙티브 학습 UI**: CSS Transform과 3D Flip 효과를 적용하여 실제 카드를 뒤집는 듯한 몰입감 있는 학습 경험 제공.
- **SRS(간격 반복 학습) 알고리즘**: 단어의 숙련도(Known/Unknown)에 따라 노출 빈도를 조절하는 개인 맞춤형 복습 시스템 구축.
- **통합 퀴즈 센터**: 기존 `quiz.html` 내에서 스피드 퀴즈와 플래시카드, 그리고 최근 추가된 Dual N-Back을 자유롭게 선택할 수 있도록 UI 통합 및 최적화.

    ![Quiz UI Dark Mode](/images/quiz_ui_dark_mode.png)
    <p align="center"><i>[그림 1: 스피드 퀴즈, 플래시카드, Dual N-Back이 통합된 다크모드 학습 센터]</i></p>

### 📅 3월 17일: 시스템 최적화 및 UI/UX 정교화
- **반응형 레이아웃 개선**: 모바일 및 태블릿 환경에서의 플래시카드 시인성 및 터치 인터페이스 최적화.
- **데이터 로딩 속도 향상**: 학습 데이터(단어/문장) 호출 시 캐싱 전략을 강화하여 페이지 전환 속도 체감 개선.

### 📅 3월 18일: V3.0 스마트 자막 파이프라인 인프라 구축
- **V3.0 백엔드 API 개발**: 새로운 고성능 자막 자동 생성 파이프라인을 위한 FastAPI 엔드포인트 및 백그라운드 태스크 엔진 구축.
- **관리자 전용 파이프라인 대시보드**: 영상별 처리 상태(Processing, Success, Failed)를 시각화하고, 실패한 작업을 즉시 재시도할 수 있는 관리 도구 구현.
- **유튜브 연동 안정화**: 유튜브 쿠키(Cookies) 주입 로직을 고도화하여 보안 및 API 차단 이슈 해결.

### 📅 3월 19일: 지능형 인프라 모니터링 및 보안 복구 시스템 완성
- **정교한 알림 제어 시스템**: CPU, 메모리, API 응답 실패, 정상 복구 등 각 항목별 알림 발송 여부를 관리자가 직접 선택할 수 있는 대시보드 구현.
- **보안 강화형 텔레그램 웹훅(Webhook)**: 알림 메시지 내 '즉시 재부팅' 버튼 클릭 시, 인가된 관리자인지 2중 검증하는 전용 웹훅 엔진 구현으로 해킹 및 오작동 위험 차단.
- **인프라 통합 UI/UX 리뉴얼**: 분산되어 있던 모니터링 요소를 '수직 스택형 프리미엄 레이아웃'으로 개편. Grafana 차트와 실시간 컨테이너 상태를 한눈에 파악 가능.
- **DB 자동 마이그레이션 엔진**: 시스템 설정 변경 시 데이터베이스 테이블을 실시간으로 감지하고 필요한 컬럼을 자동으로 생성하는 안정화 로직 도입.

    ![Infra Monitoring V2 Dashboard](/images/infra_v2_status.png)
    <p align="center"><i>[그림 2: 글래스모피즘 디자인이 적용된 차세대 인프라 모니터링 전용 대시보드]</i></p>

### 📅 3월 20일: 글로벌 현지화(Localization) 및 엔진 성능 최적화
- **i18n.js 엔진 전면 개편**: Incremental DOM 업데이트 및 MutationObserver 기반 실시간 번역 적용으로 대규모 페이지(관리자 패널 등)의 속도 저하 문제 해결.
- **한국어/영어 전환 시스템 동기화**: 헤더, 메뉴, 모든 관리자 페이지에 실시간 언어 동기화 완료 및 전역 적용.
- **음성 합성 및 자막 최적화**: 대용량 유튜브 영상 처리 시 발생하는 Whisper 413 에러 해결을 위한 오디오 압축 로직 도입.

### 📅 3월 21일: 관리자 대시보드 프리미엄 UI 고도화 및 벌크 AI
- **프리미엄 커스텀 스크롤바**: 모든 리스트에 글래스모피즘 스타일의 고급 스크롤바를 상시 노출하고, 오버스크롤 방지 로직을 도입하여 안정적인 UI 조작성 확보.
- **AI 일괄 처리(Bulk AI) 큐 구현**: 유튜브/홈 배경 영상 목록의 전체 AI 작업을 순차적으로 실행하고, 실패 시에도 다음 작업을 계속하는 큐 매니저 구현.
- **사용성 개선 (Pagination)**: V3 파이프라인 목록에 프론트엔드 페이징 시스템을 도입하여 대규모 데이터 관리 효율성 증대.
- **계정 보안 및 세션 강화**: 로그인 세션 시간을 12시간으로 연장하고, 인증 만료 및 실패 시 상세 진단 로그를 시스템에 기록.

    ![Premium Admin UI](/images/premium_admin_ui.png)
    <p align="center"><i>[그림 3: 커스텀 스크롤바와 일괄 AI 기능이 적용된 프리미엄 관리자 인터페이스]</i></p>

---

## 3. 전체 시스템 아키텍처 (System Architecture)

오늘 완성된 지능형 모니터링 시스템의 전체 구조도입니다. 각 컴포넌트 간의 실시간 데이터 'Ping' 흐름과 보안 웹훅 체계를 시각화했습니다.

![System Architecture V2](/images/system_architecture_v2.png)
<p align="center"><i>[그림 4: 3D 엔진으로 시각화된 전체 시스템 데이터 흐름 및 보안 아키텍처]</i></p>

## 4. 시스템 상태 및 보안 드로잉 (Monitoring Drawing)

전체 시스템의 상태 감시와 컨테이너 보안 복구 체계를 시각화한 드로잉입니다.

![System Monitoring Drawing](/images/system_monitoring_arch.png)
<p align="center"><i>[그림 5: 인프라 헬스체크 및 자동 복구 메커니즘을 시각화한 모니터링 드로잉]</i></p>

---

## 4. 장애 조치 내역 (Troubleshooting)

- **[장애]**: 인프라 설정 저장 시 `TypeError: null` 및 `500/422` 에러 발생.
  - **원인**: UI 개편 중 입력 필드 ID 누락 및 백엔드 DB 스키마/마이그레이션 불일치.
  - **조치**: HTML ID 전수 복구, DB 자동 마이그레이션 로직 추가 및 Pydantic 데이터 검증 스키마 유연화로 해결.
- **[장애]**: 인프라 모니터링 탭에서 Grafana 차트 및 일부 레이아웃 겹침 현상.
  - **원인**: HTML 그리드 중첩 오류 및 CSS z-index 충돌.
  - **조치**: 단일 컬럼 수직 스택 구조로 레이아웃 전면 재설계하여 시인성 및 안정성 확보.

---
---

## [ENGLISH VERSION - 영문]

## 1. Overview
This report documents the 3rd project update of the `chaeyul.uk` system (March 15-21, 2026). Key highlights include system stabilization, Flashcards integration, V3.0 Subtitle Pipeline, the final completion of the **Intelligent Infrastructure Monitoring & Secure Auto-Recovery System**, and the **Global Localization (i18n) Engine**.

---

## 2. Daily Development Logs

### 📅 March 15: Telegram Scheduler Stabilization & Recovery
- **Async Event Loop Fix**: Moved the `apscheduler` object inside the FastAPI `startup` loop.
- **DB Deadlock Prevention**: Resolved DB session occupancy issues.
- **API Exception Handling**: Added timeout and error handling for Telegram API calls.

### 📅 March 16: Flashcards Learning System Integration
- **3D Interactive Learning UI**: Applied 3D Flip effects for an immersive experience.
- **SRS Algorithm**: Built a personalized review system based on proficiency.
- **Integrated Quiz Center**: Unified Speed Quiz, Flashcards, and the newly added Dual N-Back training.

    ![Quiz UI Dark Mode](/images/quiz_ui_dark_mode.png)
    <p align="center"><i>[Figure 1: Unified Dark Mode Learning Center featuring Speed Quiz, Flashcards, and Dual N-Back]</i></p>

### 📅 March 17: System Optimization & UI/UX Refinement
- **Responsive Layout**: Optimized visibility and touch interface for mobile.
- **Data Loading Speed**: Enhanced caching strategies for faster transitions.

### 📅 March 18: V3.0 Smart Subtitle Pipeline Implementation
- **V3.0 Backend API**: Built FastAPI endpoints and task engines for auto-subtitles.
- **Admin Dashboard**: Implemented status visualization and processing tools.
- **YouTube Stabilization**: Updated cookie injection logic for security.

### 📅 March 19: Intelligent Infra Monitoring & Secure Webhook Deployment
- **Granular Alert Controls**: Implemented toggles for CPU, Memory, API, and Recovery alerts.
- **Secure Telegram Webhook**: Developed a dedicated webhook engine requiring authentication.
- **UI/UX Redesign**: Refactored the infra tab into a premium vertical stack with glassmorphism.
- **Auto-Migration Engine**: Introduced logic for automatic DB schema updates.

    ![Infra Monitoring V2 Dashboard](/images/infra_v2_status.png)
    <p align="center"><i>[Figure 2: Next-Gen Infrastructure Monitoring Dashboard with Glassmorphism]</i></p>

### 📅 March 20: Global Localization & High-Performance Engine
- **i18n.js Overhaul**: Optimized dashboard performance with Incremental DOM updates and MutationObserver.
- **Universal Language Sync**: Unified language toggles across all pages including Home, Quiz, and Admin.
- **Whisper 413 Error Fix**: Implemented automatic audio compression for large YouTube video processing.

### 📅 March 21: Premium UI Polish & Bulk AI Automation
- **Custom Glassmorph Scrollbars**: Standardized premium navigation with overscroll containment across all admin lists.
- **Bulk AI Processing**: Implemented a sequential queue manager for "Run All AI" functionality in content lists.
- **UI Usability (Pagination)**: Added frontend pagination for the V3 Status table to handle large data sets.
- **Enhanced Authentication**: Corrected session duration to 12 hours and added diagnostic logging for auth events.

    ![Premium Admin UI](/images/premium_admin_ui.png)
    <p align="center"><i>[Figure 3: Premium Admin Interface with Custom Scrollbars and Bulk AI Features]</i></p>

---

## 3. System Architecture Diagram

![System Architecture V2](/images/system_architecture_v2.png)
<p align="center"><i>[Figure 4: 3D Visualized System Architecture & Data Flow]</i></p>

## 4. System Monitoring Drawing

A visualized overview of the infrastructure health check and security recovery mechanisms.

![System Monitoring Drawing](/images/system_monitoring_arch.png)
<p align="center"><i>[Figure 5: Visualized Monitoring Arch with Auto-Recovery Mechanisms]</i></p>

---

## 4. Troubleshooting

- **[Issue]**: `TypeError: null` and `500/422` errors during infra settings save.
  - **Cause**: Missing HTML IDs and DB schema/migration mismatches.
  - **Resolution**: Restored DOM IDs, added auto-migration logic, and optimized validation schemas.
- **[Issue]**: UI overlaps and missing Grafana charts in the monitoring tab.
  - **Cause**: HTML nesting errors and CSS grid conflicts.
  - **Resolution**: Redesigned the layout into a clean vertical stack for full structural integrity.

---

**[Project Report V3.0 - Final Completion on March 21, 2026]**
