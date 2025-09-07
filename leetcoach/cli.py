from __future__ import annotations
import csv
import typer
from rich.table import Table
from rich.console import Console
from . import db
from .scheduler import priority

app = typer.Typer(help="LeetCoach-Lite: spaced repetition for DSA practice.")
console = Console()

@app.command()
def seed(csv_path: str = "sample_problems.csv"):
    """Import problems from a CSV with columns: title,tag,difficulty"""
    conn = db.connect()
    with open(csv_path, newline="", encoding="utf-8") as f:
        for title, tag, difficulty in csv.reader(f):
            db.add_problem(conn, title.strip(), tag.strip(), difficulty.strip().lower())
    console.print("[green]Seeded problems from CSV.[/green]")

@app.command()
def add(title: str, tag: str = "", difficulty: str = typer.Option("easy", help="easy|medium|hard")):
    conn = db.connect()
    db.add_problem(conn, title, tag, difficulty.lower())
    console.print(f"[green]Added:[/green] {title} ({difficulty})")

@app.command()
def due():
    """List problems due now, ordered by priority."""
    conn = db.connect()
    rows = db.list_due(conn)
    rows = sorted(rows, key=lambda r: priority(r[4], r[3]))  # box, difficulty
    if not rows:
        console.print("[yellow]Nothing due. 🎉[/yellow]")
        return
    t = Table("id", "title", "tag", "diff", "box", "next_due")
    for r in rows:
        t.add_row(str(r[0]), r[1], r[2], r[3], str(r[4]), str(r[5]))
    console.print(t)

@app.command()
def review(prob_id: int, correct: bool = typer.Option(True, help="Pass True if solved correctly")):
    """Update one problem after a review."""
    conn = db.connect()
    db.update_after_review(conn, prob_id, correct)
    console.print("[cyan]Updated.[/cyan]")

@app.command()
def stats():
    conn = db.connect()
    s = db.all_stats(conn)
    console.print({f"box_{k}": v for k, v in s.items()})

def main():
    app()

if __name__ == "__main__":
    main()
