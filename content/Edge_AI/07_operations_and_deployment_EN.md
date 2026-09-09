# ⚙️ 07. Operations, Verification Testing, & Deployment Playbook
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> [!TIP]
> 🌐 **Language Selector**: **[🇰🇷 한국어 버전으로 전환 (Switch to Korean)](./07_operations_and_deployment.md)** | **[🇺🇸 English (Current Document)](./07_operations_and_deployment_EN.md)**

---

## 🔗 Navigation
- [01. System Overview](./01_system_overview_EN.md)
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- [03. Installation History](./03_installation_history_EN.md)
- [04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)
- [05. Detailed Workflows](./05_detailed_workflows_EN.md)
- [06. Security & Tuning](./06_security_and_tuning_EN.md)
- **[07. Operations & Deployment](./07_operations_and_deployment_EN.md)**
- [08. K9s AI Engine Monitoring](./08_k9s_ai_engine_and_workload_monitoring_EN.md)
- [09. MLOps Multi-Engine Benchmark](./09_mlops_multi_engine_architecture_and_benchmark_EN.md)
- [10. Smart Text Chunking & Splitter](./10_smart_text_chunking_and_message_splitter_EN.md)
- [11. External AI (Gemini) Integration](./11_external_ai_gemini_integration_and_admin_console_EN.md)
- [12. Host OS Firewall & IPS](./12_host_os_firewall_and_intrusion_prevention_guide_EN.md)
- [13. Hardware Scale-Up (32C/192GB/GPU)](./13_hardware_scaleup_32core_192gb_gpu_optimization_EN.md)
- [14. eBPF Cilium & AI Firewall + Telegram SOC](./14_ebpf_cilium_ai_firewall_and_telegram_soc_EN.md)

---

## 1. Zero-Downtime Rollout Pipeline (`apply_all.sh`)

Deploy application updates and configuration revisions across the K3s cluster using the unified automated build script:

```bash
#!/usr/bin/env bash
# ~/apply_all.sh
set -e

# 1. Build & Import Edge AI Engine into K3s containerd
cd ~/edge-ai-engine
docker build -t edge-ai-engine:latest .
docker save edge-ai-engine:latest | sudo k3s ctr images import -

# 2. Build & Import Web Dashboard
cd ~/web-dashboard
docker build -t web-dashboard:latest .
docker save web-dashboard:latest | sudo k3s ctr images import -

# 3. Build & Import Telegram Bot Gateway
cd ~/telegram-bot
docker build -t telegram-bot:latest .
docker save telegram-bot:latest | sudo k3s ctr images import -

# 4. Apply K8s Manifests and Trigger Rolling Restarts
kubectl apply -f ~/web-dashboard/deployment.yaml
kubectl rollout restart deployment/edge-ai-engine
kubectl rollout restart deployment/web-dashboard
kubectl rollout restart deployment/telegram-bot

# Verify Workload States
kubectl get pods -o wide
```

Execution:
```bash
chmod +x ~/apply_all.sh
~/apply_all.sh
```

---

## 2. Day-2 Operations via Web Dashboard

Administrators oversee production workloads and terminology maps through the centralized management console:

![Web Admin Dashboard UI](/images/web_dashboard.jpg)
*▲ [Figure] Web Administration Portal Interface*

- **Real-Time Pod Management**: Monitor CPU/RAM consumption and trigger one-click Pod deletions/restarts.
- **Glossary Management**: Register and update regex terminology mappings live without restarting services.
- **Token Analytics**: Audit cumulative LLM token consumption patterns.

---

## 3. Post-Deployment Verification Suite

Run automated diagnostics to ensure pipeline health after rolling out updates:

### 3.1 Edge AI Pipeline Smoke Tests (`test_all_features.py`)
```bash
python3 ~/edge-ai-engine/test_all_features.py
```
Validates OCR extraction, neural translation, STT/TTS modules, and cluster health.

### 3.2 Distributed Storage Concurrency Verification (`test_token_logs.py`)
```bash
python3 ~/edge-ai-engine/test_token_logs.py
```
Validates atomic file write operations under parallel request load.

### 3.3 Audio Voice Synthesis Validation (`test_tts.py`)
```bash
python3 ~/edge-ai-engine/test_tts.py
```
Validates Edge-TTS pipeline encoding and OGG audio generation.

---

## 4. Incident Response & Troubleshooting Playbook

### 🚨 Scenario 1: Telegram Bot Unresponsive
1. Inspect Pod operational state and tail logs:
   ```bash
   kubectl get pods -l app=telegram-bot
   kubectl logs -f deployment/telegram-bot --tail=100
   ```
2. Verify egress connectivity to Telegram's cloud API:
   ```bash
   kubectl exec -it deployment/telegram-bot -- ping api.telegram.org
   ```

### 🚨 Scenario 2: Web Dashboard 403 Forbidden
- **Root Cause**: `BLOCK_DIRECT_IP="true"` drops HTTP traffic when not addressed to the authorized domain (`edgeai.local`).
- **Remediation**: Append `edgeai.local` to `/etc/hosts` pointing to the Edge node IP, or temporarily set `BLOCK_DIRECT_IP="false"` in `deployment.yaml`.

### 🚨 Scenario 3: Administrative SSH Lockout
- **Root Cause**: Client IP isolated by Fail2ban following 5 failed credential attempts.
- **Remediation**: Execute unban command from the physical console or an internal management terminal:
   ```bash
   sudo fail2ban-client set sshd unbanip <BLOCKED_CLIENT_IP>
   ```
