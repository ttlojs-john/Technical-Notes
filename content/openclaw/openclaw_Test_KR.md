# 🤖 OpenClaw: 자율 AI 에이전트 아키텍처 및 제로 트러스트 보안 체계
> **일회용 브라우저 샌드박스, 보안 가드레일, 인간 참여형(HIL) 승인 체계를 갖춘 보안 중심 자율 에이전트**

> [!TIP]
> 🌐 **Language / 언어 선택**: **[🇰🇷 한국어 (현재 문서)](./openclaw_Test_KR.md)** | **[🇺🇸 Switch to English (영문 버전 읽기)](./openclaw_Test.md)**

---

## 🔗 문서 이동 (Navigation)
- [OpenClaw Architecture & Security (EN)](./openclaw_Test.md)
- **[OpenClaw 아키텍처 및 보안 체계 (KR)](./openclaw_Test_KR.md)**

---

## 📌 프로젝트 개요 (Project Overview)

**OpenClaw**는 고신뢰 엔터프라이즈 환경을 위해 설계된 보안 중심 자율 AI 에이전트 플랫폼입니다.
단순한 LLM Wrapper 라이브러리와 달리, **철저한 제로 트러스트(Zero-Trust) 격리, 전방위 관측성(Observability), 그리고 다단계 인간 승인(Human-in-the-Loop)** 원칙을 엄격하게 준수합니다.
이 시스템은 **일회용 브라우저 샌드박스(Disposable Browser Sandbox)**, **독립 코드 실행 볼륨(Code Execution Sandbox)**, 그리고 **텔레그램 관리자 양방향 승인 게이트웨이**를 유기적으로 결합하여 구축되었습니다.

---

## 🏗️ 전체 시스템 아키텍처 (Architecture Blueprint)

```mermaid

graph TD
    User([📱 텔레그램 관리자])

    subgraph TelegramGateway ["텔레그램 게이트웨이 & 컨트롤러"]
        BotHandler["텔레그램 이벤트 수신부"]
        HTMLSanitizer["HTML 정제 엔진<br/>(readability + html2text)"]
        HILGuard["⚠️ HIL 승인 게이트<br/>(승인/거부 인라인 버튼)"]
    end

    subgraph Guardrails ["보안 및 거버넌스 프록시"]
        PIIFilter["개인정보 마스킹 필터<br/>(이메일/전화번호/API 키 난독화)"]
        CommandFilter["위험 명령어 차단기<br/>(`rm -rf`, `sudo` 즉시 차단)"]
        ThreatScorer["Langfuse 위협 채점기<br/>(프롬프트 인젝션 시 0.0점 부여)"]
    end

    subgraph AgentSandbox ["OpenClaw 에이전트 코어"]
        Brain["🧠 에이전트 추론 엔진 & ReAct 플래너"]
        CodeVol["📦 /app/workspace<br/>(격리된 파이썬 실행 볼륨)"]
    end

    subgraph DisposableBrowser ["일회용 브라우저 샌드박스"]
        HeadlessChrome["🌐 임시 헤드리스 크롬<br/>(일회용 컨테이너 격리)"]
    end

    subgraph ExternalLLM ["외부 클라우드 대규모 언어 모델"]
        LLMs["OpenAI / Anthropic / Gemini API"]
    end

    subgraph Observability ["원격 관측 및 감사 로깅"]
        LangfuseDB[("📊 Langfuse 추적 데이터베이스")]
    end

    User <-->|"원격 제어 및 인라인 승인"| BotHandler
    BotHandler --> HTMLSanitizer
    HTMLSanitizer --> Brain
    Brain --> Guardrails
    Guardrails --> LLMs
    Guardrails -.-> LangfuseDB

    Brain -->|"TOOL:PYTHON"| CodeVol
    Brain -->|"TOOL:BROWSE"| HeadlessChrome
    Brain -->|"TOOL:SENSITIVE (이메일 발송 등)"| HILGuard

    HILGuard -->|"관리자 승인 모달 전송"| User
```

---

## 🧩 5대 핵심 아키텍처 컴포넌트

