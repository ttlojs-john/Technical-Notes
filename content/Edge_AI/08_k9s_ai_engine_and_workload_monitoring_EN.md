# 📊 08. K9s Dashboard Real-Time AI Engine & Pod Workload Observability
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> [!TIP]
> 🌐 **Language Selector**: **[🇰🇷 한국어 버전으로 전환 (Switch to Korean)](./08_k9s_ai_engine_and_workload_monitoring.md)** | **[🇺🇸 English (Current Document)](./08_k9s_ai_engine_and_workload_monitoring_EN.md)**

---

## 🔗 Navigation
- [01. System Overview](./01_system_overview_EN.md)
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- [03. Installation History](./03_installation_history_EN.md)
- [04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)
- [05. Detailed Workflows](./05_detailed_workflows_EN.md)
- [06. Security & Tuning](./06_security_and_tuning_EN.md)
- [07. Operations & Deployment](./07_operations_and_deployment_EN.md)
- **[08. K9s AI Engine Monitoring](./08_k9s_ai_engine_and_workload_monitoring_EN.md)**
- [09. MLOps Multi-Engine Benchmark](./09_mlops_multi_engine_architecture_and_benchmark_EN.md)
- [10. Smart Text Chunking & Splitter](./10_smart_text_chunking_and_message_splitter_EN.md)
- [11. External AI (Gemini) Integration](./11_external_ai_gemini_integration_and_admin_console_EN.md)
- [12. Host OS Firewall & IPS](./12_host_os_firewall_and_intrusion_prevention_guide_EN.md)
- [13. Hardware Scale-Up (32C/192GB/GPU)](./13_hardware_scaleup_32core_192gb_gpu_optimization_EN.md)
- [14. eBPF Cilium & AI Firewall + Telegram SOC](./14_ebpf_cilium_ai_firewall_and_telegram_soc_EN.md)

---

## 1. Observability Goals & Architecture Overview

In distributed production environments with multi-replica microservices, administrators require real-time visibility into **which AI engines are active per pod**, **how inference workloads are partitioned**, and **which image version is actively executing**.

The K9s Web Terminal was extended to provide comprehensive operational metadata:

![Kubernetes AI Workload Monitor: Pods & Engines](/images/dashboard_engine_monitor.jpg)
*▲ [Figure] Real-Time Kubernetes Pod & Model Engine Monitoring Console*

---

## 2. Workload & Model Engine Metadata Breakdown

The `K9s Pods & Engine Telemetry` table exposes real-time status across running workloads:

| Workload / Pod Name | Active AI Engines | Responsibilities | Image Tag & Version |
| :--- | :--- | :--- | :--- |
| `edge-ai-engine-xxxx` | **RapidOCR (ONNX)**<br/>**CTranslate2 (INT8)**<br/>**Edge-TTS Pipeline** | In-memory OCR, neural translation, text-to-speech synthesis | `edge-ai-engine:latest`<br/>(Python 3.11 + FastAPI) |
| `telegram-bot-xxxx` | **aiogram v3 Async Poller**<br/>**VLM Mode Switcher** | Telegram gateway, inline button handlers, audio file dispatch | `telegram-bot:latest` |
| `web-dashboard-xxxx` | **In-Cluster RBAC Client**<br/>**Fail2ban / IP Banwall** | Web GUI, pod restarts, security auditing, token analytics | `web-dashboard:latest` |

---

## 3. Real-Time Operations Features
- **Live Pod Restart**: Allows targeted pod restarts during memory leaks or model updates with zero cluster downtime.
- **Log Streaming**: Tunnels stdout/stderr logs from inference workers directly to the browser via WebSocket / Server-Sent Events.
