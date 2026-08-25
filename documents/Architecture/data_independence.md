# Layer Isolation & Data Independence

Data Independence is the ability to modify schema definition in one level without affecting the schema definition in the next higher level.

```
Frontend (HTML/CSS/JS)
         ↓  (Zero SQL queries)
Backend Routes (Flask Blueprints)
         ↓  (Input validation)
Application Services
         ↓  (Business logic & transactions)
Data Repositories
         ↓  (Only layer executing SQL)
SQLite Database (database/lost_and_found.db)
```

---

## 1. Physical Data Independence
- **Definition**: The capacity to change the internal schema (storage structures, disk page size, file paths, or adding secondary indexes) without altering the conceptual schema or application programs.
- **Implementation in Project**:
  - Secondary B-Tree indexes (`CREATE INDEX idx_lost_items_user ON lost_items(user_id)`) are added in `database/schema.sql`.
  - Database file location is centralized in `backend/config.py`.
  - Adding or modifying indexes in SQLite requires **zero changes** to frontend templates or backend routes.

---

## 2. Logical Data Independence
- **Definition**: The capacity to modify the conceptual schema (adding new tables or attributes) without forcing rewrites of existing external views or user queries.
- **Implementation in Project**:
  - The Student View interacts exclusively with service methods (`get_student_reports()`).
  - If administrators add new internal audit attributes to `found_items` or `lost_items`, the student interface continues functioning without modification.

---

## 3. Strict Code Guarantees
1. **Frontend (`frontend/`)**: Contains zero SQL queries and zero SQLite connection drivers.
2. **Backend Routes (`backend/app/routes/`)**: Does not contain SQL strings; delegates all operations to Services.
3. **Services (`backend/app/services/`)**: Orchestrates business rules and status transitions without touching SQL syntax.
4. **Repositories (`backend/app/repositories/`)**: The sole layer responsible for SQL execution against SQLite.
