
from dataclasses import dataclass, field
from typing import List

@dataclass
class HistoricalEvent:
    id: str
    name: str
    event_type: str
    year: int
    era_name: str
    systems: List[str] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)
    corporations: List[str] = field(default_factory=list)
    description: str = ""
