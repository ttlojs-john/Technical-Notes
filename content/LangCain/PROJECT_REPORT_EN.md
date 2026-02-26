# 📘 LangChain AI Agent - Project Completion Report

## 1. Project Overview
This project is a modern, high-performance AI Web Application built using **Next.js** (Frontend) and **FastAPI** (Backend). It leverages **LangChain** to orchestrate interactions with advanced AI models (OpenAI GPT-4o, Google Gemini) while prioritizing **security**, **robustness**, and **scalability**.

---

## 2. System Architecture

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 14+** (React) | Provides a responsive UI for Chat, OCR, and Translation. Uses Proxy rewrites for secure API communication. |
| **Backend** | **FastAPI** (Python) | High-performance asynchronous API handling AI logic, authentication, and file processing. |
| **AI Orchestration** | **LangChain** | Manages LLM context, prompt templates, and model switching (OpenAI/Gemini). |
| **Process Management** | **PM2** | Ensures 24/7 uptime for both Frontend and Backend services on the Ubuntu server. |

---

## 3. Key Features Implementation

### 🤖 AI Chat with Robust Fallback
- **Primary Model**: `gpt-4o` (Optimized for quality).
- **Fallback Mechanism**: Implemented a "Try-Catch" logic. If the primary model fails (e.g., restricted API key, 404 error), the system **automatically downgrades** to `gpt-4o-mini` or `gpt-3.5-turbo` to ensure service continuity without crashing.
- **Multimodal**: Supports image uploads for vision-based analysis.

### 📷 OCR (Optical Character Recognition)
- Extracts text from images using **GPT-4o Vision** or **Gemini Pro Vision**.
- **Privacy-First**: Images are processed in memory or ephemeral storage and deleted immediately after analysis.

### 🌐 Smart Translation
- Uses context-aware prompting to act as a professional translator.
- Supports automatic language detection and target language selection (e.g., Korean, English, German).

### 🗣️ Audio Intelligence (TTS & STT)
- **Text-to-Speech**: Converts text responses into MP3 audio using `gTTS`.
- **Transcription**: Converts uploaded audio files into text for summarization or translation.

---

## 4. Security & Privacy Measures (Implemented)

This project adheres to strict security standards to protect user data and system integrity.

### 🔒 1. PII (Personal Identifiable Information) Redaction
- **Module**: `backend/pii_utils.py`
- **Function**: intercepts user input **before** it reaches external AI APIs.
- **Mechanism**: Uses Regex patterns to detect and mask sensitive data.
  - *Emails* $\rightarrow$ `<EMAIL_ADDRESS>`
  - *Phone Numbers* $\rightarrow$ `<PHONE_NUMBER>`
  - *Credit Cards* $\rightarrow$ `<CREDIT_CARD>`
- **Benefit**: Prevents sensitive data leakage to third-party AI providers (OpenAI/Google).

### 🔑 2. Secure Authentication (JWT)
- **Standard**: OAuth2 with Password Bearer flow.
- **Hashing**: Passwords are hashed using **Bcrypt** before storage (never stored in plain text).
- **Session**: Issues short-lived **JSON Web Tokens (JWT)** for API access control. unauthenticated requests to `/chat` are blocked.

### 🛡️ 3. Environment Security
- **Secret Management**: API Keys (`OPENAI_API_KEY`, `GOOGLE_API_KEY`) and `SECRET_KEY` are isolated in a `.env` file.
- **Deployment Safety**: 
  - The deployment script (`pack_v2.ps1`) **excludes** `.env` files from the artifact to prevent accidental key leakage.
  - The server-side script (`update_env.sh`) allows secure injection of keys directly on the production environment.

### 🧹 4. Automated Lifecycle Management
- **Cleanup Daemon**: A background thread runs every 10 minutes to scan and delete temporary files (`temp_*`, `audio_*`, `output_*.mp3`) older than 10 minutes.
- **Resource Protection**: Prevents disk space exhaustion attacks or data residency issues.

---

## 5. Deployment Workflow & Scripts

The project includes a complete suite of DevOps scripts for automated deployment.

