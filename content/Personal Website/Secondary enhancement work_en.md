# [Integration Report] Secondary enhancement work Project Results

> 🇰🇷 [한국어 버전](./Secondary enhancement work)

**Last Modified**: March 12, 2026
**Author**: Development Team

---

## 1. Overview
This report summarizes the key implementation details and results related to the `Smart Dictionary` and `Hybrid Cache` systems. With this update, data retrieval performance and the efficiency of the user dictionary feature have been significantly improved.

---

## 2. Key Implementations and Changes

### ① Smart Dictionary Implementation
* **AI-Based Sentence Analysis**: Developed an algorithm to understand the context of words and highly recommend the optimal meanings and example sentences.
* **Personalized Wordbook Integration**: Added functionality to automatically categorize and review unknown or frequently searched vocabulary by integrating with learning data.
* **Dictionary Data Pipeline Optimization**: Improved asynchronous loading and searching of large external/internal dictionary databases for better efficiency.

### ② Hybrid Cache System Application
* **Multi-Tier Caching System Introduction**:
  * Frequently searched words or data are stored in a `Fast Cache (Memory-based, RAM, Redis)` to ensure real-time responses (Response time < 10ms).
  * Data with relatively lower query frequencies are strategically routed through a `Flash SSD / Disk` cache or the main Cloud Database.
* **Cache Invalidation and Synchronization**: Implemented event-driven synchronization logic to instantly refresh the cache and maintain up-to-date states when data is updated.
* **Performance Stability Assurance**: Proven overall system stability by successfully distributing DB load even during peak data request periods.

    <div align="center">
      <img src="smart_dict_hybrid_cache_1773254591153.png" width="600" alt="Smart Dictionary and Hybrid Cache Architecture">
      <p><i>[Figure 1: Newly built Smart Dictionary and Hybrid Cache System Architecture]</i></p>
    </div>

---

## 3. March 12, 2026 — Additional Feature Development & Admin Enhancement

### ③ Global Dictionary UI Upgrade
* **Table-Based Layout**: Replaced the card-based dictionary view in `study.html` with a premium glassmorphism-style data table.
* **Detailed Data Display**: Each row now shows Word, Part of Speech, Gender, Plural, Korean/English meaning, and Level all at once.
* **TTS (Text-to-Speech) Integration**: Added a 🔊 speaker button to each row to read German words aloud using the Web Speech API.
* **Backend API Extension**: Updated the word detail query function in `crud.py` to return `gender`, `plural`, `level`, and `pronunciation` fields.

### ④ Speed Quiz Start Bug Fix
* **Issue**: Clicking the Start button on Speed Quiz triggered `"Cannot set properties of null (setting 'textContent')"`.
* **Root Cause**: The `#gameTimer` DOM element referenced by `quiz.js` was missing from `quiz.html`.
* **Resolution**: Added the `gameTimer` element to the `.game-stats` section in `quiz.html`. Also improved the `catch` block in `quiz.js` and added `try-except` error logging to the `/api/quiz/start` endpoint in `main.py`.

### ⑤ Sentence Management System
#### Duplicate Prevention
* CSV uploads now check against existing German entries (`sentence_de`) and automatically skip duplicates.
* Added `get_sentence_by_de()` helper function to `crud.py`.

#### Full CRUD in Admin Dashboard
* **Edit**: ✏️ button on each row opens a detailed edit modal.
* **Delete**: Individual 🗑️ delete button per row.
* **Select All Checkbox**: Header checkbox for selecting/deselecting all entries.
* **Bulk Delete**: Select multiple entries and remove them all at once with the "선택 삭제" button.

#### New Backend API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/admin/sentences/{id}` | PUT | Update a single sentence |
| `/admin/sentences/bulk-delete` | POST | Bulk delete selected sentences |

### ⑥ Sentence Data Model Extension & Dynamic CSV Header Mapping

