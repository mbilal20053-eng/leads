# Netlify & Production Deployment Architecture Guide
**Lead Engine PRO — High-Performance Lead Management Platform**

---

## 1. Executive Deployment Analysis

You requested to deploy this application on **Netlify** while keeping the full lead management and newly created **Import Leads / Ingestion Engine** fully operational.

Before deploying, it is critical to understand the architectural differences between your local Windows environment (`D:\leads`) and a cloud serverless environment like Netlify.

### Fundamental Constraints of Netlify Serverless Functions:

1. **Ephemeral Filesystem (`/tmp`):**
   Netlify Functions run on AWS Lambda containers. Any files written to the local disk or `/tmp` are wiped as soon as the container spins down (within minutes). A local database or uploaded Parquet files saved on Netlify's local disk **will not persist**.
2. **6 MB Request Payload Limit:**
   Netlify serverless functions enforce a strict **6 MB payload limit** for incoming HTTP requests. Attempting to upload a 20 MB or 50 MB CSV file directly to a Netlify Function results in an immediate `413 Payload Too Large` error.
3. **Execution Timeout (10s – 26s):**
   Netlify Functions have a hard timeout (10 seconds on the Free tier, 26 seconds on Pro). Large CSV parsing, deduplication across millions of rows, and columnar Parquet writing can easily exceed this window.
4. **Local Windows Storage (`D:\leads`):**
   Your 62.67 GB portfolio on `D:\leads` resides physically on your local laptop. Netlify servers cannot access your local drive without a network backend.

---

## 2. Recommended Production Architectures

To ensure your application retains all imported datasets, achieves sub-second queries across millions of rows, and supports large multi-file CSV uploads without failing, we recommend two proven architecture patterns:

### Pattern A: Hybrid Jamstack (Recommended for Production)
* **Frontend:** Hosted on **Netlify CDN** (instant global caching, SSL, continuous Git deployments).
* **Backend:** Hosted on **Render, Railway, Fly.io, or AWS App Runner** using the existing `Dockerfile` with a **Persistent Volume**.
* **Database & Storage:** Native **DuckDB + Parquet** on the persistent volume.
* **How It Connects:** Netlify proxies all `/api/*` calls to the persistent backend using `netlify.toml` redirects.

```
[User Browser]
      │
      ├───> Static Assets (HTML, CSS, JS) ──────> [Netlify Global CDN]
      │
      └───> API & Multi-CSV Uploads (/api/*) ───> [Netlify Redirect Proxy]
                                                          │
                                                          ▼
                                            [Persistent Backend Container]
                                              (Render / Railway / Fly.io)
                                              • Full DuckDB C++ Engine
                                              • 100 MB+ Upload Streaming
                                              • Parquet Ingestion & Storage
```

**Why this is best:**
- Identical performance to your local laptop (< 50ms query times).
- Uploads up to 100 MB+ work seamlessly without timeout or 6 MB payload limits.
- Zero code modifications required between local and cloud environments.
- Completely free or low-cost ($0–$7/mo on Railway/Render).

---

### Pattern B: Fully Serverless (Netlify + Cloudflare R2 + MotherDuck)
If you require a 100% serverless deployment without running an ongoing container:
* **Frontend:** Netlify Static Site.
* **Upload Storage:** Direct browser upload to **Cloudflare R2** or **AWS S3** via presigned URLs (bypasses Netlify's 6 MB limit).
* **Database Engine:** **MotherDuck** (Cloud DuckDB). Parquet files are read directly from S3/R2 or MotherDuck tables.
* **Serverless Functions:** Netlify Functions handle authentication and orchestration.

---

## 3. Step-by-Step Deployment Instructions (Pattern A)

### Step 1: Deploy the Persistent Backend (Railway or Render)

1. Create an account on [Railway.app](https://railway.app) or [Render.com](https://render.com).
2. Connect your GitHub repository: `https://github.com/mbilal20053-eng/leads.git`.
3. Configure the service:
   - **Build Command:** `pip install -r gui/requirements.txt`
   - **Start Command:** `python gui/app.py`
   - **Environment Variables:**
     ```ini
     APP_ENV=production
     HOST=0.0.0.0
     PORT=5000
     LEADS_DATA_DIR=/data
     MAX_CONTENT_LENGTH=104857600
     ```
4. Attach a **Persistent Volume**:
   - Mount path: `/data`
   - Size: 10 GB – 50 GB
5. Copy your public production URL (e.g., `https://leads-engine-api.up.railway.app`).

### Step 2: Deploy the Frontend to Netlify

1. Log in to [Netlify](https://app.netlify.com).
2. Click **"Add new site"** → **"Import an existing project"** → select **GitHub**.
3. Choose `mbilal20053-eng/leads`.
4. Configure Netlify build settings:
   - **Base directory:** Leave empty (root)
   - **Build command:** `# No build step required for Vanilla JS/CSS`
   - **Publish directory:** `gui/templates` (or root where `index.html` resides)
5. Set Netlify Environment Variables:
   - Go to **Site Configuration** → **Environment variables**
   - Add:
     ```ini
     BACKEND_URL=https://leads-engine-api.up.railway.app
     APP_ENV=production
     ```
6. Update the redirect in `netlify.toml`:
   ```toml
   [[redirects]]
     from = "/api/*"
     to = "https://leads-engine-api.up.railway.app/api/:splat"
     status = 200
     force = true
   ```
7. Click **Deploy Site**. Netlify will provide your live URL (e.g. `https://leads-engine-pro.netlify.app`).

---

## 4. Local Development vs. Production Configuration

The codebase includes an automatic environment separation layer:

| Component | Local Development (Windows) | Production (Cloud) |
|:---|:---|:---|
| **Storage Directory** | `D:\leads\imported_datasets` | `/data/imported_datasets` (via `LEADS_DATA_DIR`) |
| **Parquet Engine** | Local DuckDB in-memory + file scan | Persistent DuckDB on mounted volume |
| **Upload Size Limit** | 100 MB per file | Configurable via `MAX_CONTENT_LENGTH` |
| **API Host** | `localhost:5000` | Netlify `/api/*` reverse proxy |
| **Security Secrets** | None stored in Git | Configured securely in hosting dashboards |

---

## 5. Security & Reliability Safeguards Implemented

1. **No Credentials in Frontend Code:** All database connections, paths, and environment tokens are managed strictly on the backend.
2. **Formula Injection Protection:** CSV exports automatically sanitize any cell beginning with `=`, `+`, `-`, `@`, `\t`, or `\r` to prevent spreadsheet code execution.
3. **Staging & Atomic Ingestion:** Multi-file imports are staged and validated before committing to Parquet. A corrupt row or failed file will not damage active tables.
4. **Audit Trail Logging:** Every import, rename, and deletion event is appended to `audit_log.json`.
