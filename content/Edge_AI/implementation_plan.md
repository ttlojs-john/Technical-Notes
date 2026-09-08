# [구현 계획] 방화벽 고도화 6대 핵심 기능 및 스마트 국가 통제 시스템 구축

eBPF 실리움(Cilium) & 허블(Hubble) 및 로컬 AI 기반 침입 차단 시스템에 **제안 6대 핵심 기능**을 전면 구축하고, 관리자의 중요한 질문인 **"차단 국가에서의 정상 접속 허용 여부(오탐 방지 및 스마트 감시)"**를 완벽하게 반영한 **지능형 적응형 국가 통제(Smart Geo-Inspection)** 아키텍처를 구현합니다.

---

## 💡 사용자 핵심 질문 분석 및 설계 답변

> **Q. 국가별 대역 일괄 통제는 만약 차단 국가에서 일반적인 접속이 발생할 때도 차단되는 것 아니야? 정상 접속은 허용되는 거야?**

- **A. 매우 중요한 핵심 지적입니다!** 무조건적인 일괄 통째 차단(Strict IP Drop)을 적용하면, 해당 국가의 일반 사용자, 비즈니스 파트너, 해외 출장 중인 임직원의 정상적인 웹 서핑까지 차단되는 부작용이 발생합니다.
- 따라서 본 시스템은 **"지능형 적응형 국가 통제 (Smart / Adaptive Geo-Control)"** 방식으로 구축됩니다:
  1. **화이트리스트 최우선 우회**: 해당 국가 IP라도 관리자가 등록한 화이트리스트 또는 유효한 관리자 세션이 있다면 국가 통제와 무관하게 100% 정상 통과됩니다.
  2. **스마트 위협 감시 모드 (기본값, 추천)**: 해당 국가 IP의 **일반적인 웹 페이지 조회 및 정상 트래픽은 허용**하되, **SSH 접근, 비정상 포트 스캐닝, 로그인 실패, 허니팟 접근, SQLi/경로탐색 등 악성 징후가 1회라도 포착되는 순간에만 '국가 위험 가중치(Risk Multiplier)'를 적용하여 즉각 영구 차단**합니다.
  3. **관리자 모드 선택권**: 상황에 따라 `🛡️ 스마트 위협 감시 모드 (정상 접속 허용)`와 `⛔ 완전 차단 모드 (인바운드 전면 차단)`를 대시보드 스위치 하나로 유연하게 전환할 수 있습니다.

---

## 🚀 구현 6대 핵심 기능 상세

1. **🌍 스마트 국가별 대역 통제 (Adaptive Geo-Inspection & Blocking)**
   - 지정 국가(예: CN, RU, KP 등)에 대한 유연한 정책(스마트 감시 vs 전면 차단).
   - 정상 접속은 허용하면서 침입 징후 발생 시 즉시 가중치 기반 커널 차단.
2. **⚡ 커널 XDP & eBPF 기반 안티-DDoS 및 초고속 레이트 리미팅 (Rate Limiting)**
   - IP별 초당 요청 수(RPS) 및 버스트 임계치 초과 시 커널 계층에서 즉각적인 하드웨어 패킷 드롭.
3. **🍯 AI 침입 유인 허니팟 시스템 (Decoy / HoneyPot Traps)**
   - 가짜 취약 경로(`/.env`, `/admin-login`, `/phpmyadmin` 등) 및 포트(가짜 SSH 2222 등) 트랩 배치.
   - 접근 즉시 공격자로 100% 확정 판정 ➔ 즉각 영구 차단 + 텔레그램 긴급 알림.
4. **🔍 Cilium Tetragon 연동: 커널 런타임 제로 트러스트 (호스트/컨테이너 내부 감시)**
   - 호스트 및 파드 내부의 비인가 쉘/명령어 실행(`execve`), 핵심 시스템 파일(`/etc/shadow` 등) 무단 접근 실시간 감시 및 격리.
