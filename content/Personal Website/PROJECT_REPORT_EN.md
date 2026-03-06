# [Integrated Report] chaeyul.uk Web Server Project Construction & Troubleshooting Results

**Last Updated**: March 6, 2026 (Server Infrastructure Monitoring Integration)
**Target Domain**: `chaeyul.uk`
**System Environment**: Docker Compose-based Container Environment
- **Frontend**: Node.js (Express)
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL 15
- **Infrastructure**: Cloudflare Proxy & Linux Server

---

## 1. Project Overview
The objective of this project is to build a dedicated web server for premium media (photo, video, audio) management and streaming. It features a UI optimized for high-definition media storage and a robust backend structure for secure data management, finally made accessible to external users via the `chaeyul.uk` domain.

---

## 2. Key Implementations & Changes

### ① Rebranding (Custom Domain & Family Identity)
- **Enhancement**: 
    - Updated the site name to `CHAEEUN & CHAEYUL` to strengthen the identity as a family shared project.
    - Improved the system to dynamically manage top logo text and branding settings through the dashboard.

### ② External Access & Routing Optimization
- **Direct IP Access Block**: Blocked direct access via IP addresses to enhance security.
- **URL Normalization & SPA Support**: Supported root path transitions and Single Page Application (SPA) environment.
- **Layout Optimization**: Minimized the spacing between the top navigation menu and the video player to create an immersive layout.
- **Security Monitoring Dashboard [NEW]**: Established a system for monitoring real-time visitors, daily unique IPs, cumulative counters, and recent login logs (success/failure).
- **CMS-Driven Lesson Management [NEW]**: Successfully uploaded and managed 20+ German lesson pages via the dashboard, with immediate site reflection.
- **Auto-Translation for Study [NEW]**: Logic to automatically translate transcripts (DE/EN -> KO) when native Korean subtitles are unavailable.
- **Premium Masonry Gallery [NEW - 02.24]**: Implemented a sophisticated Masonry layout and year-based filtering system using photo metadata (EXIF).
- **Asset Optimization [NEW - 02.24]**: Developed a local Python preprocessing tool (`preprocess_images.py`) and enforced 1-year cache headers for improved Cloudflare and edge-node performance.

    <div align="center">
      <img src="premium_gallery_masonry.png" width="300" alt="Premium Masonry Gallery Layout">
      <p><i>[Figure 1: High-end Masonry gallery layout with smart filtering]</i></p>
    </div>
- **Learning UX & Theme Customization [NEW - 02.25]**:
    - **A-B Repeat Persistence**: Automated saving/restoration of loop points using `localStorage`.
    - **Focus Mode & Hidden Timestamps**: Optimized the transcript UI to highlight only the current active sentence while stripping time markers for better focus.
    - **Sticky Study UI**: Fixed the player and transcript to the top of the viewport for continuous access while scrolling.
    - **Global Theme Switcher**: Implemented a site-wide Dark/Light mode toggle with persistent user settings.
    - **Real-time Home Translation**: Added live DE-to-KO translation overlays on promotional homepage videos.
    - **Wordbook Pagination**: Enhanced vocabulary management with 10-item pagination and refined visibility for various theme contexts.

    <div align="center">
      <img src="theme_switcher_ui.png" width="300" alt="Global Theme Switcher System">
      <p><i>[Figure 2: Global Dark/Light mode theme switching interface]</i></p>
    </div>
- **Mobile Learning Optimization & Background Playback [NEW - 02.26]**:
    - **Mobile-Responsive Layout**: Dynamically adjusted transcript heights and optimized sticky positioning for smaller screens to ensure visibility of the video selection list.
    - **Background Playback & MediaSession**: Integrated `MediaSession` API and a silent heartbeat mechanism to prevent video pausing when the screen is locked or the browser is backgrounded.
    - **Lock Screen Controls**: Enabled play/pause and seeking capabilities directly from the mobile lock screen and notification center.

    <div align="center">
      <img src="mobile_optimized_study.png" width="300" alt="Mobile Study & Background Playback">
      <p><i>[Figure 3: Mobile-optimized study UI with lock screen background controls]</i></p>
    </div>
