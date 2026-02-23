# OpenClaw Architecture (Updated 2026.02.18)

## 📌 Project Overview
**OpenClaw** is a secure AI agent designed for high-stakes environments.
Unlike typical AI wrappers, it prioritizes **security, isolation, and observability**.
This system now includes a **Disposable Browser Sandbox**, **Code Execution Environment**, and **Human-in-the-Loop Approval**.

## 🏗️ Core Components

### 1. `guardrails-proxy` (Security Gateway)
*   **Role**: Handles ALL communication with external LLMs (OpenAI, Gemini).
*   **Security Features**:
    *   **PII Filtering**: Masks emails, phones, and API keys.
    *   **Command Blocking**: Rejects dangerous commands (`rm -rf`, `sudo`).
    *   **Flexible Policy**: "Filter-first" approach. If injection is detected, it sanitizes input, **Tags** the trace as `security_threat` in, scores it 0.0 in Langfuse, and triggers an alert.
*   **Observability**: Integrated with Langfuse for full trace logging and threat tagging.

### 2. `openclaw-agent` (Brain & Code Sandbox)
*   **Role**: Autonomous problem solver.
*   **Capabilities**:
    *   **Code Execution Sandbox**: Runs Python code in a restricted `/app/workspace` volume for data analysis and file generation (PDF, Charts).
    *   **Autonomy**: Can plan multi-step tasks (Search -> Code -> Python -> File).
    *   **Tool Usage**: Emits `TOOL:PYTHON`, `TOOL:BROWSE` protocols.

### 3. `telegram-gateway` (Interfaces & Controller)
*   **Role**: The bridge between the user and the secure agent.
*   **Functionality**:
    *   **HTML Sanitizer**: Uses `readability` + `html2text` to strip malicious JS/Tags from web content *before* LLM processing.
    *   **Human-in-the-Loop (HIL)**: Intercepts dangerous tools (EMAIL, DELETE) and requires User Approval via Telegram Buttons (Approve/Deny).
    *   **File Delivery**: Automatically detects generated files in workspace and sends them to the user.

### 4. `browser-sandbox` (Disposable Browser)
*   **Role**: Dockerized Chrome/Browserless instance.
*   **Functionality**:
    *   **Isolation**: Executes all web navigation. Malicious sites cannot touch the Host or Agent container.
    *   **Disposable**: Sessions are ephemeral.

### 5. `openclaw-db` & `langfuse-server` (Observability)
*   **Role**: Self-hosted trace storage and analytics dashboard.

## 🔄 Data Flow (Example: "Analyze & Report")

1.  **User (Telegram)**: *"Analyze Samsung Stock and enable email alerts."*
2.  **Gateway**:
    *   Sanitizes input.
    *   Forwards to **Agent**.
3.  **Agent**: Decides to use Python.
    *   Emits `TOOL:PYTHON:<code>`.
4.  **Agent (Sandbox)**: Executes code, generates `report.pdf`.
5.  **Agent**: Decides to send email.
    *   Emits `TOOL:EMAIL:me@example.com`.
6.  **Gateway (HIL)**:
    *   ⚠️ **PAUSE**: Detects sensitive tool `EMAIL`.
    *   Sends **[Approve] / [Deny]** buttons to User.
7.  **User**: Clicks **[Approve]**.
8.  **Gateway**: Executes email, sends `report.pdf` to Telegram, and resumes Agent loop.

## 🔒 Security Principles
*   **Zero-Trust**: Agent assumes all external input is untrusted (`<<<EXTERNAL_DATA>>>`).
*   **Input Sanitization**: Raw HTML is never fed to LLM; only sanitized Markdown.
*   **Threat Tagging**: Injections are tagged in Langfuse (`security_threat`) for immediate auditing.
*   **Isolation**:
    *   Browsing -> `browser-sandbox` container.
    *   Code -> `openclaw-agent` workspace volume.

## 🚀 Deployment
Use `docker-compose up --build -d` to launch the full stack.
Configure via `.env` file (see `.env.example`).

## 6. Automation & Scheduling (New)
The system now supports persistent, recurring tasks via the `telegram-gateway`.

### Architecture
- **JobQueue**: Integrated into the Telegram Bot (via `python-telegram-bot`). It manages schedule persistence (in-memory or file-based).
- **TOOL:SCHEDULE**: The agent uses this tool to register a new job in the `JobQueue`.
- **Execution Flow**:
  1. User asks: "Remind me daily at 9am".
  2. Agent calls: `TOOL:SCHEDULE:09:00:Remind User`.
  3. Gateway registers job.
  4. At 09:00, Gateway triggers `process_agent_task` with the stored instruction.

### Data Flow (Scheduled)
`Timer (09:00)` -> `Gateway JobQueue` -> `Agent API` -> `Tool Execution` -> `Gateway` -> `User`

---

## 📜 Architecture Evolution Log

- **2026-02-09**: Initial Deploy (Gemini/GPT-4).
- **2026-02-14**: "Vibe Coding" Refactor & Langfuse Observability.
- **2026-02-18**: Security Hardening (Sandbox, Guardrails Filter) & **Scheduler Integration**.
*   **Added**: `browser-sandbox` (Disposable Browserless/Chrome) for isolated web browsing.
*   **Added**: Code Execution Sandbox in `openclaw-agent` (runs Python in `/app/workspace`).
*   **Enhanced**: `telegram-gateway` with HTML Sanitizer (Readability+html2text) and HIL Approval Buttons.
*   **Modified**: `guardrails-proxy` policy to "Filter & Tag" strategy with Langfuse Alerting.

### [2026-02-17] Telegram Integration Release (v1.0)
*   **Added**: `telegram-gateway` service.
    *   Features: Re-Act Loop, JobQueue (Daily Briefing), User Message History.
*   **Added**: `openclaw-agent` Tool Protocol (`TOOL:WEATHER`, `TOOL:SEARCH`).
*   **Removed**: Direct User Frontend (Shifted entirely to Telegram Bot).

### [2026-02-16] Observability Integration
*   **Fixed**: `langfuse-server` & `db` container connectivity and schema migration.
*   **Modified**: `guardrails-proxy` to inject Langfuse Traces for every LLM call.

### [2026-02-09] GPT-4 Integration
*   **Modified**: Backend configuration to support GPT-4 API calls.

### [2026-02-08] Initial Deployment (Legacy)
*   **Created**: Basic FastAPI Backend + React Frontend (Now deprecated).
*   **Created**: Docker Compose baseline.