1.  **Packaging**: `pack_v2.ps1` (Windows)
    -   Bundles the codebase, excluding heavy/sensitive folders (`venv`, `node_modules`, `.env`).
2.  **Deployment**: `deploy_ubuntu.sh` (Linux)
    -   Automates system dependency installation (Node.js 20, Python 3.12).
    -   Sets up Virtual Environment (venv) and installs `requirements.txt`.
    -   Builds the Next.js frontend.
    -   Configures specific firewall rules (`ufw allow 8000/3000`).
3.  **Configuration**: `update_env.sh` (Linux)
    -   Interactive tool to safely update API keys and restart services without downtime.

---

### ✅ Conclusion
This system is delivered as a **Production-Ready** AI application. It successfully balances powerful AI capabilities with essential security features, making it suitable for deployment in secure environments.

## 6. Recent Updates (Feb 2026) - Model Configuration & Identity Fixes

### 🔄 GPT Model Configuration Update
- **Issue**: Persistent connection failures (404 Not Found) when attempting to use non-standard model IDs like "GPT-5" or "GPT-5 Nano" on the server environment.
- **Resolution**:
  - Switched primary configuration to the stable and official **GPT-4** model (`gpt-4`).
  - Updated `backend/config.py` to map "GPT-4" correctly.
  - Synchronized `frontend/app/page.tsx` to display "GPT-4" in the model dropdown, eliminating user confusion.

### 🆔 Strict Identity Enforcement
- **Issue**: Models with similar architectures (or when using fallbacks) would sometimes identify themselves significantly different from the selected option (e.g., GPT-5 Nano claiming to be Nano when it was actually Gemini, or vice versa during debugging).
- **Implementation**:
  - Modified `backend/main.py` power system prompts.
  - Added **Conditional Identity Logic**: The system now explicitly guides the model to identify itself based on the user's selection (e.g., "You are GPT-4...").
  - This ensures a consistent user experience where the AI's self-identification matches the interface selection.

### 🛠️ Frontend-Backend Synchronization
- **Fix**: Solved a discrepancy where the Frontend model list was hardcoded and out of sync with the Backend configuration.
- **Mechanism**: Implemented a "Force Update" via `sed` commands on the server to overwrite the `models` state in `page.tsx`, ensuring the UI accurately reflects available backend models.

---

## 7. Advanced Features Update (Feb 10, 2026) - RAG, Usage & Status

### 📚 RAG (Retrieval-Augmented Generation)
- **Goal**: Enable the AI to provide answers based on custom knowledge bases (PDFs/Text) without fine-tuning.
- **Tech Stack**:
  - **Embeddings**: `GoogleGenerativeAIEmbeddings` (`text-embedding-004`) for high speed and accuracy.
  - **Vector Storage**: `ChromaDB` for efficient document chunk indexing and retrieval.
- **Integration**: Implemented `backend/rag_utils.py` and connected it to the `/chat` flow, allowing the tutor to reference uploaded materials in real-time.

### 📊 Token Usage Tracker
- **Backend Logging**: Added `backend/tracker.py` to persist daily token counts (estimated via character count) in `backend/data/usage.json`.
- **Frontend UI**: Integrated a "Usage" button in the header that displays a breakdown of token consumption by model for the current day.

### 🚥 Real-time Model Status Monitoring
- **Health Checks**: Added a `/status` endpoint to verify connectivity with GPT and Gemini APIs.
- **High-Visibility UI**: Introduced high-contrast Emoji indicators (`🟢`/`🔴`) in the header for instant system status awareness.
- **UX Refinement**: Improved header layout spacing, padding, and added text labels to buttons for a more professional and intuitive interface.

---

## 8. Critical Stability & Deployment Update (Feb 13, 2026) - Production Readiness

### 🔧 Stability Fixes (Critical)
- **Resolved "Socket Hang Up" & Startup Crashes**:
  - **Issue**: Incompatible versions of `pydantic` (v1 vs v2) and `pydantic-core` caused segmentation faults in the Python interpreter.
  - **Fix**: Force-reinstalled `pydantic>=2.0` and pinned versions in `requirements.txt` to ensure stability.