- **AI-Powered Smart Learning Tools [NEW - 03.03]**:
    - **Context-Aware Sentence Generation**: Leverages **OpenAI gpt-4o-mini** to automatically generate practice sentences using words saved in the user's Wordbook. Sentences are provided in German with English and Korean translations, with adjustable CEFR difficulty levels (A1–B2) and sentence count (3/5/8).
    - **STT Pronunciation Checker**: Utilizes the browser's built-in **Web Speech API** (`SpeechRecognition`, `de-DE`) to capture user's spoken German and compare it against the original transcript using a **Levenshtein similarity algorithm**. Provides word-by-word accuracy feedback with color-coded highlights (✅ correct / ❌ incorrect) and an overall accuracy percentage score.
    - **Zero Server Cost for STT**: The pronunciation feature operates entirely within the browser (Chrome/Edge recommended), requiring no additional server resources or API fees.
    - **New Backend Endpoint**: `POST /api/ai/generate-sentences` added to handle AI-powered sentence generation requests.
- **Mobile Learning UX Overhaul & Subtitle Sync Enhancement [NEW - 03.04]**:
    - **Video Search & Pagination**: Added a real-time search filter bar for quickly finding videos among 66+ entries by title. Introduced 12-per-page pagination to eliminate endless scrolling on mobile devices.
    - **Compact Mobile Thumbnails**: Reduced thumbnail sizes (`minmax(140px)`) and limited titles to 2 lines on mobile for higher density display, showing more videos per screen.
    - **Saved Loop Manager**: Added a dedicated 「📋 Saved Loops」 button and modal to display all previously saved A-B repeat segments across all videos. Clicking an item auto-loads the video and applies the saved loop. Each video card displays a 「🔁 Saved」 badge if a loop exists.
    - **Persistent Loop Storage**: Turning off A-B repeat no longer deletes the saved segment from `localStorage`, enabling users to reload saved loops on subsequent visits.
    - **Subtitle Sync Offset Control**: Added ±0.5s offset adjustment buttons (−/+) next to the transcript header, allowing users to fine-tune subtitle timing. Settings persist across sessions via `localStorage`.
    - **Optimized Highlight Engine**: Replaced `requestAnimationFrame` with a **100ms `setInterval`** for more consistent subtitle synchronization. Added DOM change detection to only update when the active line changes, reducing unnecessary renders.
    - **Lazy Loading**: Applied `loading="lazy"` to video thumbnails for improved initial page load performance.

- **Infrastructure & System Monitoring Integration [NEW - 03.06]**:
    - **Prometheus & cAdvisor Integration**: Added Prometheus and cAdvisor containers to the Docker Compose topology to establish a robust collection system for server infrastructure and per-container resource (CPU, Memory, Network) usage.
    - **Admin Dashboard Integration**: Unified the system monitoring section at the top of the Admin Dashboard with direct access buttons to the cAdvisor and Prometheus web UIs. Applied text color styling for accessible visual contrast.
    - **Secure External Access (Reverse Proxy)**: Instead of exposing raw ports, configured `/cadvisor` and `/prometheus` proxy routes in the frontend Node.js server (`server.js`) to ensure secure administration through the main domain.

    <div align="center">
      <img src="admin_monitoring.png" width="300" alt="Admin Dashboard with System Monitoring Buttons">
      <p><i>[Figure 6: Admin Dashboard augmented with dedicated cAdvisor and Prometheus System Monitoring buttons]</i></p>
    </div>

