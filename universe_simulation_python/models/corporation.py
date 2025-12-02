
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Corporation:
    id: str
    name: str
    sector: str
    headquarters_system_id: Optional[str]
    primary_commodity: Optional[str]
    reach_system_ids: List[str] = field(default_factory=list)
