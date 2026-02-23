# [Integrated Report] chaeyul.xxx Web Server Project Construction & Troubleshooting Results

**Last Updated**: February 23, 2026 (CMS Lesson Integration, YouTube Translation & Security Completed)
**Target Domain**: `chaeyul.xxx`
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
![Admin Dashboard](admin_layout.png)
*(Figure 1: Admin Dashboard with integrated File Explorer and Security Stats)*

### ④ German Study Center [NEW]
- **Smart Learning Environment**:
    - **A-B Repeat & Speed Control**: Supports precise language learning with user-defined repeat intervals and 0.5x~1.5x speed adjustments.
    - **Real-time Transcript Integration**: Displays transcripts extracted via YouTube API with instant video seeking upon click.
    - **Instant Dictionary**: Provides real-time English and Korean translations via a lookup popup when clicking words in the transcript.
- **Personalized Vocabulary**:
    - **DB-Linked Vocab**: Save and manage encountered words in a personal vocabulary list with one click.
    - **Admin Control**: Easy addition/deletion of study videos via URL in the dashboard.
- **Feature Demo [Study Interface]**:
![Study Interface](study_lookup.png)
*(Figure 2: German Study Center with word selection and real-time translation popup)*
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

---

## 7. Build Walkthrough

### Phase 1: Planning & Setup
- [x] Establishment of project directory structure and Docker environment.

### Phase 2: Backend Development
- [x] API development, JWT Auth, and security (IP blocking) implementation.
- [x] [NEW] Integration of CMS and site settings management APIs.
- [x] [NEW] Completion of YouTube Study Center API, transcript extraction, and vocabulary DB design.

### Phase 3: Frontend Development
- [x] Implementation of main gallery and slideshow.
- [x] [NEW] Integration of dashboard inline editor and settings menu.
- [x] [NEW] Real-time transcript-dictionary interface for German learning.
- [x] [NEW] (2026-02-23) Real-time security stats dashboard and file explorer-based CMS enhancement completed.
- [x] [NEW] (2026-02-23) Drag-and-drop dashboard layout management and smart learning selection logic applied.
- [x] [NEW] (2026-02-23) Automated YouTube transcript translation and integration of 20+ German lesson pages.

---

## 8. Appendix: DB Management Guide (pgAdmin)
- **Path**: `https://chaeyul.xxx/xxxpgadmin/`
- **Initial Account**: `xxxadmin@xxxxadmin.com` / `xxxadmin`
- **Internal Connection**: Host `db`, Port `5432`, DB `photodb`, User `user`

---

**[chaeyul.xxx Project Construction & Troubleshooting Report Completed]**
