# ⚙️ 05. Detailed Component Workflows & Data Flow Diagrams
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> [!TIP]
> 🌐 **Language Selector**: **[🇰🇷 한국어 버전으로 전환 (Switch to Korean)](./05_detailed_workflows.md)** | **[🇺🇸 English (Current Document)](./05_detailed_workflows_EN.md)**

---

## 🔗 Navigation
- [01. System Overview](./01_system_overview_EN.md)
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- [03. Installation History](./03_installation_history_EN.md)
- [04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)
- **[05. Detailed Workflows](./05_detailed_workflows_EN.md)**
- [06. Security & Tuning](./06_security_and_tuning_EN.md)
- [07. Operations & Deployment](./07_operations_and_deployment_EN.md)
- [08. K9s AI Engine Monitoring](./08_k9s_ai_engine_and_workload_monitoring_EN.md)
- [09. MLOps Multi-Engine Benchmark](./09_mlops_multi_engine_architecture_and_benchmark_EN.md)
- [10. Smart Text Chunking & Splitter](./10_smart_text_chunking_and_message_splitter_EN.md)
- [11. External AI (Gemini) Integration](./11_external_ai_gemini_integration_and_admin_console_EN.md)
- [12. Host OS Firewall & IPS](./12_host_os_firewall_and_intrusion_prevention_guide_EN.md)
- [13. Hardware Scale-Up (32C/192GB/GPU)](./13_hardware_scaleup_32core_192gb_gpu_optimization_EN.md)
- [14. eBPF Cilium & AI Firewall + Telegram SOC](./14_ebpf_cilium_ai_firewall_and_telegram_soc_EN.md)

---

## 1. Multimodal Telegram Request Processing Sequence

User payloads delivered through the messaging gateway route dynamically based on mime-type into modular processing pipelines within `edge-ai-engine`:

```mermaid

sequenceDiagram
    autonumber
    actor User as "📱 Telegram User"
    participant Bot as "🤖 telegram-bot Pod"
    participant Engine as "🧠 edge-ai-engine Pod"
    participant Storage as "💾 Shared Storage (hostPath)"
    participant Cloud as "☁️ OpenAI (GPT-4o-mini)"

    User->>Bot: Dispatches Text / Image / Audio
    Bot->>Bot: Evaluate User Session & Mode (RapidOCR vs VLM)

    alt [1] Text Translation
        Bot->>Engine: POST /api/v1/process (type="text", text="...")
        Engine->>Storage: Apply glossary.json regex substitutions
        Engine->>Engine: CTranslate2 local neural translation
        Engine->>Engine: Edge-TTS synthesis to MP3/OGG
        Engine->>Storage: Record token consumption to token_audit_logs.json
        Engine-->>Bot: { text: "...", audio_base64: "..." }
        Bot-->>User: 📝 Translated Text + 🔊 Voice Audio Note

    else [2] Image Message (RapidOCR Mode)
        Bot->>Engine: POST /api/v1/process (type="image", mode="ocr", file=img)
        Engine->>Engine: RapidOCR (ONNX DBNet + CRNN) text extraction
        Engine->>Engine: Noise filtering & local neural translation
        Engine->>Storage: Append token audit
        Engine-->>Bot: { original_text: "...", translated_text: "..." }
        Bot-->>User: 🔍 [Extracted Text] + 🌐 [Korean Translation]

    else [3] Image Message (VLM Direct One-Shot Mode)
        Bot->>Engine: POST /api/v1/process (type="image", mode="vlm", file=img)
        Engine->>Cloud: GPT-4o-mini Vision Multi-Modal Request
        Cloud-->>Engine: Contextual scene analysis & Korean summary
        Engine->>Storage: Record external VLM token usage
        Engine-->>Bot: { vlm_analysis: "..." }
        Bot-->>User: 👁️ [VLM Contextual Scene Explanation]

    else [4] Audio Note (Voice/STT)
        Bot->>Engine: POST /api/v1/process (type="audio", file=voice)
        Engine->>Engine: Whisper STT audio transcription
        Engine->>Engine: Machine translation into Korean
        Engine-->>Bot: { transcript: "...", translation: "..." }
        Bot-->>User: 🎙️ [Speech Transcription] + 🌐 [Korean Translation]
    end
```

