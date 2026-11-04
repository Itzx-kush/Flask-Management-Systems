import os
import sqlite3
from flask import g, current_app


def get_db(db_path=None):
    """
    Get a database connection for the current application context.
    Reuses existing connection stored in Flask's g object if available.
    """
    if 'db' not in g:
        target_path = db_path or current_app.config.get('DATABASE')
        # Ensure parent directory exists
        parent_dir = os.path.dirname(target_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        g.db = sqlite3.connect(target_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db


def close_db(e=None):
    """Closes the database connection if open."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app=None, db_path=None):
    """
    Initialize SQLite database tables for Students and Employees.
    Tables are created if they do not exist, ensuring data persistence across restarts.
    """
    if app:
        target_path = db_path or app.config.get('DATABASE')
    else:
        target_path = db_path or current_app.config.get('DATABASE')

    parent_dir = os.path.dirname(target_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Practical 3: Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            semester TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Practical 4: Employees Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL UNIQUE,
            employee_name TEXT NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            salary REAL NOT NULL,
            joining_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Seed initial demonstration data if tables are empty
    cursor.execute("SELECT COUNT(*) AS count FROM students")
    if cursor.fetchone()['count'] == 0:
        cursor.executemany("""
            INSERT INTO students (student_name, roll_number, department, email, phone, semester)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ('Aarav Sharma', '2023CS0101', 'Computer Science & Engineering', 'aarav.sharma@example.edu', '9876543210', '6th Semester'),
            ('Diya Patel', '2023IT0204', 'Information Technology', 'diya.patel@example.edu', '9812345678', '4th Semester'),
            ('Rohan Varma', '2023EC0312', 'Electronics & Communication', 'rohan.varma@example.edu', '9898989898', '6th Semester'),
            ('Ananya Iyer', '2023ME0405', 'Mechanical Engineering', 'ananya.iyer@example.edu', '9765432109', '2nd Semester'),
        ])

    cursor.execute("SELECT COUNT(*) AS count FROM employees")
    if cursor.fetchone()['count'] == 0:
        cursor.executemany("""
            INSERT INTO employees (employee_id, employee_name, department, designation, email, phone, salary, joining_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ('EMP-1001', 'Vikramaditya Rao', 'Engineering', 'Lead Systems Architect', 'vikram.rao@enterprise.org', '9876501234', 125000.0, '2021-03-15'),
            ('EMP-1002', 'Meera Nambiar', 'Human Resources', 'HR Operations Manager', 'meera.nambiar@enterprise.org', '9845012345', 85000.0, '2022-07-01'),
            ('EMP-1003', 'Karan Singhal', 'Finance', 'Senior Financial Analyst', 'karan.singhal@enterprise.org', '9823012345', 92000.0, '2023-01-10'),
            ('EMP-1004', 'Pooja Kulkarni', 'Quality Assurance', 'Lead QA Automation Engineer', 'pooja.kulkarni@enterprise.org', '9811012345', 78000.0, '2023-09-18'),
        ])

    conn.commit()
    conn.close()


def query_db(query, args=(), one=False):
    """Helper to query the database with parameterized inputs."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=(), commit=True):
    """Helper to execute an INSERT, UPDATE, or DELETE query with parameterized inputs."""
    db = get_db()
    cur = db.execute(query, args)
    if commit:
        db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id
