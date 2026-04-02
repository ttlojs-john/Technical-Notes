# [Phase 6] Operational Monitoring Guide 

**Objective**: This document serves as a practical, hands-on guide to operating the centralized monitoring stacks (Grafana, Prometheus, Loki) deployed for observing the `chaeyul.uk` infrastructure.

## 📌 1. Tool Core Overview

- **Grafana**: The principal visual command center. It converts raw, complex time-series telemetry (Memory, CPU patterns) and text logs into highly legible, customizable charts and dashboards.
- **Prometheus**: The core metric database. It actively scrapes and stores raw numeric performance indicators from the host node and individual Docker containers.
- **Loki & Promtail**: The central log aggregation engine. Designed specifically to gather and index system logs and security checkpoints (like `auth.log`) allowing for massive-scale text search algorithms.

---

## 📊 2. Grafana Operations

![cAdvisor Container Monitoring Dashboard](./archive/cadvisor_monitoring_dashboard_20260308.png)
*<Figure: Real-time cAdvisor Dashboard showcasing immediate Docker container resource usage>*

### 1) Initial Access & Setup
* **Endpoint**: `https://[Domain]/grafana/` (Alternatively, click the 'Grafana ↗' redirect button inside the admin portal).
* Standard Boot Credentials: `admin` / `admin` (You will be prompted to supply a secure password immediately upon initial boot).

### 2) Bridging Data Sources
Before rendering dashboards, Grafana must be pointed toward the data reservoirs.
1. Navigate via the Hamburger Menu (☰) -> **Connections** -> **Data sources**.
2. **Link Prometheus**: In the URL field, input `http://prometheus:9090` and finalize by clicking the blue **[Save & test]** button at the footer (This routes internally through the Docker network).
3. **Link Loki**: In the URL field, input `http://loki:3100` and confirm with **[Save & test]**.

### 3) Importing Readymade Dashboards
You can bypass manual layout designing by importing globally recognized community templates within seconds.
1. Hamburger Menu (☰) -> **Dashboards** -> Select **[New]** dropdown -> **[Import]**.
2. To monitor primary server hardware, type **`1860`** (Node Exporter metric template) or **`14282`** (cAdvisor for isolated container tracking) into the ID box and hit **[Load]**.
3. Under the Data Source dropdown at the bottom, select the **Prometheus** link you created previously and click **[Import]**.

![Grafana Real-time Monitoring Dashboard](./archive/grafana_success.png)
*<Figure: Live Grafana Monitoring Console surfacing active Node exporter metrics post-import>*

---

## 🔍 3. Prometheus Direct Queries

* **Endpoint**: `https://[Domain]/prometheus/`
* The native Prometheus interface is typically utilized for low-level debugging or querying raw metrics that aren't mapped onto Grafana endpoints.
* *Example*: Typing `node_cpu_seconds_total` into the search bar and clicking [Execute] will return the cumulative raw CPU uptime metrics for algorithmic cross-checking.

---

## 🚨 4. Security Sweeps utilizing Loki

Loki acts as the supreme tool for auditing unauthorized intrusion attempts via log exploration.

### Log Deep-Dives (Explore Tab)
1. In Grafana, select Hamburger Menu (☰) -> **Explore**.
2. Swap the top-left Data Source dropdown to **Loki**.
3. **Filtering for Hostile Logins (Brute-force Hunting)**:
   - Instead of clicking the Label browser, utilize the direct query input:
   - `{job="varlogs", filename="/var/log/auth.log"} |= "Failed password"`
   - Hitting `Run query` will instantly filter out thousands of normal logs, isolating exclusively failed SSH or terminal access attempts allowing you to pinpoint hostile IPs.

### Appending Terminal Panels to Dashboards
You can fuse log streams directly onto dynamic visual dashboards (like `1860`).
1. Click **[Add panel]** -> **[Add new panel]** on the top right of your dashboard.
2. Select **Loki** as the target source and enter `{job="varlogs"}`.
3. Switch the right-side Visualization style from 'Time series' to **Logs** and click Apply. You now have a unified pane mirroring both hardware stress-levels and security terminologies side-by-side.