---

## 2. In-Cluster K9s Web Console Management Architecture

Controls and metrics collected by the web admin backend traverse in-cluster RBAC boundaries to interact directly with the Kubernetes API server:

```mermaid

flowchart TD
    subgraph Browser ["💻 Web Admin Dashboard GUI"]
        UI_K9s["☸️ K9s Cluster Tab"]
        UI_Logs["📜 Real-time Pod Log Viewer"]
        UI_Action["⚡ One-Click Pod Restart"]
        UI_Glossary["📖 Custom Glossary Editor"]
        UI_Tokens["🪙 Cumulative Token Audit Tab"]
    end

    subgraph DashboardBackend ["Web Dashboard Backend (FastAPI)"]
        K8sClient["Kubernetes Python Client<br/>(In-Cluster Config)"]
        GlossaryMgr["Glossary Storage Manager"]
        TokenViewer["Token Log Aggregator"]
    end

    subgraph K8sRBAC ["Kubernetes Cluster Security (RBAC)"]
        SA["ServiceAccount: web-dashboard-sa"]
        CRB["ClusterRoleBinding: web-dashboard-sa-binding"]
        CR["ClusterRole: web-dashboard-k9s-role<br/>• pods (get, list, watch, delete)<br/>• pods/log, events, nodes<br/>• deployments/scale"]
    end

    subgraph K8sCore ["Kubernetes API & Pods"]
        APIServer["☸️ K8s API Server"]
        Pod_Engine["🧠 Pod: edge-ai-engine-xxxx"]
        Pod_Bot["💬 Pod: telegram-bot-xxxx"]
        Pod_Dash["📊 Pod: web-dashboard-xxxx"]
    end

    UI_K9s -->|"GET /api/v1/k8s/pods"| K8sClient
    UI_Logs -->|"GET /api/v1/k8s/pods/{name}/logs"| K8sClient
    UI_Action -->|"POST /api/v1/k8s/pods/{name}/restart"| K8sClient
    UI_Glossary <-->|"GET / POST / DELETE /api/v1/glossary"| GlossaryMgr
    UI_Tokens -->|"GET /api/v1/tokens/audit"| TokenViewer

    K8sClient --- SA
    SA --- CRB
    CRB --- CR
    CR --> APIServer

    APIServer -.->|Live Log Stream| Pod_Engine
    APIServer -.->|Live Log Stream| Pod_Bot
    APIServer -.->|Restart/Delete Pod| Pod_Engine
```

---

## 3. Persistent Storage Synchronization

Eliminates race conditions between multi-replica inference pods:

```mermaid

flowchart LR
    subgraph Pods ["Edge AI Engine Multi-Pods (replicas: 2)"]
        Pod1["Pod 1<br/>(API Worker 1)"]
        Pod2["Pod 2<br/>(API Worker 2)"]
    end

    subgraph Shared ["Host OS Level Storage"]
        File[("💾 token_audit_logs.json<br/>(Atomic File Write with Lock)")]
    end

    subgraph Dash ["Web Dashboard View"]
        DBB["Dashboard Backend API"]
        DGUI["🪙 Token Audit Tab"]
    end

    Pod1 -->|"1. File Lock / Append"| File
    Pod2 -->|"1. File Lock / Append"| File
    File -.->|2. Real-time Read| DBB
    DBB -.->|3. Render Charts & Logs| DGUI
```

- **Atomic File Locking**: Utilizes POSIX `fcntl` locking to prevent race conditions during high concurrent traffic.
- **Hardware Persistence**: HostPath mounts guarantee log preservation across Pod eviction or restart cycles.