#### New Data Fields
| Column | Description | Example |
|---|---|---|
| `situation` | Situational category/topic | Hospital, School, Restaurant |
| `pronunciation` | Phonetic Korean romanization | 이히 하-베 코프슈메르첸 |

#### Dynamic Header Mapping
* The CSV upload engine reads the first row and automatically maps column names to the correct DB fields.
* Supported column name aliases:
  * `german` → `sentence_de`
  * `korean` → `translation_ko`
  * `level` → `difficulty`
  * `situation`, `pronunciation` map directly

**Supported CSV format example:**
```
id,situation,german,korean,pronunciation,level
1,Hospital,Ich habe Kopfschmerzen.,머리가 아파요.,이히 하-베 코프슈메르첸,A1
```

---

## 4. Troubleshooting Log (2026-03-12)

### 🔴 Issue #1 — Speed Quiz Fails to Start (`gameTimer` Missing)
* **Symptom**: JavaScript error and page freeze upon clicking the quiz start button.
* **Root Cause Analysis**: The `#gameTimer` DOM element referenced by `gameTimer.textContent = ...` in `quiz.js` was not defined in `quiz.html`, resulting in a `null` pointer error.
* **Fix**: Added `<div id="gameTimer">` to the `.game-stats` section in `quiz.html`.
* **Supplementary Improvements**: Enhanced error logging in both `quiz.js` and `main.py` to surface user-friendly error messages for faster future diagnosis.

---

### 🔴 Issue #2 — Sentence Management Table Shows "API Error: Unknown error"

* **Symptom**: The sentence management table in the Admin Dashboard displayed `"API 오류: Unknown error"` and failed to load any data immediately after adding new fields to the data model.
* **Error Log**:
  ```
  sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn)
  column sentences.situation does not exist
  ```
* **Root Cause**: The `situation` and `pronunciation` columns were added to `models.py` (SQLAlchemy model), but the actual running PostgreSQL table was never migrated — the columns did not physically exist in the database.
  * SQLAlchemy uses a **code-first** approach. Without Alembic, schema changes in Python models do **not** automatically propagate to the database.
* **Fix**: Applied a manual DDL migration directly on the PostgreSQL database:
  ```sql
  ALTER TABLE sentences ADD COLUMN IF NOT EXISTS situation VARCHAR;
  ALTER TABLE sentences ADD COLUMN IF NOT EXISTS pronunciation VARCHAR;
  ```
* **Verification**: Confirmed successful migration via `\d sentences` in psql. API returned data normally afterwards.
* **Future Recommendation**: Introduce **Alembic** for database migration management. This will auto-generate migration scripts whenever models change, eliminating the need for manual DDL and reducing the risk of schema drift.

---

## 5. Future Plans
* **User Behavior Analysis**: Further tune the Cache Hit Ratio by analyzing actual learning data search trends.
* **Integrated Monitoring**: Plan to integrate hybrid cache performance metrics (Redis, DB Load, etc.) for real-time monitoring on the Grafana dashboard.
* **Alembic Migration Integration**: Adopt Alembic for versioned DB schema management to improve deployment safety.

---

**[March 12, 2026 — Additional Development Update Complete]**

---

## 6. March 13, 2026 — UI/UX Unification & Unified Theme System

### ⑧ Quiz Page Full UI/UX Overhaul (quiz.html Rewrite)

#### Background
The quiz page relied on the **UIkit** third-party CSS framework, making it visually inconsistent with the rest of the site (`study.html`, `index.html`). It also had a hardcoded dark theme with no way to switch to light mode.

#### Key Changes

| Item | Before | After |
|------|--------|-------|
| CSS Framework | UIkit CDN | Site-wide `/css/style.css` |
| Navigation Bar | UIkit navbar | Glassmorphism sticky header |
| Theme Support | Dark-only | 🌙 Night / ☀️ Day toggle button |
| Login Modal | UIkit modal | Custom glassmorphism modal |
| Theme Persistence | None | localStorage permanent save |

