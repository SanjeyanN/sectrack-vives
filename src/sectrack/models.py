from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Host:
    hostname: str
    ip: Optional[str] = None
    owner: Optional[str] = None
    notes: Optional[str] = None
