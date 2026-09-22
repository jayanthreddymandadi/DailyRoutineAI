import sqlite3
from datetime import datetime

DB_NAME = "routine.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            task_date TEXT NOT NULL,
            task_time TEXT NOT NULL,
            priority TEXT DEFAULT 'Medium',
            category TEXT DEFAULT 'General',
            repeat_days TEXT DEFAULT '',
            completed INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_task(
    title,
    description,
    task_date,
    task_time,
    priority,
    category,
    repeat_days
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (
            title,
            description,
            task_date,
            task_time,
            priority,
            category,
            repeat_days,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        task_date,
        task_time,
        priority,
        category,
        repeat_days,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            task_date,
            task_time,
            priority,
            category,
            repeat_days,
            completed
        FROM tasks
        ORDER BY task_date, task_time
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def toggle_task(task_id, completed):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
    """, (completed, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


def update_task(
    task_id,
    title,
    description,
    task_date,
    task_time,
    priority,
    category,
    repeat_days
):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET
            title = ?,
            description = ?,
            task_date = ?,
            task_time = ?,
            priority = ?,
            category = ?,
            repeat_days = ?
        WHERE id = ?
    """, (
        title,
        description,
        task_date,
        task_time,
        priority,
        category,
        repeat_days,
        task_id
    ))

    conn.commit()
    conn.close()