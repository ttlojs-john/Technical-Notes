# [Phase 2] chaeyul.uk Secondary Enhancements

**Update Period**: March 12, 2026 – March 14, 2026

**Project Overview**: Phase 2 shifts focus towards high-octane data optimization engines (Caching), granular Gamification components, and structural consistency across the frontend via a unified cross-page layout synchronization.

## 🌟 1. Major Functional Upgrades

### Smart Dictionary & Hybrid Cache System
- **Smart Dictionary**: Rolled out an AI-context-aware dictionary algorithm providing dynamic phrase recommendations linked intimately with users' private glossaries.
- **Hybrid Multi-tier Caching**: Deployed a dual-level data cache pattern. Level 1 leverages Redis (in-memory) yielding sub-10ms latency for frequent queries. Level 2 relies on efficient disk-persistence caching. Exported `hybrid_cache_hits_total` metrics natively to Prometheus.

![Smart Dictionary & Hybrid Cache System Architecture](./archive/smart_dict_hybrid_cache_1773254591153.png)
*<Figure: Newly Deployed Smart Dictionary and Hybrid Cache Architecture>*

### Smart Quiz Center Revamp
- Redesigned the baseline learning interface into an expansive, four-pillared gamification suite utilizing a sleek glassmorphism aesthetic:
  - 🧠 Classic Mode (Contextual Word Meaning Selection)
  - ⌨️ Spelling Expert (Korean-to-German manual typing drill)
  - ✏️ Fill-in-the-Blank (Sentence context insertion)
  - 💬 Dialogue Master (Whole-sentence translation multi-choice)

![Quiz UI Dark Mode](./archive/quiz_ui_dark_mode.png)
*<Figure: Smart Quiz Center featuring Glassmorphism UI and 4 Game Modes>*

### Unified Global Theme Orchestration 
- Converted isolated theme logic spread across 30+ pages into a strictly supervised `theme.js` module.
- Leveraged single-source `localStorage` keys guaranteeing zero-flash (FOUC), instantaneous Light/Dark theme switching across all interactive and static HTML resources.

![Unified Theme System Architecture](./archive/unified_theme_system.png)
*<Figure: Centralized Theme Architecture Operating via Single LocalStorage Key>*

### Enhanced CMS & Telegram Routing
- Fully decoupled the Telegram scheduling portal into a discrete admin sub-tab, enabling precise notification editing, manual rebroadcast triggers, and visual history logs.
- Added advanced CSV parsing dynamically matching localized dataset headers to exact PostgreSQL columns.

![Project Enhancement Summary](./archive/project_enhancement_summary_mar14.png)
*<Figure: Telegram Notification Management and Quiz UI Selection Screen>*

## 🛠 2. Logged Troubleshooting

- **Database Missing Column (Alembic Void)**: Newly appended columns (`situation`, `pronunciation`) via Pydantic caused an `UndefinedColumn` crash in production due to the lack of code-first automatic DDL mapping. Bridged manually by executing direct `ALTER TABLE` queries; outlined future need for Alembic migrations.
- **Racing Theme Application Script**: Manual insertion tools failed to uniformly inject toggling functions inside deeply nested HTML sub-pages resulting in disconnected UI themes. Replaced inline scripting entirely with the single automated global injector logic.
- **Modal DOM Clipping**: The analytics heatmap modal failed to visually render despite valid data receipt. Root-cause traced to CSS `transform` boundary limitations set by a parent layout. Remapped modal injection directly inside the top-tier `<body>` context, strictly enforcing overriding `z-index` properties.