- **Progressive TypeScript (JSDoc) Integration for Architecture Stability [NEW - 03.06]**:
    - **JSDoc-based Type Inference**: Rather than introducing a complex build step with a full TypeScript conversion, utilized JSDoc syntax (`/** @type {...} */`) to establish type safety directly within existing vanilla JavaScript files (`app.js`, `study.html`).
    - **Data Interface Definition (`types.ts`)**: Declared standard interface models for backend API responses (e.g., `User`, `Photo`, `Vocabulary`) and frontend configuration data (`SiteSettings`) in `types.ts` to ensure structural consistency.
    - **IDE IntelliSense Optimization**: Added `jsconfig.json` (`"checkJs": true`) to the project root, enabling proactive detection of type errors in VS Code and substantially improving DOM element casting stability.

---

## 3. Troubleshooting Log

### [Issue]: Login modal appears forcefully on initial domain access instead of the home page
- **Root Cause Analysis**:
    - Conflicting style attributes were declared in the login modal (`id="loginModal"`) within `index.html`. (`style="display:none; ... display:flex;"`)
    - Due to CSS priority, the later declared `display:flex;` was applied, causing the modal to cover the screen upon initial access.
- **Action Taken**:
    - Removed the redundant `display:flex;` from inline styles and fixed the default state to `display:none;`.
    - Modified logic to ensure the modal is only activated via JavaScript.

### [Issue]: Internal Server Error (500) due to missing database columns
- **Root Cause Analysis**:
    - New columns `is_active` and `created_at` were added to `models.py` during account management enhancement but were not reflected in the existing DB tables, causing `UndefinedColumn` errors.
- **Action Taken**:
    - Developed an automated migration script (`migrate.py`) to execute `ALTER TABLE` commands.
    - Real-time update of the containerized database schema resolved the issue.

### [Issue]: YouTube transcript load failure and no click response
- **Root Cause Analysis**:
    - **Network Isolation**: The backend container was exclusively in an `internal` network, blocking external YouTube API calls.
    - **Library Specification Change**: Updates in `youtube-transcript-api` required class instantiation, which was not reflected in the code.
    - **Event Propagation Block**: `stopPropagation()` in frontend transcript clicks prevented the video seek logic from executing.
- **Action Taken**:
    - Added a `public` network to the backend in `docker-compose.yml` to allow internet access.
    - Upgraded the transcript extraction logic in `main.py` to be instance-based, fetching all available transcripts including auto-generated ones.
    - Fixed event propagation in `study.html` to allow both word dictionary lookup and video seeking on click.

### [Issue]: 'Not Found' or 'Field required' errors after adding CMS features
- **Root Cause Analysis**:
    - **Code Desync**: Even though the backend code (`main.py`) was edited locally, the Docker image held a static copy. A simple `restart` was insufficient for the container to recognize the new API endpoints.
    - **Data Validation Conflict**: When creating a page with empty editor content, the backend expected the `content` field as mandatory (`required`), leading to validation errors.
    - **Insufficient Exception Handling**: The frontend failed to check the response status during file loading, causing the editor to display `undefined` upon fetch failure.
- **Action Taken**:
    - Rebuilt the backend image using `docker compose up -d --build backend` to activate the updated APIs.
    - Refactored the form data handling in `main.py` to allow empty content sequences (`Form("")`).
    - Enhanced `app.js` with robust response verification and explicit error alerts to replace silent failures.

### [Issue]: Study Center: Video stops or jumps incorrectly when clicking words
- **Root Cause Analysis**:
    - Event bubbling from `word-item` to the parent `transcript-line` caused both the dictionary lookup and the video seek logic to fire simultaneously, leading to conflicts.
- **Action Taken**:
    - Implemented `event.stopPropagation()` within the `lookupWord` function to prevent bubbling.
    - Clearly separated dictionary lookup (click on word) from video seeking (click on line background).

### [Issue]: Timestamp numbers included when dragging text for selection
- **Root Cause Analysis**:
    - Timestamps like `[0:15]` were part of the text nodes, causing them to be copied along with sentences when manually dragged, which broke dictionary queries.
