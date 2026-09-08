#!/usr/bin/env bash
"""
Automatic Index Generator for Technical-Notes (Quartz Digital Garden)
Scans all markdown documents, detects bilingual (KR/EN) pairs,
and updates index.md dynamically with rich Quartz wikilinks.
"""
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Directories to exclude from indexing
EXCLUDE_DIRS = {
    '.git', '.github', 'images', 'archive', 'scratch', 'node_modules', 
    '.gemini', '.antigravity', 'static', 'assets'
}

ROOT_DIR = Path(__file__).parent.resolve()

def extract_metadata(filepath: Path):
    """Extracts H1 title and brief description from a markdown file."""
    title = ""
    description = ""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line in lines:
            line_str = line.strip()
            if not title and line_str.startswith('# '):
                # Clean up markdown headers
                raw_title = line_str[2:].strip()
                # Remove emojis for cleaner link text if needed or keep them
                title = raw_title
            elif not description and (line_str.startswith('> **') or line_str.startswith('> _')):
                description = line_str.strip('> * _').strip()
            elif not description and line_str and not line_str.startswith('#') and not line_str.startswith('!['):
                description = line_str[:120] + '...' if len(line_str) > 120 else line_str
                
            if title and description:
                break
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        
    if not title:
        title = filepath.stem
    return title, description

def scan_repository():
    """Scans all folders and groups markdown files into document pairs."""
    categories = {}
    
    for item in sorted(os.listdir(ROOT_DIR)):
        folder_path = ROOT_DIR / item
        if not folder_path.is_dir() or item in EXCLUDE_DIRS or item.startswith('.'):
            continue
            
        md_files = [f for f in folder_path.glob("*.md") if not f.name.endswith(".metadata.json")]
        if not md_files:
            continue
            
        # Group files into paired (KR/EN) or single documents
        doc_map = {}
        for f in sorted(md_files):
            stem = f.stem
            
            # Check for language suffixes
            is_en = stem.endswith("_EN")
            is_kr = stem.endswith("_KR")
            
            if is_en:
                base_name = stem[:-3]
                lang = "EN"
            elif is_kr:
                base_name = stem[:-3]
                lang = "KR"
            else:
                base_name = stem
                lang = "DEFAULT"
                
            if base_name not in doc_map:
                doc_map[base_name] = {}
            doc_map[base_name][lang] = f
            
        categories[item] = doc_map
        
    return categories