- **Robust RAG Initialization**:
  - **Issue**: `chromadb` configuration errors prevented the entire application from starting.
  - **Fix**: Wrapped RAG initialization in a `try-except` block, allowing the core application to run even if the knowledge base is temporarily unavailable.

### 🚀 Automated Deployment System
- **One-Click Server Setup**: Introduced `setup_server.sh` to automate the entire provisioning process:
  - Installs system dependencies (Python 3.12, Node.js 20, Unzip).
  - Unzips deployment artifacts.
  - Sets up the Python virtual environment (`.venv`) and installs dependencies.
  - Prepares the `.env` configuration template.
- **Cross-Platform Compatibility**:
  - Resolved path issues where Windows-generated `venv` and `node_modules` folders caused Linux execution failures.
  - Implemented logic to rebuild these environments natively on the production server.

### 🌍 Production Configuration
- **External Access**: Configured the Frontend to bind to `0.0.0.0` (instead of `localhost`), enabling secure external access to the application.
- **Process Management**: Cleared legacy zombie processes (`pm2`) to ensure a clean startup state for the new deployment.

---

## 9. Recent Updates (Feb 15, 2026) - Langfuse Integration & Critical Compatibility

### 🛠️ Langfuse Self-Hosted Infrastructure (Docker)
To establish a self-hosted observability stack without external dependencies, we deployed Langfuse locally.
- **Docker Compose Architecture**:
    - **Path**: `langfuse/docker-compose.yml`
    - **Services**:
        - `langfuse-server`: Core application (Exposed on port 3333).
        - `langfuse-db`: PostgreSQL database for persistent trace storage (v16).
    - **Configuration**:
        - `langfuse/.env` manages sensitive secrets (`DATABASE_URL`, `NEXTAUTH_SECRET`, `SALT`).
- **Integration**:
    - The backend was configured to send asynchronous traces to `http://localhost:3333` using the `langfuse` Python SDK.

### 🚨 CRITICAL ISSUE: Python 3.14 Incompatibility
A major stability issue was identified during the integration process.

#### **The Diagnostic**
- **Symptoms**: The backend crashed silently ("Socket Hang Up") or failed with `AttributeError: 'Langfuse' object has no attribute 'trace'`.
- **Root Cause**:
    - The project runs on **Python 3.14 (Preview)**.
    - `Langfuse` SDK relies on **Pydantic V1**.
    - **Incompatibility**: Pydantic V1 fails to initialize correctly on Python 3.14, preventing the creation of Trace objects. This is a known upstream issue with the preview runtime.

#### **Resolution & Mitigation**
1.  **Conditional Logic**: Modified `backend/main.py` to wrap Langfuse initialization in a guard block controlled by `ENABLE_LANGFUSE`.
2.  **Environment Control**: Introduced `ENABLE_LANGFUSE=false` in `.env`.
3.  **Result**: Successfully bypassed the crashing code path, restoring full Chatbot functionality while keeping the infrastructure ready for the fix.

### 🔮 Future Plan: Python Downgrade
To enable the observability features, the runtime environment must be standardized.
- **Plan**: Downgrade from Python 3.14 to **Python 3.12 (Stable)**.
- **Status**: Completed (Python 3.12.9 environment setup and dependencies reinstalled).

### ✅ Langfuse Re-enabled
- **Action**: Reinstalled `requirements.txt` in Python 3.12 environment and set `ENABLE_LANGFUSE` to `true` in `.env`.
- **Result**: Stable Langfuse tracing functionality restored.

---

## 10. Langfuse Final Stabilization & Data Persistence (Feb 15 - 16)

We have resolved the final issues regarding data loss and detailed trace capture after enabling the tracing function.

### 💾 Data Persistence
- **Issue**: API keys and configurations were reset upon container restart due to the use of Docker virtual volumes.
- **Resolution**: Modified `docker-compose.yml` to use **Bind Mounts** (`./db_data`), linking the database directly to a host directory.
- **Result**: All trace records and project settings are now permanently preserved across server restarts.

