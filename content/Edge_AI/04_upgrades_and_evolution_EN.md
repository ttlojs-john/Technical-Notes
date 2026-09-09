# 🚀 04. Post-Setup Upgrades & System Evolution
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> [!TIP]
> 🌐 **Language Selector**: **[🇰🇷 한국어 버전으로 전환 (Switch to Korean)](./04_upgrades_and_evolution.md)** | **[🇺🇸 English (Current Document)](./04_upgrades_and_evolution_EN.md)**

---

## 🔗 Navigation
- [01. System Overview](./01_system_overview_EN.md)
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- [03. Installation History](./03_installation_history_EN.md)
- **[04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)**
- [05. Detailed Workflows](./05_detailed_workflows_EN.md)
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

## 1. Evolution Overview

Following baseline deployment, 8 major system upgrades were rolled out to elevate OCR precision, autonomy, memory utilization, and zero-trust perimeter defense.

```mermaid
flowchart TD
    subgraph Timeline ["🚀 Edge AI System Evolutionary Milestones"]
        Step0["<b>Initial Release</b><br/>K3s Cluster baseline with 3 primary microservices"]
        Step1["<b>Upgrade 1</b><br/>RapidOCR (ONNX) & CTranslate2 INT8 deep learning engines"]
        Step0 --> Step1
        Step2["<b>Upgrade 2</b><br/>Multimodal VLM One-Shot (GPT-4o-mini) & Telegram mode switcher"]
        Step1 --> Step2
        Step3["<b>Upgrade 3</b><br/>Edge-TTS / gTTS neural audio synthesis & voice dispatch"]
        Step2 --> Step3
        Step4["<b>Upgrade 4</b><br/>token_audit_logs.json atomic HostPath distributed storage"]
        Step3 --> Step4
        Step5["<b>Upgrade 5</b><br/>In-Cluster K9s Web Terminal & Custom Glossary Manager"]
        Step4 --> Step5
        Step6["<b>Upgrade 6</b><br/>16 vCPU & 60GB RAM OS Kernel & Memory optimization"]
        Step5 --> Step6
        Step7["<b>Upgrade 7</b><br/>Fail2ban SSH defense & Direct IP Scanner blocking firewall"]
        Step6 --> Step7
        Step8["<b>Upgrade 8</b><br/>apply_all.sh automated CI/CD build and rollout pipeline"]
        Step7 --> Step8
    end
```

---

## 2. The 8 Major Upgrades Breakdown

### 🚀 Upgrade 1: RapidOCR (ONNX) & CTranslate2 (INT8)
- **Background**: Replaced legacy Tesseract and Python translators to address OCR inaccuracies and translation latencies.
- **Implementation**:
  - `rapidocr_onnxruntime`: Leverages DBNet text detection and CRNN character recognition, pushing OCR accuracy beyond 99% for Latin scripts.
  - `ctranslate2`: Quantized INT8 NLLB neural translation executes 4x faster on local CPU memory.

### 🚀 Upgrade 2: Multimodal VLM Hybrid Routing (GPT-4o-mini)
- **Background**: Traditional OCR extracts isolated text, missing holistic situational context on signs, complex documents, or receipts.
- **Implementation**:
  - **Local OCR Engine**: Rapid, direct word-by-word extraction and translation.
  - **VLM Vision Hybrid**: Delegates visual interpretation to cloud LLMs with markdown scene summaries.
  - Toggled dynamically through Telegram inline button keyboards.

### 🚀 Upgrade 3: Real-Time Neural Speech Synthesis (Edge-TTS / gTTS)
- **Implementation**:
  - Integrated Microsoft Edge neural voice models into the inference backend.
  - Automatically synthesizes translated output into `.mp3`/`.ogg` audio files and delivers them as native voice messages.

### 🚀 Upgrade 4: Atomic HostPath Distributed Token Storage
- **Background**: Multiple `edge-ai-engine` Pod replicas caused token counter divergence across isolated container memory.
- **Implementation**:
  - Mounted `token_audit_logs.json` via Kubernetes `hostPath` with file locking to guarantee transactional atomic logging.

### 🚀 Upgrade 5: In-Cluster K9s Web Admin & Glossary Customization
- **Implementation**:
  - **K9s Web Console**: Authenticated RBAC access to view Pod health, tail container logs, and trigger rolling restarts.
  - **Glossary UI**: Direct GUI editing of `glossary.json` enforcing pre-translation regex substitution for specialized terminology.

### 🚀 Upgrade 6: 16 vCPU & 60GB RAM OS Kernel Optimization
- **Implementation**:
  - Configured kernel swappiness to 10 (`vm.swappiness = 10`) to prefer RAM caching and scaled socket queues (`net.core.somaxconn = 4096`).

### 🚀 Upgrade 7: Fail2ban SSH Protection & Direct IP Block Firewall
- **Implementation**:
  - Automatically isolates host SSH port brute-force scanners for 24 hours after 5 failures.
  - Web dashboard drops direct IP requests (`BLOCK_DIRECT_IP="true"`), requiring valid domain headers.

### 🚀 Upgrade 8: One-Click CI/CD Rollout Automation (`apply_all.sh`)
- Builds all three microservices locally and rolls out updated images to K3s within seconds.
