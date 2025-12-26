# SecTrack (CLI) — SQLite mini vulnerability tracker

SecTrack is a simple command-line tool to track hosts and security findings (vulnerabilities) in a small SQLite database.

## Features
- SQLite database with 2 tables: `hosts` and `findings`
- Add/list/search hosts
- Add/list findings (linked to a host)
- Export:
  - Hosts to CSV (`hosts.csv`)
  - Findings to Excel (`findings.xlsx`)
- Settings in a separate file (`settings.ini`) that is NOT committed

## Project structure
- `src/sectrack/` : application package
- `scripts/` : helper scripts (init/seed database)
- `data/sample.db` : sample database with sample data (committed for grading)
- `data/exports/` : exports folder (NOT committed)

## Setup (Use this please!)
```bash 
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
