# 🧠 02. 전체 시스템 구성도 및 아키텍처 (System Architecture & Drawings)
> **Edge AI 텔레그램 멀티모달 번역 및 웹 통합 관리 시스템 가이드**

---

## 🔗 문서 이동 (Navigation)
- [01. 시스템 개요](file:///home/aiadmin01/edge_ai_guide/01_system_overview.md)
- **[02. 전체 시스템 구성도 및 아키텍처](file:///home/aiadmin01/edge_ai_guide/02_system_architecture.md)**
- [03. 단계별 초기 구축 및 설치 내역](file:///home/aiadmin01/edge_ai_guide/03_installation_history.md)
- [04. 설치 이후 추가 기능 및 업그레이드](file:///home/aiadmin01/edge_ai_guide/04_upgrades_and_evolution.md)
- [05. 상세 컴포넌트 동작 및 데이터 흐름](file:///home/aiadmin01/edge_ai_guide/05_detailed_workflows.md)
- [06. 보안 및 인프라 성능 최적화](file:///home/aiadmin01/edge_ai_guide/06_security_and_tuning.md)
- [07. 운영 관리, 검증 테스트 및 배포 가이드](file:///home/aiadmin01/edge_ai_guide/07_operations_and_deployment.md)

---

## 1. 전체 시스템 구성도 (System Architecture Blueprint)

본 시스템은 마이크로서비스 아키텍처(MSA) 구조로 설계되었으며, 모든 핵심 애플리케이션은 **K3s 쿠버네티스** 상에 배포되어 서로 유기적으로 연동됩니다.

```mermaid
graph TD
    %% 외부 사용자 및 클라이언트 영역
    subgraph "External Clients / End Users"
        User([📱 Telegram App User])
        Admin([💻 Web Admin Browser])
        Attacker([⚠️ Unauthenticated Scanner/Attacker])
    end

    %% 텔레그램 클라우드
    subgraph "Telegram Cloud Ecosystem"
        TelegramAPI[Telegram Bot Cloud Gateway]
    end

    User <-->|Text / Image / Voice / Inline Buttons| TelegramAPI

    %% Edge Node K3s Cluster
    subgraph "Ubuntu 26 Edge Server (16 vCPU, 60GB RAM - K3s Cluster)"
        
        %% 네트워크 인프라 레이어
        subgraph "Ingress & Edge Security Layer"
            Ingress[Traefik / Nginx Ingress Controller (Port 80)]
            SecModule[Direct IP Blocker & Web Banwall]
            Fail2ban[Fail2ban Host Protection (SSH: 22022, 443)]
        end

        Admin <-->|HTTPS / HTTP Port 80| Ingress
        Attacker -.->|Direct IP / Brute-force Attack| SecModule
        Attacker -.->|SSH Port Attack| Fail2ban

        %% 마이크로서비스 레이어
        subgraph "Kubernetes Workloads (Microservices Layer)"
            BotService["💬 telegram-bot (aiogram)<br/>- Asynchronous Polling/Webhook<br/>- VLM / RapidOCR Mode Selector<br/>- TTS Auto Playback Manager"]
            
            AIEngine1["🧠 edge-ai-engine (Pod 1)<br/>FastAPI Worker"]
            AIEngine2["🧠 edge-ai-engine (Pod 2)<br/>FastAPI Worker"]
            
            WebDashboard["📊 web-dashboard (FastAPI + Modern UI)<br/>- K9s Web Terminal & Pod Manager<br/>- Glossary Custom Dictionary<br/>- Realtime Telemetry & Security Audit"]
        end

        TelegramAPI <-->|Long-polling Async Stream| BotService
        Ingress --> WebDashboard
        BotService -->|HTTP REST: /api/v1/process| AIEngine1
        BotService -->|HTTP REST: /api/v1/process| AIEngine2

        %% AI 엔진 내부 컴포넌트
        subgraph "Edge AI Processing Core"
            RapidOCR["🔍 RapidOCR Engine<br/>(ONNX Runtime + Tesseract Fallback)"]
            NMT["🌐 CTranslate2 NMT<br/>(Quantized INT8 NLLB / Marian)"]
            STT["🎙️ Speech Recognition<br/>(Whisper / Google STT)"]
            TTS["🔊 Voice Synthesis<br/>(Edge-TTS / gTTS Pipeline)"]
            VLM["👁️ Direct VLM Parser<br/>(GPT-4o-mini Vision Hybrid)"]
        end

        AIEngine1 & AIEngine2 --- RapidOCR
        AIEngine1 & AIEngine2 --- NMT
        AIEngine1 & AIEngine2 --- STT
        AIEngine1 & AIEngine2 --- TTS
        AIEngine1 & AIEngine2 --- VLM

        %% 스토리지 및 영속화 레이어
        subgraph "Shared Persistent Storage (hostPath & Memory)"
            TokenAudit[("🪙 token_audit_logs.json<br/>(Atomic Shared JSON Storage)")]
            GlossaryDB[("📖 glossary.json<br/>(Custom Translation Dictionary)")]
            UserDB[("👥 users.json<br/>(Bcrypt Hashed Admin Accounts)")]
            AuthLog[("🔒 /var/log/auth.log<br/>(Host SSH Security Log)")]
            SharedMemory["⚡ /dev/shm (8GB RAM Cache)"]
        end

        AIEngine1 & AIEngine2 <-->|Atomic Append/Read| TokenAudit
        AIEngine1 & AIEngine2 <-->|Dictionary Lookup| GlossaryDB
        WebDashboard <-->|Read/Write GUI| GlossaryDB
        WebDashboard <-->|Audit Aggregation| TokenAudit
        WebDashboard <-->|Auth & JWT| UserDB
        WebDashboard <-->|SSH Scan Inspection| AuthLog
        AIEngine1 & AIEngine2 --- SharedMemory

        %% K8s API 연동
        K8sAPI[("☸️ Kubernetes API Server<br/>(RBAC: ClusterRole)")]
        WebDashboard <-->|In-Cluster Pod Exec/Logs/Scale| K8sAPI
    end

    %% 외부 클라우드 AI API
    subgraph "External Cloud AI (Hybrid Fallback)"
        OpenAI[OpenAI API (GPT-4o-mini / GPT-4o)]
    end
    VLM -.->|Optional Hybrid Routing| OpenAI
```

---

## 2. 주요 아키텍처 컴포넌트 설명 (Core Components)

### 2.1 텔레그램 봇 마이크로서비스 (`telegram-bot`)
- **역할**: 텔레그램 메신저 서버와 Long-Polling 방식으로 실시간 이벤트를 주고받는 메시지 게이트웨이입니다.
- **기술 스택**: Python 3.11, `aiogram v3` (비동기 프레임워크).
- **특징**:
  - 오디오 파일, 이미지 및 다중 문장 텍스트를 파싱하여 `edge-ai-engine`으로 전달합니다.
  - OCR(기본 번역)과 VLM(상황 해설) 모드를 전환할 수 있는 인라인 키보드(Inline Keyboards) 사용자 환경(UI)을 제공합니다.

### 2.2 Edge AI 프로세싱 엔진 (`edge-ai-engine`)
- **역할**: 입력받은 데이터의 종류(이미지, 음성, 텍스트)에 맞춰 분기 처리하고 AI 추론을 실행하는 핵심 백엔드 API입니다.
- **기술 스택**: Python, FastAPI, ONNX Runtime, CTranslate2.
- **특징**:
  - `replicas: 2`로 기동하여 로드를 분산 처리합니다.
  - 내부 로컬 추론 모듈과 외부 GPT API(VLM Fallback용)를 라우팅하는 하이브리드 중계기 역할을 담당합니다.

### 2.3 웹 관리자 대시보드 (`web-dashboard`)
- **역할**: 시스템 메트릭, 인클러스터 리소스 현황, 번역 사전 관리, 보안 로그 확인을 위한 관리 화면입니다.
- **기술 스택**: Python, FastAPI, Vanilla JS / HTML CSS.
- **특징**:
  - Kubernetes API Server와 직접 통신할 수 있는 RBAC ServiceAccount가 할당되어 클러스터 내의 리소스 관리를 웹 인터페이스로 제공합니다.

---

## 3. 네트워크 토폴로지 및 포트 맵 (Network Ports)

엣지 노드 내부의 네트워크 흐름은 외부 Ingress로부터 각각의 K8s Service로 분기됩니다.

| 포트 번호 | 프로토콜 | 서비스명 | 공개 범위 | 역할 |
| :--- | :--- | :--- | :--- | :--- |
| **80** | HTTP | Ingress (Traefik) | 외부 공개 | 웹 대시보드 접근용 게이트웨이 |
| **443** | TCP/SSH | Host Server | 외부 공개 | SSH 원격 접속 및 Fail2ban 감시 대상 |
| **22022** | TCP/SSH | Host Server | 외부 공개 | SSH 대체 포트 및 Fail2ban 감시 대상 |
| **8000** | HTTP | `edge-ai-engine` | K8s 내부 전용 | 봇 및 대시보드 통신용 백엔드 REST API |
| **3000** | HTTP | `web-dashboard` | K8s 내부 전용 | 관리자 웹 서버 포트 |
| **5432** | TCP | `postgresql` (Bitnami) | K8s 내부 전용 | 영속 로깅 및 감사 데이터 저장 데이터베이스 |