#### 4 New Game Modes
| Mode | Badge | Description |
|------|-------|-------------|
| 🧠 Word Meaning Quiz | CLASSIC | German word → Korean meaning (4-choice MCQ) |
| ⌨️ Spelling Game | NEW | See Korean meaning → type the German word |
| ✏️ Fill in the Blank | NEW | Fill missing word in a conversation sentence |
| 💬 Conversation Quiz | NEW | German conversation → Korean meaning (MCQ) |

<div align="center">
  <img src="quiz_ui_dark_mode.png" width="640" alt="Quiz Page UI Overhaul — Glassmorphism Dark Theme">
  <p><i>[Figure 2: Quiz Game Center — New glassmorphism UI with 4 game mode selection cards]</i></p>
</div>

---

### ⑨ Dark / Light Mode Added to All Lesson Pages

#### Background
While `study.html` and `quiz.html` already supported theme switching, all Lesson pages (`Lesson_1.html` through `Lesson_30.html` and `Menu.html`) were hardcoded to light mode only.

#### Implementation
- `Lesson_1.html`: Added 🌙 Night button to header; applied dark theme via `body.dark-mode` CSS class
- `Menu.html`: Added 🌙 Night button to top-right corner; card/background colors driven by CSS variables
- **CSS Variable Design**: Background, card, text, and button colors transition naturally with the theme

**Dark Mode CSS Variable Structure:**
```css
body.dark-mode {
    --bg-grad-start: #0f172a;
    --bg-grad-end:   #1e293b;
    --card-bg:       rgba(30,41,59,0.9);
    --card-active-bg:  rgba(16,185,129,0.12);  /* currently playing card */
    --card-looping-bg: rgba(245,158,11,0.12);  /* looping card */
    --text-main:     #f1f5f9;
}
```

---

### ⑩ Unified Theme System (`/js/theme.js`)

#### Background
Each page was managing its own theme using separate localStorage keys (`theme`, `lesson_theme`) and duplicated JS logic, causing **theme settings to fall out of sync across pages**.

#### Architecture

**Unified Theme Flow:**
```
localStorage['theme'] = 'dark' | 'light'
              ↕ shared across ALL pages
      ┌────────────────────────────────┐
      │      /js/theme.js  (shared)    │
      └────────────────────────────────┘
           ↙                    ↘
  Main / Study / Quiz         All Lesson Pages
  (:root.light class)       (body.dark-mode class)
```

#### Key Features
| Feature | Description |
|---------|-------------|
| Single Key | One `localStorage['theme']` syncs all pages |
| Auto Button Injection | Floating 🌙 Night button injected into Lesson pages |
| Auto CSS Injection | Dark styles applied even to Lesson 8–30 with no existing toggle |
| No Flash (FOUC) | Theme applied immediately on page load, no visual flicker |
| Universal Coverage | Covers index, study, quiz, and all 20 Lesson pages |

#### Automated Bulk Deployment
Used a shell one-liner to inject the script tag into all 20 Lesson HTML files at once:
```bash
for f in *.html; do
  sed -i 's|</body>|    <script src="/js/theme.js"></script>\n</body>|' "$f"
done
```

<div align="center">
  <img src="unified_theme_system.png" width="640" alt="Unified Theme System Architecture">
  <p><i>[Figure 3: Unified Theme System — theme.js as the single source of truth, sharing one localStorage key across all pages]</i></p>
</div>

---

## 7. Troubleshooting Log (2026-03-13)

### 🔴 Issue #5 — Orphaned UIkit Code in quiz.html
* **Symptom**: After migrating quiz.html, the login button stopped working; orphaned code blocks found after the `</html>` closing tag.
* **Root Cause**: The previous UIkit script block was not fully removed during the UIkit → shared CSS migration, leaving dead code that confused the JS parser.
* **Fix**: Complete clean rewrite of `quiz.html` to eliminate all remnants. Theme logic moved to the shared `theme.js` file.