- **Action Taken**:
    - Added a `mouseup` listener to clone the selection and strip out all nodes with the `.timestamp` class before extracting text.
    - Ensures pure text search even when selecting multiple words manually.

---

## 4. Infrastructure Operations & Management

### ① Docker Compose Service Configuration
- **web_frontend**: Port 80/443 mapping, static file and proxy server.
- **web_backend**: API server and media/page management logic.
- **web_db**: Database for metadata storage.

### ② Deployment Automation
- Maintained a seamless deployment system based on `docker compose up -d --build`.

### ③ Web Page Management (CMS) [NEW]
- **Web Page Management (CMS)**:
    - **Real-time Editing**: Instant modification of HTML source code via an embedded editor in the dashboard.
    - **Page CRUD**: Direct creation and deletion of custom pages.
    - **HTML Upload**: Immediate reflection of uploaded local HTML files to the site.
- **Site & Navigation Settings**:
    - **Branding Control**: Unified management of site name (Logo) through the dashboard.
    - **Dynamic Navigation**: Freedom to add/remove top menu items with real-time reflection.
    - **Persistence**: All design and menu settings are stored via `settings.json`.
    - **File Explorer & Folder Management [NEW]**: Supports creating folders directly in the dashboard and intuitive navigation via Breadcrumbs.
    - **Direct CSS & Source Editing [NEW]**: Instant editing and application of all dedicated resources, including CSS files, through the built-in editor.
- **Feature Demo [Admin Layout]**:

    <div align="center">
      <img src="admin_layout.png" width="300" alt="Admin Dashboard Interface">
      <p><i>[Figure 4: Admin Dashboard with integrated File Explorer and Security Stats]</i></p>
    </div>


### ④ German Study Center [NEW]
- **Smart Learning Environment**:
    - **A-B Repeat & Speed Control**: Supports precise language learning with user-defined repeat intervals and 0.5x~1.5x speed adjustments.
    - **Real-time Transcript Integration**: Displays transcripts extracted via YouTube API with instant video seeking upon click.
    - **Instant Dictionary**: Provides real-time English and Korean translations via a lookup popup when clicking words in the transcript.
- **Personalized Vocabulary**:
    - **DB-Linked Vocab**: Save and manage encountered words in a personal vocabulary list with one click.
    - **Admin Control**: Easy addition/deletion of study videos via URL in the dashboard.
- **Feature Demo [Study Interface]**:

    <div align="center">
      <img src="study_lookup.png" width="300" alt="Study Interface Demo">
      <p><i>[Figure 5: German Study Center with word selection and real-time translation popup]</i></p>
    </div>

- **Homepage Promo & Loop Player [NEW]**:
    - **Randomized Loop Playback**: Infuses life into the site by randomly selecting and continuously looping YouTube videos registered for the homepage.
    - **Custom Controls**: Offers playback speed control (0.5x ~ 2.0x) and free zoom in/out for screen size.
    - **UI Optimization**: Minimalist design focused on the video player by removing unnecessary promo text and the 'Recent Uploads' section.
    - **Dedicated Management**: Independently manage the homepage video list separately from study videos via the dashboard.

---

## 5. Project Structure

```text
web_project/
├── docker-compose.yml           # Service container orchestration
├── PROJECT_REPORT.md            # Detailed project report (Korean)
├── PROJECT_REPORT_EN.md         # Detailed project report (English)
├── web-project.service          # Systemd service for auto-start
├── backend/                     # Python (FastAPI) API Server
│   ├── main.py                  # API endpoints and logic
│   ├── models.py                # SQLAlchemy DB models
│   ├── auth.py                  # JWT Auth and Security (IP blocking)
│   ├── crud.py                  # Database CRUD functions
│   ├── database.py              # DB connection and session
│   ├── migrate.py               # DB schema migration tool
│   ├── requirements.txt         # Python dependencies
│   └── uploads/                 # User-uploaded media storage
├── frontend/                    # Node.js (Express) Web Server
│   ├── server.js                # Proxy and static file server logic
│   ├── package.json             # Node dependencies
│   └── public/                  # Static resources (Vanilla JS)
│       ├── index.html           # Main Landing Page
│       ├── admin.html           # Admin Dashboard (CMS)
│       ├── gallery.html         # Media Gallery & Slideshow
│       ├── study.html           # YouTube Learning Center
│       ├── settings.json        # Dynamic site settings
│       ├── js/app.js            # Integrated frontend business logic
│       ├── css/style.css        # Unified design stylesheet
│       └── certs/               # SSL/TLS certificates
├── scripts/                     # Utility and automation scripts
│   └── preprocess_images.py     # [NEW] Local image optimization & metadata tool
└── db/
    └── init.sql                 # Initial database schema
```

