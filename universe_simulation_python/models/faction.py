
from dataclasses import dataclass, field
from typing import List

@dataclass
class Faction:
    id: str
    name: str
    archetype: str
    government_type: str
    values: List[str] = field(default_factory=list)
    territory_system_ids: List[str] = field(default_factory=list)
    population: int = 0
