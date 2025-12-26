import sys
from pathlib import Path

# project root = 1 map boven scripts/
ROOT = Path(__file__).resolve().parents[1]

# so scripts can import from src/ when run inside Spyder
sys.path.insert(0, str(ROOT / "src"))

from sectrack.config import load_config
from sectrack.db import Database


def main() -> int:
    cfg = load_config(str(ROOT / "settings.ini"))  # <-- FIX: absolute path
    db = Database(cfg.db_path)
    db.init_schema()
    print("OK: schema created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
