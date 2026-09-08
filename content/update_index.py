#!/usr/bin/env python3
"""
Advanced Bilingual Index Generator for Technical-Notes (Quartz Digital Garden)
Generates:
1. index.md: Korean-dedicated catalog with quick toggle to English.
2. index_EN.md: English-dedicated catalog with quick toggle to Korean.
"""
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).parent.resolve()

EXCLUDE_DIRS = {
    '.git', '.github', 'images', 'archive', 'scratch', 'node_modules', 
    '.gemini', '.antigravity', 'static', 'assets'
}

def extract_metadata(filepath: Path):
    """Extracts H1 title and description from a markdown file."""
    title = ""
    description = ""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line in lines:
            line_str = line.strip()
            if not title and line_str.startswith('# '):
                title = line_str[2:].strip()
            elif not description and (line_str.startswith('> **') or line_str.startswith('> _')):
                description = line_str.strip('> * _').strip()
            elif not description and line_str and not line_str.startswith('#') and not line_str.startswith('!['):
                description = line_str[:120] + '...' if len(line_str) > 120 else line_str
                
            if title and description:
                break
    except Exception as e:
        pass
        
    if not title:
        title = filepath.stem
    return title, description

def scan_repository():
    """Scans all folders and groups markdown files into KR and EN collections."""
    categories = {}
    
    for item in sorted(os.listdir(ROOT_DIR)):
        folder_path = ROOT_DIR / item
        if not folder_path.is_dir() or item in EXCLUDE_DIRS or item.startswith('.'):
            continue
            
        md_files = [f for f in folder_path.glob("*.md") if not f.name.endswith(".metadata.json")]
        if not md_files:
            continue
            
        kr_docs = []
        en_docs = []
        
        for f in sorted(md_files):
            stem = f.stem
            title, desc = extract_metadata(f)
            
            # Check if this is an English or Korean document
            if stem.endswith("_EN"):
                en_docs.append({
                    "file": f,
                    "stem": stem,
                    "folder": item,
                    "title": title,
                    "desc": desc
                })
            elif stem.endswith("_KR"):
                kr_docs.append({
                    "file": f,
                    "stem": stem,
                    "folder": item,
                    "title": title,
                    "desc": desc
                })
            else:
                # Default documents
                # If name has English keywords or English title
                if "EN" in stem or stem.startswith("openclaw_Test") or "guide" in stem.lower():
                    # Check companion
                    companion_kr = folder_path / f"{stem}_KR.md"
                    if companion_kr.exists():
                        en_docs.append({"file": f, "stem": stem, "folder": item, "title": title, "desc": desc})
                    else:
                        kr_docs.append({"file": f, "stem": stem, "folder": item, "title": title, "desc": desc})
                else:
                    kr_docs.append({"file": f, "stem": stem, "folder": item, "title": title, "desc": desc})
                    
        categories[item] = {
            "KR": kr_docs,
            "EN": en_docs
        }
        
    return categories

CATEGORY_META_KR = {
    "Edge_AI": ("🤖 엣지 AI & 인클러스터 딥러닝 (Edge AI)", "K3s 클러스터 기반 멀티모달 딥러닝 파이프라인 및 eBPF 방화벽 SOC 관제"),
    "Openclaw": ("🧠 자율형 AI 에이전트 (OpenClaw)", "일회용 브라우저 샌드박스 및 인간 참여형(HIL) 제로트러스트 에이전트 시스템"),
    "LangCain": ("🔗 랭체인 & LLM 오케스트레이션 (LangChain)", "Next.js + FastAPI 기반 멀티모달 AI 에이전트 및 고가용성 폴백 아키텍처"),
    "Personal Website": ("🌐 데브옵스 & 디지털 가든 (chaeyul.uk)", "Quartz 디지털 가든 인프라, Grafana & Prometheus 모니터링 시스템 구축"),
    "Excel_Analyzer": ("📊 업무 자동화: 엑셀 데이터 분석기", "ITSM 티켓 데이터 집계, 작업자별 처리 시간 분석 및 반복 장애 추출 도구"),
    "PDF_APPS": ("📄 보안 유틸리티: PDF 프로 보안 편집기", "PyMuPDF 기반 개인정보 영구 파기 마스킹 및 한글 텍스트 박스 편집 데스크톱 앱"),
    "Self-study German": ("🇩🇪 웹앱: 독일어 학습 플랫폼", "글래스모피즘 UI, Web Speech TTS, 인터랙티브 퀴즈 기반 어학 학습 시스템")
}

