# 🛠️ 03. Step-by-Step Installation History
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> 🌐 **Language / 언어 전환**: [English](./03_installation_history_EN.md) | [한국어](./03_installation_history.md)

---

## 🔗 Navigation
- [01. System Overview](./01_system_overview_EN.md)
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- **[03. Step-by-Step Installation History](./03_installation_history_EN.md)**
- [04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)
- [05. Detailed Workflows](./05_detailed_workflows_EN.md)
- [06. Security & Infrastructure Tuning](./06_security_and_tuning_EN.md)
- [07. Operations & Deployment Guide](./07_operations_and_deployment_EN.md)
- [14. eBPF Cilium & AI Firewall + Telegram SOC](./14_ebpf_cilium_ai_firewall_and_telegram_soc_EN.md)

---

## 1. Overview

The initial deployment of this platform was achieved across five sequential phases, bringing lightweight Kubernetes infrastructure, deep learning backends, conversational bots, and observability portals to life on an on-premise edge node.

---

## 2. Phase-by-Phase Installation Breakdown

### 📌 Step 1: Lightweight Kubernetes (K3s) Cluster Provisioning
1. **Ubuntu 26 LTS Preparation & K3s Setup**:
   - Single-node K3s cluster installed with native `containerd` runtime:
   ```bash
   curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
   export KUBECONFIG=~/.kube/config
   ```
2. **K3s Node Health Verification**:
   ```bash
   kubectl get nodes
   ```

---

### 📌 Step 2: Edge AI Engine Microservice Build & Rollout
1. **FastAPI Inference Core**:
   - Integrated Tesseract v5 and Python bindings (`pytesseract`) for on-premise OCR.
   - Built neural machine translation pipelines and Whisper-based STT audio decoders.
2. **Private Container Ingestion**:
   - Built images locally and imported them directly into K3s containerd without external registry pushes:
   ```bash
   cd ~/edge-ai-engine
   docker build -t edge-ai-engine:latest .
   docker save edge-ai-engine:latest | sudo k3s ctr images import -
   ```
3. **K8s Deployment and ClusterIP Manifests**:
   - Created `edge-ai-engine-service` exposing Port 8000 internally:
   ```bash
   kubectl apply -f deployment.yaml
   ```

---

### 📌 Step 3: Asynchronous Telegram Bot Gateway
1. **Async Gateway Client**:
   - Python 3.11 with `aiogram` listening for text, image, and audio messages.
2. **Secret Management**:
   ```bash
   kubectl create secret generic telegram-bot-secret --from-literal=token="<YOUR_TELEGRAM_BOT_TOKEN>"
   ```
3. **Bot Deployment**:
   - Configured internal routing to `http://edge-ai-engine-service:80/api/v1/process`:
   ```bash
   cd ~/telegram-bot
   kubectl apply -f deployment.yaml
   ```

---

### 📌 Step 4: Web Administration Portal
1. **Real-time Observability UI**:
   - Built FastAPI backend with JWT session security, telemetry polling at `/api/v1/telemetry`, and Vanilla JS dashboard.
2. **Ingress Ingress Controller Exposure**:
   - Traefik Ingress resource routing HTTP port 80 traffic to `web-dashboard-service`.
   ```bash
   cd ~/web-dashboard
   kubectl apply -f deployment.yaml
   ```

---

### 📌 Step 5: End-to-End Baseline Verification
- Verified bidirectional Telegram communications: audio, image, and text messages accurately translated to Korean.
- Logged into the Web Dashboard at `http://<EDGE_NODE_IP>` to confirm node telemetry streaming.
