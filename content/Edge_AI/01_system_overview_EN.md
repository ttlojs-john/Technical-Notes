# 🤖 01. System Overview
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> 🌐 **Language / 언어 전환**: [English](./01_system_overview_EN.md) | [한국어](./01_system_overview.md)

---

## 🔗 Navigation
- **[01. System Overview](./01_system_overview_EN.md)**
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- [03. Installation History](./03_installation_history_EN.md)
- [04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)
- [05. Detailed Workflows](./05_detailed_workflows_EN.md)
- [06. Security & Infrastructure Tuning](./06_security_and_tuning_EN.md)
- [07. Operations & Deployment Guide](./07_operations_and_deployment_EN.md)
- [14. eBPF Cilium & AI Firewall + Telegram SOC](./14_ebpf_cilium_ai_firewall_and_telegram_soc_EN.md)

---

## 1. Overview

This system is a **hybrid Edge AI Telegram bot and Web Admin platform** built on a lightweight Kubernetes (**K3s**) cluster hosted on an **Ubuntu 26 Edge Server**.

It processes diverse media types (text, images, voice) sent by users via Telegram through an on-premise deep learning AI pipeline, delivering real-time Korean translation and contextual scene understanding. Concurrently, administrators can govern cluster resources, manage custom translation glossaries, and monitor security from a unified browser dashboard.

![System Architecture Concept](./images/system_architecture.jpg)
*▲ [Figure] High-level Edge AI Infrastructure and System Topology*

---

## 2. 🌟 Core Values and Objectives

- **Edge-First / Lightweight Prioritized**
  - Offline capable: Local deep learning engines (RapidOCR, CTranslate2, Whisper) deliver low-latency OCR, neural machine translation, and speech-to-text without cloud round trips.
  - Drastically lowers recurring external API expenditure and guarantees continuity during WAN outages.

- **Hybrid VLM Scalability**
  - Goes beyond primitive text extraction: complex imagery like signs, menus, and contextual announcements are dynamically promoted to cloud Vision-Language Models (GPT-4o-mini).

- **Natural Real-Time Voice Synthesis (TTS)**
  - Combines Microsoft Edge-TTS and gTTS pipelines to synthesize localized voice responses (`.mp3`, `.ogg`) returned immediately to the messaging chat.

- **Integrated In-Cluster Observability (Web K9s)**
  - Browser-based terminal management mimicking the CLI `k9s` tool: Pod inspection, live log streaming, one-click restarts, and scaling.
  - Custom glossary UI editor for precise organizational terminology management.

- **Enterprise-Grade Triple-Layer Security**
  - **Host Level**: Fail2ban tracking SSH brute-force patterns with 24-hour IP isolation.
  - **Web Brute-Force Wall**: Automatic permanent IP bans after 3 consecutive login failures.
  - **Direct IP Blocker**: Drops naked IP scanners, enforcing access exclusively through verified domains (`edgeai.local`).
