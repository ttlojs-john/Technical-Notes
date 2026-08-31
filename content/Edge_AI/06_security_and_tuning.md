# 🛡️ 06. 보안 및 인프라 성능 최적화 (Security & Performance Tuning)
> **Edge AI 텔레그램 멀티모달 번역 및 웹 통합 관리 시스템 가이드**

---

## 🔗 문서 이동 (Navigation)
- [01. 시스템 개요](file:///home/aiadmin01/edge_ai_guide/01_system_overview.md)
- [02. 전체 시스템 구성도 및 아키텍처](file:///home/aiadmin01/edge_ai_guide/02_system_architecture.md)
- [03. 단계별 초기 구축 및 설치 내역](file:///home/aiadmin01/edge_ai_guide/03_installation_history.md)
- [04. 설치 이후 추가 기능 및 업그레이드](file:///home/aiadmin01/edge_ai_guide/04_upgrades_and_evolution.md)
- [05. 상세 컴포넌트 동작 및 데이터 흐름](file:///home/aiadmin01/edge_ai_guide/05_detailed_workflows.md)
- **[06. 보안 및 인프라 성능 최적화](file:///home/aiadmin01/edge_ai_guide/06_security_and_tuning.md)**
- [07. 운영 관리, 검증 테스트 및 배포 가이드](file:///home/aiadmin01/edge_ai_guide/07_operations_and_deployment.md)

---

## 1. 다계층 보안 구조 (Multi-layered Security)

본 시스템은 호스트 OS 수준부터 애플리케이션 REST API 수준에 이르기까지 촘촘한 보안 필터를 구성하고 있습니다.

### 1.1 호스트 레벨 SSH 무차별 대입 공격 차단 (`setup_fail2ban.sh`)
공용 네트워크상에서 유입되는 SSH 침입 시도를 차단하기 위해 Fail2ban 규칙을 구축하여 백그라운드 데몬으로 상시 기동합니다.

- **대상 포트**: 22022 (기본 변경 포트) 및 443 (HTTPS 공용망 감시)
- **로그 모니터링**: `/var/log/auth.log`를 정밀 파싱하여 비밀번호 5회 연속 실패 IP를 실시간으로 탐색합니다.
- **차단 수행**: 감지 즉시 호스트 `iptables` 방화벽 차단 테이블에 등록하여 24시간 동안 서버 접근을 완전히 차단합니다.
- **감시 상태 조회**:
  ```bash
  sudo fail2ban-client status sshd
  ```

---

### 1.2 웹 대시보드 직접 IP 접근 원천 거부 (Direct IP Blocking)
악의적인 봇이나 인터넷 스캐너가 서버의 원시 IP 주소로 포트 스캔을 하며 웹 대시보드에 접근하는 것을 원천적으로 차단합니다.

- **차단 조건**: 들어오는 HTTP Header의 Host 값이 승인 도메인(`edgeai.local`)이 아닐 경우, `HTTP 403 Forbidden` 처리합니다.
- **관리자 설정**: 웹 대시보드 `web-dashboard/deployment.yaml` 내 환경 변수에서 손쉽게 활성화 및 도메인 지정이 가능합니다.
  ```yaml
  env:
  - name: BLOCK_DIRECT_IP
    value: "true"
  - name: ALLOWED_DOMAIN
    value: "edgeai.local"
  ```

---

### 1.3 웹 로그인 브루트포스(Brute-Force) 자체 방어 메커니즘
관리자 비밀번호를 무작위로 추측하는 공격을 무력화하기 위해 대시보드 백엔드 단에 인메모리 차단 레지스트리를 구현했습니다.

- **동작**: 특정 IP 대역에서 로그인 시도가 연속 3회 실패할 경우, 해당 클라이언트 IP는 영구적으로 로그인 접근이 제한됩니다.
- **해제**: 웹 관리 콘솔 보안 탭에서 차단된 IP 목록을 시각적으로 확인하고 '원클릭 해제'가 가능하도록 편의를 지원합니다.

---

## 2. 16 vCPU & 60GB RAM OS 커널 최적화 (`tune_memory.sh`)

인공지능 모델(RapidOCR, CTranslate2 NMT 등)은 고용량 메모리 입출력이 빈번하여 OS 커널 수준의 파라미터 최적화가 전체 처리 대기 시간(Latency) 단축에 매우 결정적인 역할을 합니다.

```bash
# /etc/sysctl.d/99-ram-optimization.conf

# 1. 60GB 대용량 RAM 우선 활용 정책 (디스크 스왑 방지)
vm.swappiness = 10                  # 메모리가 거의 찰 때까지 디스크 스왑을 미룹니다.
vm.vfs_cache_pressure = 50          # 리눅스 파일 시스템 메타데이터 캐시 소멸 주기를 늘려 디스크 접근 지연을 감소시킵니다.
vm.dirty_ratio = 20                 # 활성 메모리 상의 더티 페이지 쓰기 버퍼 한도
vm.dirty_background_ratio = 5       # 디스크 백라이트 쓰기 스레드 시작 임계치

# 2. 동시 트래픽 및 네트워크 소켓 대역 확장
net.core.somaxconn = 4096           # 동시 TCP 백로그 소켓 연결 대기 큐 크기 확장
net.ipv4.tcp_max_syn_backlog = 4096 # 대량 접속 시 TCP 핸드셰이크 처리 대기열 확장
fs.file-max = 2097152               # 시스템 전체 열기 가능한 파일 핸들 최댓값 상향
```

### 튜닝 적용 및 반영 명령어
```bash
sudo chmod +x /home/aiadmin01/tune_memory.sh
sudo /home/aiadmin01/tune_memory.sh
```
실행 결과 OS 커널 메모리 상태가 즉시 갱신되어 최적의 속도로 동작하게 됩니다.
