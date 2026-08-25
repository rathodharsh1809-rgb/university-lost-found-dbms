# Backend &mdash; University Lost & Found Department

This directory contains the Python Flask application, business logic, repositories, and centralized database configuration.

## Directory Structure

```
backend/
├── app/
│   ├── routes/          # Flask Blueprints & HTTP handlers (Zero SQL)
│   ├── services/        # Business logic, status updates & validation
│   ├── repositories/    # Data Access Layer (All SQL operations: INSERT, SELECT, UPDATE, JOIN)
│   ├── models/          # Conceptual entity dataclasses
│   └── utils/           # SQLite connection & database initialization
│
├── config.py            # Central path & application configuration
├── main.py              # Application entry point & factory
├── requirements.txt     # Python dependencies
└── README.md
```

## Architectural Decoupling
- **Routes** (`app/routes/`) delegate processing exclusively to **Services** (`app/services/`).
- **Services** invoke **Repositories** (`app/repositories/`) to perform SQL operations.
- **Repositories** access the database via the connection manager in `app/utils/db.py`.
- **Frontend** templates in `../../frontend/templates` are rendered directly without exposing SQL.