CATEGORY_META_EN = {
    "Edge_AI": ("🤖 Edge AI & In-Cluster Deep Learning", "On-premise K3s cluster running multimodal AI pipelines and eBPF cyber defense."),
    "Openclaw": ("🧠 Autonomous AI Agents (OpenClaw)", "Zero-trust autonomous agent ecosystem with disposable browser sandbox and Human-in-the-Loop governance."),
    "LangCain": ("🔗 LangChain & LLM Orchestration", "Next.js + FastAPI enterprise AI agent integration, multimodal fallback pipelines, and PM2 production operations."),
    "Personal Website": ("🌐 DevOps, Infrastructure & Digital Garden", "chaeyul.uk digital garden architecture, Grafana & Prometheus monitoring, and reverse-proxy hardening."),
    "Excel_Analyzer": ("📊 Automation: Excel Data Task Analyzer", "Automated ticketing analysis, resolution metrics calculation, and repetitive issue clustering desktop tool."),
    "PDF_APPS": ("📄 Security: PDF Pro Redaction Editor", "PyMuPDF desktop utility performing true structural PII byte-purging and localized text annotations."),
    "Self-study German": ("🇩🇪 Web App: Self-Study German Platform", "Glassmorphism UI language learning application with Web Speech API integration and static hosting.")
}

def build_korean_index(categories):
    lines = [
        "![Intro Image](./ai_infra_bridge.jpg)",
        "",
        "# 🚀 인프라 엔지니어에서 AI 혁신가로 (Infra Veteran ➔ AI Innovator)",
        "",
        "> [!TIP]",
        "> 🌐 **Language / 언어 선택**: **[🇰🇷 한국어 (현재 페이지)]** | **[🇺🇸 Switch to English (영문 전용 메인으로 이동)](./index_EN.md)**",
        "",
        '> **"엔터프라이즈 인프라의 견고한 기반 위에 차세대 AI 혁신의 지평을 엽니다."**',
        "> 본 디지털 가든은 17년 이상의 글로벌 데이터센터 및 인프라 운영 전문성(CDCP 인증)을 바탕으로, 실무 중심의 AI 통합 및 시스템 자동화 여정을 기록한 기술 지식 저장소입니다.",
        "",
        "<br>",
        "",
        "## 🛠️ 핵심 역량 (Core Competencies)",
        "![IT Infrastructure](https://img.shields.io/badge/IT_Infrastructure-005A9C?style=for-the-badge&logo=server&logoColor=white)",
        "![Kubernetes & K3s](https://img.shields.io/badge/Kubernetes_&_K3s-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)",
        "![AI Agents & MLOps](https://img.shields.io/badge/AI_&_MLOps-FF9900?style=for-the-badge&logo=openai&logoColor=white)",
        "![eBPF & Security](https://img.shields.io/badge/eBPF_&_ZeroTrust-1389FD?style=for-the-badge&logo=linux&logoColor=white)",
        "![System Automation](https://img.shields.io/badge/System_Automation-3776AB?style=for-the-badge&logo=python&logoColor=white)",
        "",
        "---",
        "",
        "## 🔍 주요 하이라이트 (Quick Highlights)",
        "| 분야 | 핵심 마일스톤 | 바로가기 |",
        "| :--- | :--- | :--- |",
        "| **Edge AI & eBPF SOC** | 32코어/192GB 스케일업, eBPF Cilium/Hubble 방화벽 & 텔레그램 SOC 관제 구축 | [[Edge_AI/14_ebpf_cilium_ai_firewall_and_telegram_soc|방화벽 & 텔레그램 관제 보고서]] |",
        "| **AI Agent R&D** | OpenClaw 멀티에이전트 아키텍처, HIL 승인 체계, 일회용 브라우저 샌드박스 | [[Openclaw/openclaw_Test_KR|OpenClaw 아키텍처 가이드]] |",
        "| **DevOps & 웹 인프라** | Quartz 기술 블로그 배포, Prometheus & Grafana 실시간 관측 스택 구축 | [[Personal Website/05_Final_Completion_Report_KR|인프라 최종 완료 보고서]] |",
        "| **업무 자동화 & 도구** | ITSM 티켓 자동 분석 툴 & PyMuPDF 개인정보 영구 파기 보안 편집기 | [[Excel_Analyzer/Project_Completion_Report_KR|엑셀 분석기]] · [[PDF_APPS/Project_Completion_Report_KR|PDF 보안 편집기]] |",
        "",
        "---",
        "",
        "## 📂 기술 문서 카탈로그 (한국어 전용 목록)",
        ""
    ]
    
    for folder, data in sorted(categories.items()):
        title, desc = CATEGORY_META_KR.get(folder, (f"📁 {folder}", "기술 구현 및 아키텍처 문서"))
        kr_docs = data["KR"]
        if not kr_docs:
            continue
            
        lines.append(f"### {title}")
        lines.append(f"> {desc}")
        lines.append("")
        
        for doc in kr_docs:
            clean_title = doc["title"].replace("[최종 완료 보고서]", "").strip()
            link_path = f"{folder}/{doc['stem']}"
            lines.append(f"* [[{link_path}|{clean_title}]]")
            if doc["desc"] and not doc["desc"].startswith("#"):
                lines.append(f"  - *{doc['desc']}*")
                
        lines.append("")
        
    lines.extend([
        "---",
        "",
        "## 🗂️ 프로젝트 폴더 안내 (Folder Directory)",
        ""
    ])
    
    for folder in sorted(categories.keys()):
        title, desc = CATEGORY_META_KR.get(folder, (folder, "기술 문서"))
        lines.append(f"- **{folder}/** → {desc}")
        
    lines.extend([
        "",
        "<br>",
        "",
        '<div align="center">',
        '  <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fdoc.chaeyul.uk&label=Total%20Views&labelColor=%23555555&countColor=%23005a9c&style=flat" alt="Views" />',
        "</div>",
        ""
    ])
    
    return "\n".join(lines)

