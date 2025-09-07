
[![CI](https://github.com/Fada-Mannie/leetcoach-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/Fada-Mannie/leetcoach-lite/actions/workflows/ci.yml)

*A spaced-repetition CLI to make Data Structures & Algorithms practice actually stick.*

> Built by **Emmanuel Akwasi Opoku** — [@Fada-Mannie](https://github.com/Fada-Mannie).  
> GSU CS student focused on backend, AI, and practical developer tools. Open to SWE internships & collabs.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-%E2%89%A53.10-blue">
  <img alt="Typer" src="https://img.shields.io/badge/CLI-Typer-informational">
  <img alt="Rich" src="https://img.shields.io/badge/Terminal-Rich-brightgreen">
  <img alt="Tests" src="https://img.shields.io/badge/Tests-pytest-success">
</p>

LeetCoach-Lite tracks coding problems in a local SQLite database and schedules reviews using a simple **Leitner box** system (spaced repetition).  
It’s small, clean, and intentionally practical—perfect for a beginner-friendly portfolio repo that still shows real-world skills: packaging, CLI UX, data modeling, a unit test, and CI.

---



```bash
# 1) Create & activate a virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2) Install
pip install -r requirements.txt
python -m pip install -e .

# 3) Seed a few sample problems, then see what's due
leetcoach seed
leetcoach due

# 4) Review a problem (mark correct/incorrect)
leetcoach review 1 --correct true

# 5) Check simple stats
leetcoach stats
```

>  The data is stored at: `~/.leetcoach.db` (SQLite). Delete that file to reset.

---

## What this project demonstrates (for recruiters)
- Clean Python package layout with an installable CLI (`pyproject.toml`).
- **SQLite** persistence + minimal data model.
- Simple **scheduling algorithm** (Leitner boxes).
- A **unit test** (`pytest`) and ready-to-run **GitHub Actions** workflow.
- Clear README, typed code, and an obvious path to extend (web API / dashboard).

---

##  Feature Overview
- **Add problems** manually or **seed** from CSV.
- **Due queue** ordered by priority (box number + difficulty bias).
- **Review updates** move problems between boxes and schedule the next due date.
- **Stats** summarize how many problems sit in each box.

---

## Project Structure
```
leetcoach-lite/
├─ leetcoach/
│  ├─ __init__.py
│  ├─ cli.py          # Typer CLI commands
│  ├─ db.py           # SQLite helpers + schema
│  └─ scheduler.py    # Leitner priority logic
├─ tests/
│  └─ test_scheduler.py
├─ sample_problems.csv
├─ requirements.txt
├─ pyproject.toml
├─ .github/workflows/ci.yml
└─ README.md
```

---

##  CLI Usage

### Seed from CSV
```bash
leetcoach seed                      # uses sample_problems.csv by default
leetcoach seed --csv-path my.csv    # (alt. path if you add an option later)
```

### Add one problem
```bash
leetcoach add "Two Sum" --tag arrays --difficulty easy
```

### See what's due (now)
```bash
leetcoach due
# id | title                         | tag   | diff   | box | next_due
#  1 | Two Sum                       | arrays| easy   | 0   | 2025-01-01 12:00:00
```

### Review + schedule next time
```bash
leetcoach review 1 --correct true    # moves box up (max 4) and reschedules
```

### Stats
```bash
leetcoach stats
# {'box_0': 1, 'box_1': 3, 'box_2': 0, 'box_3': 1, 'box_4': 0}
```

Run `leetcoach --help` for the full command list.

---

##  How the Scheduling Works (Leitner)
Each problem sits in a **box** (0–4). After a review:
- **Correct:** move up one box (max **4**).
- **Incorrect:** move down one box (min **0**).

Default intervals by box (days): `[1, 2, 4, 7, 15]`  
You can tweak this in `db.update_after_review`.

A tiny difficulty bias nudges **harder problems** to appear earlier when boxes tie.

---

## Data Model (SQLite)
Table: `problems`
```
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
tag TEXT,
difficulty TEXT CHECK(difficulty IN ('easy','medium','hard')) NOT NULL,
box INTEGER NOT NULL DEFAULT 0,
last_review TIMESTAMP,
next_due TIMESTAMP
```
Database path: `~/.leetcoach.db`

---

## 🧪 Testing & CI
```bash
pytest -q
```
The repo includes a **GitHub Actions** workflow (`.github/workflows/ci.yml`) that runs tests on every push/PR.

**CI badge:** [![CI](https://github.com/Fada-Mannie/leetcoach-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/Fada-Mannie/leetcoach-lite/actions/workflows/ci.yml)

> Add more tests! Easy targets: CLI behaviors (via Typer’s testing utilities), DB functions, and edge cases in scheduling.

---

## 🛣️ Roadmap (Good first issues)
- [ ] **Streamlit** dashboard for the due queue and stats.
- [ ] **FastAPI** endpoints: `GET /due`, `POST /review`, `POST /add`.
- [ ] Import and store **LeetCode links**.
- [ ] Export **ICS calendar** of upcoming reviews.
- [ ] Add **Dockerfile** for one-command run.
- [ ] Add **type hints** everywhere + `mypy` config.
- [ ] Add `black`/`ruff` and a pre-commit config.

---

## 🤝 Contributing
PRs welcome! Please open an issue first for bigger changes.  
Before pushing, run tests locally:

```bash
pytest -q
```

---

## 📸 Optional: Add a GIF Demo
Record a short terminal session with asciinema or a screen recorder, export a GIF, and drop it under a `docs/` folder. Then embed it here:

```markdown
![demo](docs/demo.gif)
```

---

## 📜 License
MIT © 2025 Emmanuel Akwasi Opoku

---

## 🙌 Credits
Built with **Python**, **Typer**, **Rich**, and **SQLite**.
