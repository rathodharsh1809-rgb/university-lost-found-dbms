# University Lost & Found Department &mdash; DBMS Academic Project

A clean, compact, full-stack academic DBMS project demonstrating **Three-Level Architecture**, **Layer Isolation / Data Independence**, and **SQLite Database Operations** using Python Flask and modern HTML/CSS.

---

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Minimalist, Responsive Full-Screen Layout)
- **Backend**: Python 3, Flask
- **Database**: SQLite 3 (`database/lost_and_found.db`)
- **Inspection Tool**: DB Browser for SQLite

---

## Project Structure

```
University-Lost-and-Found/
│
├── frontend/                     # User Interface & presentation files
│   ├── templates/                # HTML Jinja templates (base, browse, report, etc.)
│   ├── static/                   # Static assets (css/style.css, js, images)
│   └── README.md
│
├── backend/                      # Python Flask application & business logic
│   ├── app/
│   │   ├── routes/               # HTTP Request handlers & routing (Zero SQL)
│   │   ├── services/             # Business logic & notification workflows
│   │   ├── repositories/         # Data Access Layer (All SQL operations)
│   │   ├── models/               # Conceptual entity models
│   │   └── utils/                # SQLite connection manager & DB bootstrap
│   ├── config.py                 # Centralized path & app configuration
│   ├── main.py                   # Backend entry point
│   ├── requirements.txt          # Python dependencies
│   └── README.md
│
├── database/                     # SQLite Database & SQL scripts
│   ├── lost_and_found.db         # Physical SQLite database file
│   ├── schema.sql                # Table definitions, PK/FK constraints & indexes
│   ├── seed.sql                  # Initial demonstration seed data
│   └── queries.sql               # Reference SQL queries (INSERT, SELECT, UPDATE, JOIN)
│
├── documents/                    # Academic Documentation
│   ├── README.md
│   ├── ER_Diagram/               # Entity-Relationship diagram & cardinality
│   ├── Architecture/             # 3-Level Architecture & Data Independence docs
│   ├── SQL/                      # SQL operation reference & explanations
│   └── Screenshots/              # UI walkthrough & DB Browser captures
│
├── main.py                       # Root launcher
├── requirements.txt              # Root requirements file
└── README.md
```

---

## Features & Master Operations Dashboard

The system includes a dedicated **Master Operations & DBMS Analytics Dashboard** (`/` or `/dashboard`):

- **4 Key Performance Indicator (KPI) Cards**:
  - Total Lost Reports with status breakdown (`SEARCHING`, `FOUND`, `COLLECTED`)
  - Found Items Inventory (`AVAILABLE`, `CLAIMED`, `DISPOSED`)
  - Recovery / Resolution Rate percentage gauge
  - Community Metrics (Students, Faculty, Admins) & notification logs
- **Visual Analytics**:
  - Item category distribution progress bars
  - Campus activity hotspot rankings
- **Multi-Tab Detailed Data Explorer**:
  - **Lost Items Registry**: Complete details with student details, location, status, and timestamps
  - **Found Items Inventory**: Full catalog of turned-in items with quick removal/management actions
  - **Registered Users & Roles**: Complete directory of students, faculty, and administrators
  - **Notification History**: Audit trail of system messages and student alerts
  - **Physical DBMS Architecture**: Live SQLite telemetry (`lost_and_found.db`, file size, page size, page count, WAL journal mode, and raw table schemas with row counts)
- **Instant Live Search**: Real-time client-side filter across all records and tables without page reloads.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```
*Alternatively, you can run:*
```bash
python backend/main.py
```

### 3. Open in Browser
Open: **`http://127.0.0.1:5000`**

---

## Database Inspection with DB Browser for SQLite

1. Open **DB Browser for SQLite**.
2. Open database file: `database/lost_and_found.db`.
3. Under **Database Structure**, view tables: `users`, `lost_items`, `found_items`, `notifications`.
4. Under **Browse Data**, inspect live records.
5. Under **Execute SQL**, execute queries from `database/queries.sql`.

---

## 🚀 Cloud Deployment

### Deploy on Render (Free & Recommended)
1. Sign up/Log in at [render.com](https://render.com).
2. Click **New +** &rarr; **Web Service**.
3. Connect your GitHub repository: `https://github.com/dkr4102/university-lost-found-dbms`.
4. Render will automatically detect `render.yaml` or use the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
5. Click **Deploy Web Service**.

### Deploy on Railway
1. Go to [railway.app](https://railway.app).
2. Click **New Project** &rarr; **Deploy from GitHub repo**.
3. Select `dkr4102/university-lost-found-dbms`.
4. Railway automatically detects `Procfile` / `requirements.txt` and deploys instantly.