### 1. `guardrails-proxy` (보안 게이트웨이)
* **역할**: 외부 상용 LLM(OpenAI, Gemini 등)과 주고받는 모든 입출력 트래픽을 단일 통로로 검증 및 필터링합니다.
* **주요 보안 기능**:
  * **개인정보(PII) 필터링**: 이메일, 전화번호, 사내 비밀 API 키를 외부 전송 전 자동 마스킹.
  * **위험 명령어 차단**: 셸 인젝션 및 파괴적 명령어(`rm -rf`, `sudo`, `dd` 등)를 사전 차단.
  * **필터 우선 정책**: 프롬프트 인젝션이 감지되면 입력을 강제 소독하고, Langfuse에 `security_threat` 태그를 부착(위협 점수 0.0점)한 뒤 관리자 경보를 발생시킵니다.
* **관측성(Observability)**: 모든 호출 트레이스를 Langfuse에 중앙 집중식으로 보관하여 감사를 보장합니다.

### 2. `openclaw-agent` (추론 두뇌 및 코드 샌드박스)
* **역할**: 복잡한 문제 해결을 자율적으로 수행하는 에이전트 본체.
* **기능**:
  * **코드 실행 격리 샌드박스**: `/app/workspace` 전용 마운트 공간 내에서만 파이썬 코드를 실행하여 데이터 분석 및 보고서(PDF, 차트)를 생성합니다.
  * **자율 계획(ReAct)**: 다단계 작업(정보 검색 ➔ 코드 작성 ➔ 파이썬 실행 ➔ 결과 파일 송출)을 스스로 수립하고 실행합니다.

### 3. `telegram-gateway` (인터페이스 및 HIL 컨트롤러)
* **역할**: 사용자와 에이전트 간의 실시간 브릿지 인터페이스.
* **기능**:
  * **HTML 무해화(Sanitizer)**: 외부 웹 페이지를 스크래핑할 때 악성 자바스크립트 및 태그를 `readability`와 `html2text`로 전처리하여 LLM에 전달.
  * **인간 참여형(Human-in-the-Loop)**: 이메일 외부 전송, 파일 삭제 등 민감도가 높은 도구 실행 시 임의로 처리하지 않고 관리자 텔레그램으로 **[승인 / 거부]** 모달을 띄워 최종 결재를 받습니다.

### 4. `browser-sandbox` (일회용 브라우저)
* **역할**: 도커 기반 독립 컨테이너로 구동되는 브라우저리스(Browserless) 크롬 인스턴스.
* **격리 원칙**: 웹 탐색 세션은 임시(Ephemeral)로 생성되고 파기되므로 악성 사이트에 접속하더라도 호스트나 에이전트 컨테이너에 일절 영향을 주지 않습니다.

---

## 🔄 엔드-투-엔드 데이터 흐름: "주식 분석 및 리포트 발송"

```mermaid

sequenceDiagram
    autonumber
    actor User as "📱 텔레그램 사용자"
    participant Gateway as "🚪 텔레그램 게이트웨이"
    participant Agent as "🧠 OpenClaw 에이전트"
    participant Sandbox as "📦 파이썬 샌드박스"
    participant HIL as "⚠️ HIL 승인 게이트"
    participant Browser as "🌐 브라우저 샌드박스"

    User->>Gateway: "삼성전자 주가 데이터 분석 및 요약 리포트 이메일 발송해줘"
    Gateway->>Gateway: 입력값 정제 및 보안 세션 검증
    Gateway->>Agent: 정제된 프롬프트 전달
    Agent->>Browser: TOOL:BROWSE (실시간 금융 지표 크롤링)
    Browser-->>Agent: 원시 HTML 정제 ➔ 안전한 마크다운 회신
    Agent->>Sandbox: TOOL:PYTHON (데이터 가공 및 report.pdf 생성)
    Sandbox-->>Agent: 생성 파일 저장 (/app/workspace)
    Agent->>HIL: TOOL:EMAIL:admin@example.com (발송 요청)
    HIL-->>User: ⚠️ 민감 작업 발생: 이메일을 발송할까요? [승인] [거부]
    User->>HIL: [승인] 버튼 클릭
    HIL->>Agent: 실행 재개 승인 신호 전달
    Agent->>User: 📧 이메일 발송 완료 통보 및 📄 report.pdf 텔레그램 전달
```

---

## 🔒 핵심 보안 설계 원칙
1. **외부 데이터 불신 원칙**: 인터넷에서 수집된 모든 외부 데이터는 `<<<EXTERNAL_DATA>>>` 구획으로 격리되며, 날것의 실행 태그는 전면 제거됩니다.
2. **비가역적 행위 통제**: 외부 발송, DB 변경, 파일 영구 삭제와 같은 비가역적 액션은 관리자의 명시적 버튼 승인 없이 자율 수행될 수 없습니다.
