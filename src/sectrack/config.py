from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    db_path: Path
    export_dir: Path


def load_config(settings_path: str = "settings.ini") -> AppConfig:
    p = Path(settings_path)
    if not p.exists():
        raise FileNotFoundError(
            f"Missing {settings_path}. Create it from settings_example.ini (do NOT commit it)."
        )

    parser = configparser.ConfigParser()
    parser.read(p, encoding="utf-8")

    if "app" not in parser:
        raise ValueError("Invalid settings.ini: missing [app] section")

    db_path = Path(parser["app"].get("db_path", "data/sample.db"))
    export_dir = Path(parser["app"].get("export_dir", "data/exports"))
    return AppConfig(db_path=db_path, export_dir=export_dir)