5. **📱 텔레그램 봇 양방향 원격 제어 커맨드 (`/ban`, `/unban`, `/whitelist`, `/geoblock`)**
   - 모바일 텔레그램 대화방에서 직접 차단/해제 및 보안 설정 변경 ➔ 웹 대시보드와 커널에 실시간 동기화.
6. **📊 보안 감사 리포트 원클릭 내보내기 & 다운로드 (CSV / HTML / JSON)**
   - 전체 차단 이력, eBPF 플로우, 허니팟 탐지 로그, 런타임 이벤트를 정형화된 보안 감사 보고서(HTML 보고서 및 CSV 데이터)로 즉시 다운로드.

---

## 🛠️ 변경 대상 파일

### 1. 백엔드 코어
- #### [MODIFY] [security_config.json](file:///home/aiadmin01/web-dashboard/security_config.json)
  - `geo_policy`, `rate_limiting`, `honeypot_policy`, `tetragon_policy` 스키마 추가.
- #### [MODIFY] [main.py](file:///home/aiadmin01/web-dashboard/main.py)
  - 스마트 Geo 통제 로직 (`is_geo_blocked_or_flagged`)
  - 레이트 리미터 미들웨어/인터셉터 (`check_rate_limit`)
  - AI 허니팟 트랩 핸들러 (`handle_honeypot_trap`)
  - Tetragon 런타임 이벤트 수집 및 모니터링 API (`/api/security/tetragon-events`)
  - 보안 감사 보고서 내보내기 API (`/api/security/export/csv`, `/api/security/export/html`)
  - 텔레그램 봇 연동을 위한 백엔드 제어 API (`/api/security/remote-ban`, `/api/security/remote-unban` 등)

### 2. 텔레그램 봇
- #### [MODIFY] [main.py](file:///home/aiadmin01/telegram-bot/main.py)
  - 양방향 관리자 원격 명령어 추가:
    - `/ban <IP> [사유]`
    - `/unban <IP>`
    - `/whitelist <IP>`
    - `/geoblock <국가코드>`
    - `/geounblock <국가코드>`
  - 명령어 실행 후 웹 대시보드 API 호출 및 즉각적인 피드백 카드 회신.

### 3. 웹 프론트엔드 UI
- #### [MODIFY] [index.html](file:///home/aiadmin01/web-dashboard/static/index.html)
  - 상단 탭 또는 관제 카드에 **[🌍 스마트 국가 통제]**, **[🍯 AI 허니팟]**, **[⚡ DDoS 레이트 리미팅]**, **[🛡️ Tetragon 런타임]** 섹션 추가.
  - **[📥 보안 감사 리포트 다운로드 (CSV/HTML)]** 원클릭 버튼 제공.

### 4. 검증 및 테스트
- #### [MODIFY] [test_security_ebpf_ai.py](file:///home/aiadmin01/web-dashboard/test_security_ebpf_ai.py)
  - 6대 기능(스마트 Geo 통제, 레이트 리미터, 허니팟 차단, Tetragon 이벤트, 텔레그램 원격 제어, 감사 리포트 내보내기)에 대한 자동화 단위 테스트 추가.

---

## 🧪 검증 계획

### Automated Tests
- `python3 -m unittest test_security_ebpf_ai.py -v`: 신규 6대 기능 엔드포인트 및 정책 엔진 100% 통과 검증.
- `python3 -m py_compile /home/aiadmin01/telegram-bot/main.py`: 텔레그램 봇 코드 정적 문법 검사.

### Manual Verification
- 웹 대시보드(포트 80)에서 스마트 Geo 통제 모드 스위치 및 타겟 국가 토글 동작 확인.
- 허니팟 경로(`/.env`, `/admin-login`) 호출 시 즉각적인 Auto-Ban 및 텔레그램 알림 동작 확인.
- CSV 및 HTML 보고서 파일 정상 다운로드 및 서식 확인.
- 텔레그램 앱에서 관리자가 `/ban 203.0.113.50 테스트차단` 입력 시 실시간 차단 적용 확인.
