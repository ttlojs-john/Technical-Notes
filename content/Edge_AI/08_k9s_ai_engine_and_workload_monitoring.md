# 📊 08. K9s 대시보드 실시간 AI 엔진 및 파드 작업 가시화 가이드 (K9s AI & Workload Monitoring)
> **Edge AI 텔레그램 멀티모달 번역 및 웹 통합 관리 시스템 가이드**

> [!TIP]
> 🌐 **Language / 언어 선택**: **[🇰🇷 한국어 (현재 문서)](./08_k9s_ai_engine_and_workload_monitoring.md)** | **[🇺🇸 Switch to English (영문 버전으로 전환)](./08_k9s_ai_engine_and_workload_monitoring_EN.md)**

---

## 🔗 문서 이동 (Navigation)
- [01. 시스템 개요](./01_system_overview.md)
- [02. 전체 시스템 구성도 및 아키텍처](./02_system_architecture.md)
- [03. 단계별 초기 구축 및 설치 내역](./03_installation_history.md)
- [04. 설치 이후 추가 기능 및 업그레이드](./04_upgrades_and_evolution.md)
- [05. 상세 컴포넌트 동작 및 데이터 흐름](./05_detailed_workflows.md)
- [06. 보안 및 인프라 성능 최적화](./06_security_and_tuning.md)
- [07. 운영 관리, 검증 테스트 및 배포 가이드](./07_operations_and_deployment.md)
- **[08. K9s AI 엔진 워크로드 모니터링](./08_k9s_ai_engine_and_workload_monitoring.md)**
- [09. MLOps 멀티 엔진 아키텍처 & 벤치마크](./09_mlops_multi_engine_architecture_and_benchmark.md)
- [10. 스마트 텍스트 청킹 & 메시지 분할기](./10_smart_text_chunking_and_message_splitter.md)
- [11. 외부 AI (Gemini) 연동 관리](./11_external_ai_gemini_integration_and_admin_console.md)
- [12. 호스트 방화벽 & 침입 방지 가이드](./12_host_os_firewall_and_intrusion_prevention_guide.md)
- [13. 하드웨어 스케일업 & 32C/192GB/GPU 최적화](./13_hardware_scaleup_32core_192gb_gpu_optimization.md)
- [14. eBPF 실리움 & 로컬 AI 방화벽 + 텔레그램 관제](./14_ebpf_cilium_ai_firewall_and_telegram_soc.md)

---

## 1. 개요 및 업그레이드 목적 (Overview & Goals)

클러스터 운영 환경에서 다중 복제본(Multi-Replica)으로 구동되는 **`web-dashboard`**와 분산 추론을 담당하는 **`edge-ai-engine`** 등 파드들이 각각 **어떤 세부 AI 엔진을 구동하고 있는지**, **어떤 역할을 분산 처리하고 있는지**, 그리고 **어떤 소프트웨어/이미지 버전으로 운영되고 있는지**를 관리자가 한눈에 직관적으로 파악할 수 있도록 대시보드 모니터링 시스템을 확장 구축하였습니다.

![Kubernetes AI Workload Monitor: Pods & Engines](/images/dashboard_engine_monitor.jpg)

---

## 2. 세부 파드별 실시간 가동 엔진 및 역할 (Workload & Engine Details)

대시보드의 `📦 Pods 실시간 상태 조회 (K9s Pods)` 테이블에서 실시간 수집 및 표기되는 서비스별 세부 메타데이터 구성입니다.

