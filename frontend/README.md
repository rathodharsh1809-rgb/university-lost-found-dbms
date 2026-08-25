# Frontend &mdash; University Lost & Found Department

This directory contains all client-side presentation assets and templates.

## Structure

```
frontend/
├── templates/
│   ├── base.html             # Main layout, compact navigation & footer
│   ├── browse.html           # Browse campus recovered items view
│   ├── report.html           # Report lost item form
│   ├── my_reports.html       # Student's submitted reports table
│   ├── notifications.html    # Student inbox updates
│   └── admin.html            # Department administrator dashboard
└── static/
    ├── css/
    │   └── style.css         # Modern compact collegiate stylesheet
    ├── js/
    └── images/
```

## Architectural Isolation Rule
- The frontend contains **zero SQL queries** and **no direct database access**.
- It communicates exclusively with the backend routes via Jinja templates and HTTP form submissions.