---

## 6. Conclusion & Future Roadmap

### Current Status
- Management efficiency maximized through the integration of CMS and site settings.
- All functions are operating stably on a Docker container basis.

### Future Roadmap
- **Security**: Implement Cloudflare Full SSL and evaluate 2FA.
- **Performance**: Add thumbnail generation and caching logic for high-volume media.
- **AI Expansion**: Explore conversational AI simulations for sentence generation and detailed phoneme-level analysis for pronunciation feedback.
- **Learning Analytics**: Evaluate a per-user learning analytics dashboard tracking study time, loop frequency, and vocabulary progress.

---

## 7. Build Walkthrough

### Phase 1: Planning & Setup
- [O] Establishment of project directory structure and Docker environment.

### Phase 2: Backend Development
- [O] API development, JWT Auth, and security (IP blocking) implementation.
- [O] [NEW] Integration of CMS and site settings management APIs.
- [O] [NEW] Completion of YouTube Study Center API, transcript extraction, and vocabulary DB design.

### Phase 3: Frontend Development
- [O] Implementation of main gallery and slideshow.
- [O] [NEW] Integration of dashboard inline editor and settings menu.
- [O] [NEW] Real-time transcript-dictionary interface for German learning.
- [O] [NEW] (2026-02-23) Real-time security stats dashboard and file explorer-based CMS enhancement completed.
- [O] [NEW] (2026-02-23) Drag-and-drop dashboard layout management and smart learning selection logic applied.
- [O] [NEW] (2026-02-23) Automated YouTube transcript translation and integration of 20+ German lesson pages.
- [O] [NEW] (2026-02-24) Premium Masonry gallery, year-based filtering, and Cloudflare performance optimization completed.
- [O] [NEW] (2026-02-25) Study Center A-B persistence, focus mode, and sticky layout implemented.
- [O] [NEW] (2026-02-25) Global Light/Dark theme switcher and real-time translation system established.
- [O] [NEW] (2026-02-25) Vocabulary pagination and light mode UX optimization completed.
- [O] [NEW] (2026-02-26) Mobile learning layout optimization and background/lock screen playback control functionality completed.
- [O] [NEW] (2026-03-03) AI-powered Smart Learning: OpenAI gpt-4o-mini sentence generation API integration and Web Speech API STT pronunciation correction system implemented.
- [O] [NEW] (2026-03-04) Mobile learning UX overhaul: video search/pagination, saved loop management modal, subtitle sync offset controls, and rendering performance optimization completed.
- [O] [NEW] (2026-03-06) Server infrastructure monitoring established with Prometheus and cAdvisor container integration, along with admin domain reverse proxy routing.
- [O] [NEW] (2026-03-06) Implemented progressive TypeScript type inference using JSDoc to enforce structural stability in the frontend architecture.

---

## 8. Appendix: DB Management Guide (pgAdmin)
- **Path**: `https://chaeyul.uk/pgadmin/`
- **Initial Account**: `adm**@********` / `********`
- **Internal Connection**: Host `db`, Port `5432`, DB `********`, User `********`

---

**[chaeyul.uk Project Construction & Troubleshooting Report Completed]**
