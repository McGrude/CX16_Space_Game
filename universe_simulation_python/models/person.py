
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Person:
    id: str
    name: str
    birth_year: int
    death_year: Optional[int]
    role: str
    faction_id: Optional[str] = None
    corporation_id: Optional[str] = None
    accomplishments: List[str] = field(default_factory=list)