def build_index_content(categories):
    """Builds the comprehensive index.md content in Quartz digital garden format."""
    lines = [
        "![Intro Image](./ai_infra_bridge.jpg)",
        "",
        "# 🚀 Infra Veteran ➔ AI Innovator",
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
        "| Core Domain | Key Operational Milestone | Quick Links |",
        "| :--- | :--- | :--- |",
        "| **Edge AI & eBPF SOC** | K3s 32C/192GB Scale-up, eBPF Cilium/Hubble L3-L7 Firewall & Telegram SOC | [[Edge_AI/14_ebpf_cilium_ai_firewall_and_telegram_soc_EN|Security SOC (EN)]] · [[Edge_AI/14_ebpf_cilium_ai_firewall_and_telegram_soc|한국어]] |",
        "| **AI Agent R&D** | OpenClaw Multi-Agent Architecture with HIL Approvals & Disposable Browser Sandbox | [[Openclaw/openclaw_Test|OpenClaw (EN)]] · [[Openclaw/openclaw_Test_KR|한국어]] |",
        "| **DevOps & Digital Garden** | Quartz Digital Garden with Prometheus & Grafana Monitoring Stack | [[Personal Website/05_Final_Completion_Report_EN|Build Log (EN)]] · [[Personal Website/05_Final_Completion_Report_KR|한국어]] |",
        "| **Automation & Tooling** | High-speed Excel Data Analyzer & PyMuPDF Security Redaction Desktop App | [[Excel_Analyzer/Project_Completion_Report_EN|Excel Analyzer]] · [[PDF_APPS/Project_Completion_Report_EN|PDF Utility]] |",
        "",
        "> 💡 *Documents are maintained with bilingual support (한국어 / English). Click on the corresponding links to open the localized documentation.*",
        "",
        "---",
        "",
        "## 📂 Technical Notes & Knowledge Catalog",
        ""
    ]
    
    # Categorization mapping for friendly display
    category_meta = {
        "Edge_AI": {
            "title": "🤖 Edge AI & In-Cluster Deep Learning",
            "desc": "On-premise K3s cluster running multimodal AI pipelines (RapidOCR, CTranslate2, Whisper, VLM) and eBPF cyber defense."
        },
        "Openclaw": {
            "title": "🧠 Autonomous AI Agents (OpenClaw)",
            "desc": "Zero-trust autonomous agent ecosystem with disposable browser sandbox and Human-in-the-Loop governance."
        },
        "LangCain": {
            "title": "🔗 LangChain & LLM Orchestration",
            "desc": "Next.js + FastAPI enterprise AI agent integration, multimodal fallback pipelines, and PM2 production operations."
        },
        "Personal Website": {
            "title": "🌐 DevOps, Infrastructure & Digital Garden",
            "desc": "chaeyul.uk digital garden architecture, Grafana & Prometheus monitoring, and reverse-proxy hardening."
        },
        "Excel_Analyzer": {
            "title": "📊 Automation: Excel Data Task Analyzer",
            "desc": "Automated ticketing analysis, resolution metrics calculation, and repetitive issue clustering desktop tool."
        },
        "PDF_APPS": {
            "title": "📄 Security: PDF Pro Redaction Editor",
            "desc": "PyMuPDF desktop utility performing true structural PII byte-purging and localized text annotations."
        },
        "Self-study German": {
            "title": "🇩🇪 Web App: Self-Study German Platform",
            "desc": "Glassmorphism UI language learning application with Web Speech API integration and static hosting."
        }
    }
    
    # Render folders
    for folder, doc_map in sorted(categories.items()):
        meta = category_meta.get(folder, {
            "title": f"📁 {folder.replace('_', ' ')}",
            "desc": f"Technical documentation and architectural notes for {folder}."
        })
        
        lines.append(f"### {meta['title']}")
        lines.append(f"> {meta['desc']}")
        lines.append("")
        
        for base_name, langs in sorted(doc_map.items()):
            # Determine display title
            preferred_file = langs.get("DEFAULT") or langs.get("KR") or langs.get("EN")
            raw_title, desc = extract_metadata(preferred_file)
            
            # Format clean title
            display_title = raw_title.replace("[최종 완료 보고서]", "").strip()
            
            links_part = []
            if "EN" in langs:
                en_path = f"{folder}/{langs['EN'].stem}"
                links_part.append(f"[[{en_path}|English (🇺🇸)]]")
            if "KR" in langs:
                kr_path = f"{folder}/{langs['KR'].stem}"
                links_part.append(f"[[{kr_path}|한국어 (🇰🇷)]]")
            if "DEFAULT" in langs:
                def_path = f"{folder}/{langs['DEFAULT'].stem}"
                # If there is also an EN counterpart
                if "EN" in langs:
                    links_part = [f"[[{def_path}|한국어 (🇰🇷)]]"] + links_part
                else:
                    links_part.append(f"[[{def_path}|Read Note]]")
                    
            links_str = " · ".join(links_part)
            lines.append(f"* **{display_title}** : {links_str}")
            if desc and not desc.startswith("#"):
                lines.append(f"  - *{desc}*")
                
        lines.append("")
        
    lines.extend([
        "---",
        "",
        "## 🗂️ Workspace Directory Overview",
        ""
    ])
    
    for folder in sorted(categories.keys()):
        meta = category_meta.get(folder, {"desc": "Technical notes and implementation guides."})
        lines.append(f"- **{folder}/** → {meta['desc']}")
        
    lines.extend([
        "",
        "<br>",
        "<br>",
        "",
        '<div align="center">',
        '  <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fdoc.chaeyul.uk&label=Total%20Views&labelColor=%23555555&countColor=%23005a9c&style=flat" alt="Views" />',
        "</div>",
        ""
    ])
    
    return "\n".join(lines)

def main():
    print("🔍 Scanning Technical-Notes workspace for folders and markdown files...")
    categories = scan_repository()
    total_docs = sum(len(docs) for docs in categories.values())
    print(f"✅ Found {len(categories)} categories and {total_docs} document groups.")
    
    new_index_content = build_index_content(categories)
    index_file = ROOT_DIR / "index.md"
    
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(new_index_content)
        
    print(f"🎉 Successfully generated and updated {index_file}!")

if __name__ == "__main__":
    main()
