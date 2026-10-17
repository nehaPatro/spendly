import sqlite3
import os
from werkzeug.security import generate_password_hash


def get_db():
    db = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spendly.db'))
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db():
    db = get_db()

    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    db.execute('''
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
    ''')

    db.commit()
    db.close()


def seed_db():
    db = get_db()

    # Check if data already exists
    cursor = db.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        db.close()
        return

    # Insert demo user
    hashed_password = generate_password_hash('demo123')
    db.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', hashed_password)
    )

    # Get the demo user's id
    cursor = db.execute('SELECT id FROM users WHERE email = ?', ('demo@spendly.com',))
    user_id = cursor.fetchone()[0]

    # Insert 8 sample expenses
    expenses = [
        (user_id, 500, 'Food', '2026-10-01', 'Groceries from market'),
        (user_id, 150, 'Transport', '2026-10-05', 'Uber ride to office'),
        (user_id, 2000, 'Bills', '2026-10-08', 'Electricity bill'),
        (user_id, 500, 'Health', '2026-10-10', 'Medicine and vitamins'),
        (user_id, 800, 'Entertainment', '2026-10-12', 'Movie tickets'),
        (user_id, 1200, 'Shopping', '2026-10-15', 'Winter clothes'),
        (user_id, 300, 'Other', '2026-10-18', 'Random purchase'),
        (user_id, 750, 'Food', '2026-10-20', 'Restaurant dinner'),
    ]

    db.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        expenses
    )

    db.commit()
    db.close()