### 🧩 SDK Version & Data Ingestion Fix
- **Issue**: Protocol mismatch between Langfuse Server (v2.95) and Python SDK (v3.x) caused data to be recorded as `null` or failed transmission.
- **Resolution**:
    1.  **SDK Downgrade**: Pinned Python SDK to v2.60 series to ensure compatibility with the server.
    2.  **Trace Level Handler**: Switched to v2-style `CallbackHandler(stateful_client=trace)` instead of the v3-only `as_langchain_handler`.
    3.  **Explicit Flush**: Implemented `langfuse.flush()` immediately after response generation to guarantee 100% data transmission in async environments.
- **Result**: Input/Output chat history is now correctly recorded in the Langfuse dashboard.

### 📝 Explicit Data Capture
- **Issue**: Due to LangChain's internal structure, User Input and AI Output were buried within internal Steps rather than being visible at the top Trace level.
- **Resolution**:
    1.  Explicitly set `input=request.message` during `trace()` creation.
    2.  Used `as_stateful_client=False` in `CallbackHandler` to prevent overwriting significantly.
    3.  Called `trace.update(output=response_text)` to explicitly update the final result.
- **Effect**: Conversation content and results are immediately visible in the Langfuse UI list and detail views.

### 🛑 Resolving LangChain "Dependency Hell" (ImportError)
- **Symptom**: `ImportError: cannot import name 'ContextOverflowError'` and `AzureChatOpenAI` module load failures caused backend crashes.
- **Cause**: While `langchain` main package was downgraded to 0.2.16, derivative packages like `langchain-openai` and `langchain-google-genai` were still on 0.3.x, causing `langchain-core` version conflicts.
- **Resolution**:
    - `langchain==0.2.16`
    - `langchain-community==0.2.16`
    - `langchain-openai<0.2.0` (0.1.x)
    - `langchain-google-genai<2.0.0` (1.x)
    - Downgraded the entire ecosystem to the 0.2.x compatible range.
- **Result**: `ImportError` completely resolved, server starts normally.

---

## 11. Configuration Reference

This section documents the key configuration values for the self-hosted Langfuse environment and monitoring system.

### 🐳 Docker Compose Configuration (`langfuse_infra/docker-compose.yml`)
The Langfuse server and Postgres database are managed via `docker-compose`.

#### 1. Langfuse Server (`langfuse-server`)
- **Image**: `langfuse/langfuse:2` (Using stable v2 tag)
- **Port Mapping**: `3333:3000` (Access via host port 3333)
- **Environment Variables**:
  - `NODE_ENV`: `production`
  - `DATABASE_URL`: `postgresql://postgres:postgres@db:5432/postgres` (Internal Docker Network)
  - `NEXTAUTH_URL`: `http://localhost:3333`
  - Security Keys (See `.env`): `NEXTAUTH_SECRET`, `SALT`, `ENCRYPTION_KEY`
- **Health Check**: Monitors `/api/health` on port 3000.

#### 2. PostgreSQL Database (`db`)
- **Image**: `postgres:16`
- **Port Mapping**: `5432:5432` (Allows local access)
- **Volumes (Persistence)**:
  - `./db_data:/var/lib/postgresql/data` (Bind Mount used)
  - **Important**: Using host directory instead of Docker Volume guarantees data persistence even if containers are recreated.
- **Default Credentials**:
  - User: `postgres`
  - Password: `postgres`
  - DB: `postgres`

### 🔌 Backend Langfuse Integration

#### 1. Environment Variables (`.env`)
```bash
# Enable Langfuse
ENABLE_LANGFUSE=true

# Langfuse Auth (Local Docker)
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=http://localhost:3333

# Database Connection String (If needed)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
```

#### 2. Python SDK Initialization (`backend/main.py`)
- **Version Pinning**: `langfuse>=2.0.0` (v2 compatibility)
- **Handler Setup**:
  ```python
  from langfuse.callback import CallbackHandler
  
  # Disable stateful client to prevent input overwrite
  trace = langfuse.trace(name=..., input=...)
  handler = CallbackHandler(stateful_client=trace)
  ```
- **Flush Strategy**: Must call `langfuse.flush()` after request completion to avoid async data loss.
