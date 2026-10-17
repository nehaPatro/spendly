# Implementation Plan: Database Setup (Step 1)

## Context

The Spendly expense tracker requires a foundational data layer before any authentication, profile, or expense features can be implemented. This step establishes the SQLite database schema, helper functions, and seed data that all future features depend on.

**Why this matters:** A robust database layer with proper constraints (unique emails, foreign keys) and idempotent initialization prevents data corruption and makes subsequent features straightforward to build.

---

## Approach Overview

Implement three database helper functions (`get_db()`, `init_db()`, `seed_db()`) in `database/db.py`, then modify `app.py` to initialize the database on startup.

**Key design decisions:**
- Use raw SQLite (no ORM) with parameterized queries for simplicity and security
- Enable foreign key constraints on every connection (SQLite off by default)
- Make `init_db()` and `seed_db()` idempotent—safe to call multiple times
- Store amounts as REAL (float) to handle rupee decimals properly
- Use werkzeug's `generate_password_hash` for password security

---

## Schema Design

### Users Table
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

### Expenses Table
```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

---

## Implementation Tasks

### 1. Implement `database/db.py`

**Location:** `database/db.py`

**Functions to add:**

#### `get_db()`
- Open connection to `spendly.db` in project root
- Set `row_factory = sqlite3.Row` (allows dict-like row access)
- Execute `PRAGMA foreign_keys = ON` to enforce FK constraints
- Return connection

#### `init_db()`
- Accept optional `db` parameter for testing
- Create `users` table with all columns and constraints
- Create `expenses` table with foreign key to users
- Use `CREATE TABLE IF NOT EXISTS` for idempotency
- Commit changes

#### `seed_db()`
- Accept optional `db` parameter for testing
- Check if users table has data; return early if it does (prevents duplication)
- Insert demo user:
  - name: "Demo User"
  - email: "demo@spendly.com"
  - password: hash of "demo123" using `generate_password_hash`
- Insert 8 sample expenses across the 7 categories:
  - Spread across current month (use YYYY-MM-DD dates)
  - Each must reference demo user's id
  - Include varied amounts and descriptions
  - At least one per category
- Commit all changes

**Critical rules:**
- All SQL queries must use `?` placeholders for parameters
- Never use f-strings or string formatting in SQL
- Hash password using: `from werkzeug.security import generate_password_hash`
- Categories must be exactly: Food, Transport, Bills, Health, Entertainment, Shopping, Other

---

### 2. Modify `app.py`

**Location:** `app.py`

**Changes:**
- Add import: `from database.db import get_db, init_db, seed_db`
- Add startup code after app creation:
  ```python
  with app.app_context():
      init_db()
      seed_db()
  ```
- This ensures database is ready before any routes execute

---

## Implementation Sequence

1. **Write `database/db.py`:**
   - Import sqlite3 and werkzeug.security
   - Implement `get_db()` (simple connection setup)
   - Implement `init_db()` (create tables)
   - Implement `seed_db()` (insert demo data)

2. **Update `app.py`:**
   - Add imports from database.db
   - Call init_db() and seed_db() in app context

3. **Verify:**
   - Run app: `python app.py`
   - Check `spendly.db` is created in project root
   - Verify schema: `sqlite3 spendly.db ".schema"`
   - Verify demo data: `sqlite3 spendly.db "SELECT * FROM users; SELECT * FROM expenses;"`

---

## Critical Files

- `database/db.py` — implement all functions
- `app.py` — add startup initialization

---

## Testing Considerations

**Manual verification:**
- App starts without errors
- `spendly.db` file exists in project root
- Both tables have correct schema and constraints
- Demo user and 8 expenses are seeded
- Running app twice doesn't duplicate data

**Future test hooks:**
- Test database isolation (each test gets fresh DB)
- Test constraint enforcement (duplicate email should fail)
- Test foreign key enforcement (invalid user_id should fail)

---

## Dependencies

- **Standard library:** `sqlite3`
- **Already installed:** `werkzeug.security.generate_password_hash`
- **No new packages needed**

---

## Definition of Done

- [ ] `get_db()` returns working connection with row_factory and foreign keys enabled
- [ ] `init_db()` creates both tables safely, idempotent
- [ ] `seed_db()` inserts demo user and 8 expenses, prevents duplicates on repeat runs
- [ ] `app.py` imports and calls init_db(), seed_db() on startup
- [ ] App starts without errors
- [ ] Database file exists at project root
- [ ] All queries use parameterized SQL (no string formatting)
- [ ] Foreign key and unique email constraints are enforced
