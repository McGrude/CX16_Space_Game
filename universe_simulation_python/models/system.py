
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class InhabitedLocation:
    id: str
    system_id: str
    name: str
    type: str
    population: int
    faction_id: Optional[str]
    industry: str

@dataclass
class ResourceNode:
    id: str
    system_id: str
    name: str
    body_type: str
    richness: str

@dataclass
class StarSystem:
    id: str
    name: str
    real_name: str
    position_3d: Tuple[float, float, float]
    position_2d: Tuple[float, float]
    spectral_class: str
    distance_from_sol_ly: float
    inhabited_locations: List[InhabitedLocation] = field(default_factory=list)
    resource_nodes: List[ResourceNode] = field(default_factory=list)
    controlling_faction: Optional[str] = None
    population: int = 0
