from __future__ import annotations
import sqlite3, pathlib, datetime as dt

DB_PATH = pathlib.Path.home() / ".leetcoach.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS problems(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  tag TEXT,
  difficulty TEXT CHECK(difficulty IN ('easy','medium','hard')) NOT NULL,
  box INTEGER NOT NULL DEFAULT 0,
  last_review TIMESTAMP,
  next_due TIMESTAMP
);
"""

def connect(db_path: pathlib.Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute(SCHEMA)
    return conn

def add_problem(conn, title: str, tag: str, difficulty: str):
    now = dt.datetime.utcnow()
    conn.execute(
        "INSERT INTO problems(title, tag, difficulty, box, last_review, next_due) VALUES (?,?,?,?,?,?)",
        (title, tag, difficulty, 0, None, now),
    )
    conn.commit()

def list_due(conn):
    now = dt.datetime.utcnow()
    cur = conn.execute(
        "SELECT id,title,tag,difficulty,box,next_due FROM problems WHERE next_due <= ? ORDER BY next_due ASC",
        (now,),
    )
    return cur.fetchall()

def update_after_review(conn, prob_id: int, correct: bool):
    days_by_box = [1, 2, 4, 7, 15]
    cur = conn.execute("SELECT box FROM problems WHERE id=?", (prob_id,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Problem not found")
    box = row[0]
    box = min(box + 1, 4) if correct else max(box - 1, 0)
    next_due = dt.datetime.utcnow() + dt.timedelta(days=days_by_box[box])
    conn.execute(
        "UPDATE problems SET box=?, last_review=?, next_due=? WHERE id=?",
        (box, dt.datetime.utcnow(), next_due, prob_id),
    )
    conn.commit()

def all_stats(conn):
    cur = conn.execute("SELECT box, COUNT(*) FROM problems GROUP BY box ORDER BY box;")
    return dict(cur.fetchall())
