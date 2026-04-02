# [Phase 3] chaeyul.uk V3.0 Subtitle Pipeline & Architecture Update

**Update Period**: March 15, 2026 – March 21, 2026

**Project Overview**: Phase 3 heralded the arrival of the **V3.0 Smart Subtitle Rendering Pipeline**. It decisively bridged operational gaps by incorporating **Intelligent Auto-Recovery Monitoring Webhooks** and a seamless, high-speed **Global Localization Engine (i18n)** capable of hot-swapping languages on the fly.

## 🌟 1. Progressive Milestones

### 🚀 3D Flashcards & Asynchronous Scheduler (Mar 15-16)
- **Interactive Flashcards**: Engineered a visually immersive 3D-CSS flipping flashcard system structurally woven into the unified Quiz Center alongside Dual N-Back and the classic Speed Quiz.
- **SRS Mechanism**: Integrated Spaced Repetition Algorithms ensuring priority caching and review frequency for unfamiliar vocabulary.
- **Scheduler Stabilization**: Extinguished recurrent backend DB deadlocks by forcefully tethering the `apscheduler` chron-engine directly into the FastAPI asynchronous startup event loop.

### 🎥 V3.0 Backend Subtitle Pipeline (Mar 18)
- Transcended unstable client-side subtitle loading by injecting a bulletproof, server-driven background queue pipeline.
- Established strict job tracking properties allowing isolated processing/retry attempts and incorporated injected YouTube cookie bypass techniques for restricted videos.

### 🛡️ Smart Webhooks & Auto-Migration Models (Mar 19)
- **Two-Way Recovery Webhooks**: Upgraded passive Telegram monitoring to bidirectional control. Administrators can now authorize remote container-reboots directly from Telegram alerts through a rigidly verified, dual-auth webhook endpoint.
- **Auto-Schema Migration**: Implemented boot-time validation scripts. If dynamic dashboard settings mandate new database columns, the system detects and automatically modifies the PostgreSQL structural layout instantly, obliterating previous crash models.

![Infra Monitoring V2 Dashboard](./infra_v2_status.png)
*<Figure: Next-Gen Infrastructure Monitoring Dashboard with Glassmorphism>*

### 🌍 Universal i18n & Bulk Processing Refinements (Mar 20-21)
- Formulated an `i18n.js` interpreter engine. Backed by `MutationObserver` protocols and Incremental DOM updating practices, users can instantly switch between English and Korean translations system-wide without incurring full page reloads.
- Rolled out the **Bulk AI Job Queue** automating repetitive translation, narration, and transcription actions safely. Rectified OpenAI Whisper 413 HTTP limitations by actively performing intermediate audio compression down-sampling before API transmission.

![Premium Admin UI](./premium_admin_ui.png)
*<Figure: Premium Admin Interface featuring Custom Scrollbars and Bulk AI Process Visualization>*

## 🛠 2. Logged Troubleshooting

- **Admin Save Mechanism Halt (Pydantic Null)**: Updating extensive dashboard config settings sporadically threw 500/422 responses. Conclusively resolved by strictly pairing loose HTML template IDs with loosened Pydantic validation parameters alongside the brand-new auto-migration engine.
- **Monitoring CSS Grid Intersections**: Found Grafana iframes and real-time sparkline cards fiercely overlapping due to Z-index/Box clashes inside CSS Grid boundaries. Radically redesigned the UI layout paradigm moving from an overlapping grid to a much safer, premium vertical-stack architecture.