def build_english_index(categories):
    lines = [
        "![Intro Image](./ai_infra_bridge.jpg)",
        "",
        "# 🚀 Infra Veteran ➔ AI Innovator",
        "",
        "> [!TIP]",
        "> 🌐 **Language Selector**: **[🇰🇷 한국어 버전으로 이동 (Switch to Korean)](./index.md)** | **[🇺🇸 English (Current Page)]**",
        "",
        '> **"Building the new frontier of AI innovation upon the solid foundation of enterprise infrastructure."**',
        "> This digital garden documents my journey in practical AI integration and system automation, viewed through the lens of a CDCP-certified global data center and infrastructure operations expert with over 17 years of experience.",
        "",
        "<br>",
        "",
        "## 🛠️ Core Competencies",
        "![IT Infrastructure](https://img.shields.io/badge/IT_Infrastructure-005A9C?style=for-the-badge&logo=server&logoColor=white)",
        "![Kubernetes & K3s](https://img.shields.io/badge/Kubernetes_&_K3s-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)",
        "![AI Agents & MLOps](https://img.shields.io/badge/AI_&_MLOps-FF9900?style=for-the-badge&logo=openai&logoColor=white)",
        "![eBPF & Security](https://img.shields.io/badge/eBPF_&_ZeroTrust-1389FD?style=for-the-badge&logo=linux&logoColor=white)",
        "![System Automation](https://img.shields.io/badge/System_Automation-3776AB?style=for-the-badge&logo=python&logoColor=white)",
        "",
        "---",
        "",
        "## 🔍 Quick Highlights",
        "| Core Domain | Key Operational Milestone | Direct Link |",
        "| :--- | :--- | :--- |",
        "| **Edge AI & eBPF SOC** | K3s 32C/192GB Scale-up, eBPF Cilium/Hubble L3-L7 Firewall & Telegram SOC | [[Edge_AI/14_ebpf_cilium_ai_firewall_and_telegram_soc_EN|Security SOC Report]] |",
        "| **AI Agent R&D** | OpenClaw Multi-Agent Architecture with HIL Approvals & Disposable Browser Sandbox | [[Openclaw/openclaw_Test|OpenClaw Architecture Guide]] |",
        "| **DevOps & Digital Garden** | Quartz Digital Garden with Prometheus & Grafana Monitoring Stack | [[Personal Website/05_Final_Completion_Report_EN|Final Completion Report]] |",
        "| **Automation & Tooling** | High-speed Excel Data Analyzer & PyMuPDF Security Redaction Desktop App | [[Excel_Analyzer/Project_Completion_Report_EN|Excel Analyzer]] · [[PDF_APPS/Project_Completion_Report_EN|PDF Utility]] |",
        "",
        "---",
        "",
        "## 📂 Technical Notes & Knowledge Catalog (English)",
        ""
    ]
    
    for folder, data in sorted(categories.items()):
        title, desc = CATEGORY_META_EN.get(folder, (f"📁 {folder}", "Technical Documentation"))
        en_docs = data["EN"]
        if not en_docs:
            continue
            
        lines.append(f"### {title}")
        lines.append(f"> {desc}")
        lines.append("")
        
        for doc in en_docs:
            clean_title = doc["title"].replace("[최종 완료 보고서]", "").strip()
            link_path = f"{folder}/{doc['stem']}"
            lines.append(f"* [[{link_path}|{clean_title}]]")
            if doc["desc"] and not doc["desc"].startswith("#"):
                lines.append(f"  - *{doc['desc']}*")
                
        lines.append("")
        
    lines.extend([
        "---",
        "",
        "## 🗂️ Workspace Directory Overview",
        ""
    ])
    
    for folder in sorted(categories.keys()):
        title, desc = CATEGORY_META_EN.get(folder, (folder, "Technical Documentation"))
        lines.append(f"- **{folder}/** → {desc}")
        
    lines.extend([
        "",
        "<br>",
        "",
        '<div align="center">',
        '  <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fdoc.chaeyul.uk&label=Total%20Views&labelColor=%23555555&countColor=%23005a9c&style=flat" alt="Views" />',
        "</div>",
        ""
    ])
    
    return "\n".join(lines)

def main():
    print("🔍 Scanning Technical-Notes for bilingual separation...")
    categories = scan_repository()
    
    kr_index = build_korean_index(categories)
    (ROOT_DIR / "index.md").write_text(kr_index, encoding="utf-8")
    print("✅ Successfully generated Korean index.md!")
    
    en_index = build_english_index(categories)
    (ROOT_DIR / "index_EN.md").write_text(en_index, encoding="utf-8")
    print("✅ Successfully generated English index_EN.md!")

if __name__ == "__main__":
    main()
