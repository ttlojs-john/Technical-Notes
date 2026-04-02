# [Phase 1] chaeyul.uk Initial Web Server Setup & Core Features

**Project Overview**: This project aims to build a dedicated web server for managing and streaming premium media (photos, videos, audio). It emphasizes a UI optimized for high-quality media storage and a highly secure backend architecture.

## 📌 1. Infrastructure Operation & Management Architecture

### Docker Compose Environment
- **Frontend**: Node.js (Express) - Ports 80/443 mapped, serving static files, acting as a reverse proxy, and providing API Rate Limiting.
- **Backend**: Python (FastAPI) - REST API server managing media processing and page business logic.
- **Database**: PostgreSQL 15 - Persistent storage for system metadata and user accounts.
- **Infrastructure**: Cloudflare Proxy & Linux environment for secure external access and SSL offloading.

## 🌟 2. Core Implementations

### User Domain & Co-branding
- Secured main domain (`chaeyul.uk`) by strictly blocking direct IP connections.
- Rebranded to `CHAEEUN & CHAEYUL`, supporting dynamic visual configurations directly via the dashboard.

### Admin Dashboard & CMS Enhancements
- Introduced an inline code editor within the admin UI, enabling real-time adjustments to HTML/CSS files without server restarts (CMS).
- State persistency configured through a unified `settings.json` module.
- Modernized the UI layout utilizing a cohesive sidebar navigation.
- Elevated login security to enterprise levels by mandating 2FA (Google Authenticator) for administrators.

![Admin Dashboard Interface](./admin_layout.png)
*<Figure: Admin Dashboard Interface with CMS and Security Stats>*

![2FA Google OTP Setup UI](./2fa_google_otp_setup_20260308.png)
*<Figure: QR Code-based 2FA Configuration UI for Enhanced Login Security>*

### German Study Center (YouTube Interactive Interface)
- Leveraged the YouTube API to extract dual-subtitles (DE/EN) dynamically, integrated with instant dictionary lookups.
- Implemented personalized A-B loop configurations with local storage persistence.
- Constructed mobile-friendly foundations, including native background playback options.

![Dark/Light Theme Switcher System](./theme_switcher_ui.png)
*<Figure: Dark/Light Transition Interface Responsive to System Themes>*

![Study Interface Demo](./study_lookup.png)
*<Figure: Word Selection and Real-time Translation Popup in German Study Center>*

![Mobile Study & Background Playback](./mobile_optimized_study.png)
*<Figure: Mobile-Optimized Layout and Lock Screen Control UI>*

### Media Gallery (Masonry Style)
- Built a premium Masonry layout utilizing CSS Columns.
- Integrated automated EXIF data parsers for year-based multimedia filtering alongside video hover previews.

![Premium Masonry Gallery Layout](./premium_gallery_masonry.png)
*<Figure: Premium Photo Gallery Applying Masonry Techniques>*

## 🛠 3. Troubleshooting Log

- **Login Modal Rendering Conflict**: A recurring issue where the login screen forcefully overlayed the landing page was fixed. Duplicate inline CSS (`display: flex`) was eradicated in favor of JS-only state manipulation.
- **Backend Model Schema Mismatch**: Deployed an automated `migrate.py` snippet to synchronize missing database columns (`telegram_chat_id`, etc.) across containers without data losses.
- **Brute-Force Attack Mitigation**: Instead of delegating security solely to the backend, established a robust first line of defense using Node.js `express-rate-limit`. This efficiently blocked malicious floods and preserved Real-IP tracking behind proxy layers.

---
> [!NOTE]
> This document records the **Phase 1 (Initial Setup & Core System)** prior to the major expansions seen during V3/V4 module developments. Subsequent milestones are covered in the respective Phase chapters.