| 파드 구분 (Workload) | 실시간 수행 작업 (Task Role) | 가동 중인 세부 엔진 (Active AI & System Engines) | 운영 버전 및 태그 (Version / Tag) |
| :--- | :--- | :--- | :--- |
| **`edge-ai-engine`**<br>*(2 Replicas)* | **`🧠 Edge AI 추론 엔진 (Active)`**<br>독일어 OCR 인식 / 신경망 번역 / 비즈니스 작문 / VLM 시각언어 분석 | ⚡ `RapidOCR (ONNX)` : 16 vCPU 최적화 문자 인식<br>⚡ `CTranslate2 (INT8 NMT)` : 로컬 고속 신경망 기계번역<br>⚡ `VLM One-Shot` : 시각-언어 복합 문서 심층 분석<br>⚡ `Neural TTS` : 독일어 음성 합성 엔진 | `🏷️ latest`<br>*(edge-ai-engine:latest)* |
| **`web-dashboard`**<br>*(2 Replicas)* | **`🌐 관리자 콘솔 & API (HA 로드밸런싱)`**<br>2-Replica 고가용성 분산 세션 관리 / 클러스터 실시간 제어 / 보안 감사 | ⚡ `K9s Cluster Monitor` : 쿠버네티스 In-Cluster 실시간 감시<br>⚡ `WAF 방화벽` : 무차별 대입 공격 실시간 차단 & IP 통제<br>⚡ `토큰 감사 로거` : VLM/NMT 누적 사용량 추적<br>⚡ `REST API Engine` : 클러스터 제어 및 터미널 웹 Exec | `🏷️ latest`<br>*(web-dashboard:latest)* |
| **`telegram-bot`**<br>*(1 Replica)* | **`💬 텔레그램 봇 인터페이스`**<br>사용자 메시지/사진/음성 수신 및 Edge AI 실시간 파이프라인 중계 | ⚡ `Telegram Polling Engine`<br>⚡ `Edge AI Pipeline Router` | `🏷️ latest`<br>*(telegram-bot:latest)* |
| **`postgres-postgresql-0`**<br>*(StatefulSet)* | **`🗄️ PostgreSQL 데이터베이스`**<br>영속 데이터 및 세션/감사 로그 스토리지 | ⚡ `PostgreSQL Storage Engine` | `🏷️ 18.6.0`<br>*(bitnami/postgresql:latest)* |

---

## 3. 백엔드 및 프론트엔드 아키텍처 구현 (Implementation Architecture)

### 3.1 백엔드 메타데이터 분석 엔진 (`web-dashboard/main.py`)
- **버전 태그 추출**: 파드 컨테이너 명세(`spec.containers[].image`) 및 레이블(`labels`)을 파싱하여 도커 이미지 태그 및 버전 번호를 동적으로 반환합니다.
- **파드 역할(Role) 및 구동 엔진 식별**: 파드 이름 규칙과 런타임 환경을 매핑하여 각 서비스가 수행 중인 활성 엔진(`task_info.engines`)과 작업 요약(`task_info.description`)을 REST API 응답에 실시간 포함합니다.

```python
# web-dashboard/main.py (발췌)
if "edge-ai-engine" in pod_name:
    task_info = {
        "type": "ai",
        "title": "🧠 Edge AI 추론 엔진 (Active)",
        "engines": ["RapidOCR (ONNX)", "CTranslate2 (INT8 NMT)", "VLM One-Shot", "Neural TTS"],
        "description": "독일어 OCR 인식 / 신경망 번역 / 비즈니스 작문 / VLM 시각언어 분석"
    }
elif "web-dashboard" in pod_name:
    task_info = {
        "type": "web",
        "title": "🌐 관리자 콘솔 & API (HA 로드밸런싱)",
        "engines": ["K9s Cluster Monitor", "WAF 방화벽", "토큰 감사 로거", "REST API Engine"],
        "description": "2-Replica 고가용성 분산 세션 관리 / 클러스터 실시간 제어 / 보안 감사"
    }
```

### 3.2 프론트엔드 UI/UX 설계 (`web-dashboard/static/index.html`)
- **실시간 수행 작업 열 신설**: `실시간 수행 작업 / 구동 AI 엔진 (Role)` 전용 컬럼을 구성하여 사이버펑크 딥 다크 테마에 어울리는 네온 뱃지와 서브 뱃지로 표시합니다.
- **버전/태그 전용 뱃지**: `Version / Image` 열에 네온 퍼플 뱃지(`🏷️ latest`, `🏷️ 18.6.0`)를 적용하고 마우스 오버 시 전체 이미지 URI 툴팁을 제공합니다.
- **디버그 인스펙터 연동**: `🩺 초강력 디버깅` 탭과 `🚀 Deployments 상태` 테이블에도 동일한 버전 태그 뱃지를 연계하여 모니터링 일관성을 확보했습니다.

---

## 4. 검증 및 무중단 적용 절차 (Verification & Deployment)

1. **자동 E2E 엔드투엔드 테스트 실행**:
   ```bash
   python3 /home/aiadmin01/web-dashboard/test_k9s_dashboard.py
   ```
2. **K8s 롤아웃 무중단 갱신**:
   ```bash
   kubectl rollout restart deployment/web-dashboard
   ```
3. **웹 대시보드 브라우저 확인**:
   브라우저에서 대시보드(`http://edgeai.local/` 또는 `http://<서버IP>/`) 접속 후 새로고침(`F5`) 시 각 파드별 가동 AI 엔진과 2대 분산 작업 내용이 실시간 렌더링됩니다.
