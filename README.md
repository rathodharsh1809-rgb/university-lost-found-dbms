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

## Architectural Data Flow

$$\text{Frontend (HTML/CSS)} \longrightarrow \text{Backend Routes} \longrightarrow \text{Services} \longrightarrow \text{Repositories} \longrightarrow \text{SQLite DB}$$

- **Zero SQL in Frontend**: Presentation layer is completely decoupled from database access.
- **Single Source of Truth**: All SQL queries are encapsulated inside `backend/app/repositories/lost_found_repo.py`.
- **Centralized Configuration**: `backend/config.py` manages all database and template paths.

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