### 🔴 Issue #6 — Dark Mode JS Function Missing in Lesson_1.html
* **Symptom**: Clicking the 🌙 Night button had no effect.
* **Root Cause**: Inaccurate target-content matching in the `replace_file_content` tool caused the `toggleDarkMode()` function to not be inserted correctly.
* **Fix**: Restored `playNextSequence()` function and reinserted the dark mode function at the correct position. Later removed all inline dark mode code after migrating to `theme.js`.

### 🔴 Issue #7 — Missing `theme.js` Script Tag in Menu.html
* **Symptom**: Console error `toggleTheme is not defined` on Menu.html.
* **Root Cause**: During `theme.js` integration, only an HTML comment was inserted instead of the actual `<script src>` tag, so the function never loaded.
* **Fix**: Manually added `<script src="/js/theme.js"></script>` tag directly.

---

## 8. March 14, 2026 — Game Mode Expansion, Telegram Optimization & Statistics Restoration

### ⑪ Quiz System Evolution & 4 Primary Game Modes
*   **Game Mode Completion**: Fully integrated **Spelling (⌨️)**, **Fill in the Blank (✏️)**, and **Conversation (💬)** expert modes into `quiz.js` beyond simple word selection.
*   **Learning Algorithm Optimization**: Refined the SM-2 algorithm's quality score calculation to improve the accuracy of review intervals.

### ⑫ Admin Dashboard & Integrated Telegram Management
*   **Dedicated Telegram Menu**: Separated Telegram settings from the general admin panel into a standalone tab for improved UX.
*   **Advanced Scheduler Management**: Implemented **Edit**, **History View**, and **Instant Resend** features for scheduled notifications, maximizing operational convenience.
*   **Daily Goal Integration**: Enabled setting daily targets (words/quizzes) per user, with automatic achievement notifications sent via Telegram.

### ⑬ System Security & Stability (Vulnerability Improvements)
*   **API Path Normalization**: Normalized all endpoints to a consistent `/api/` prefix to resolve path duplication and clipping issues in proxy environments.
*   **Hardened JWT Validation**: Improved global error handling for token expiration and unauthorized access via a centralized `apiFetch` wrapper.
*   **Function Anchoring (Race Condition Fix)**: Resolved the "unresponsive buttons" issue caused by script loading order by anchoring all global handlers early in the execution flow.

### ⑭ User Statistics (Heatmap) Final Restoration
*   **Issue**: Data was fetched successfully, but the modal remained invisible on the screen.
*   **Root Cause**: The modal was clipped or hidden by parent elements' `overflow` or `z-index` properties within the deep DOM tree.
*   **Resolution**: 
    - **DOM Relocation**: Moved the statistics modal to the top-level `<body>` tag to ensure an independent stacking context.
    - **Forced Visibility**: Applied `z-index: 99999` and `!important` styling to ensure it always appears on top of any other element.

<div align="center">
  <img src="project_enhancement_summary_mar14.png" width="640" alt="March 14 Key Updates Summary">
  <p><i>[Figure 4: 4 Game Modes Selection and Telegram Notification Settings UI]</i></p>
</div>

---

## 9. Troubleshooting Log (2026-03-14)

### 🔴 Issue #8 — Visual "Invisibility" of Statistics Modal
*   **Symptom**: Console showed successful data retrieval (200 OK), but no visual change occurred on the page.
*   **Root Cause**: A parent element within the `admin-layout` had a `transform` property, creating a new stacking context that trapped/clipped the fixed pop-up.
*   **Resolution**: Moved the modal HTML to be a direct child of `<body>` and re-established `position: fixed` relative to the viewport.

### 🔴 Issue #9 — Unresponsive Admin Dashboard Buttons (Registration Race)
*   **Symptom**: Statistics or Login buttons would sometimes fail to trigger after a page refresh.
*   **Root Cause**: A race condition where user list rendering happened faster than the event listener registration.
*   **Resolution**: Restructured the script to anchor all global handlers to the `window` object *before* any list rendering (`loadUsers`) occurs.

---

**[March 14, 2026 — Additional Development Update Complete]**
