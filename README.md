# SecTrack (CLI) — SQLite mini vulnerability tracker

SecTrack is a small command-line tool to track **hosts** (assets) and **security findings** in a local **SQLite** database.
It allows adding and searching data from the terminal and exporting a report.

## Purpose
Keep an overview of systems in a lab/network and simple vulnerability notes (severity/status) in a structured way.

## Features
### Implemented (Day 1)
- SQLite database with **2 tables**: `hosts` and `findings`
- Initialize database schema
- Add/list/search **hosts**
- Export **hosts** report to **CSV**

### Planned (Day 2/3)
- Add/list/search **findings**
- Export report to **Excel (.xlsx)**
- Sample database with sample data

## Project structure
