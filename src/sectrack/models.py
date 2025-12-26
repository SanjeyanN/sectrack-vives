from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Host:
    hostname: str
    ip: Optional[str] = None
    owner: Optional[str] = None
    notes: Optional[str] = None

from datetime import datetime

@dataclass
class Finding:
    host_id: int
    title: str
    severity: str
    status: str = "open"
    created_at: str = datetime.now().strftime("%Y-%m-%d")
