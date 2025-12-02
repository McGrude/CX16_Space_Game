
import math
import random
from typing import List, Dict, Tuple

from config import CONFIG
from models.system import StarSystem, InhabitedLocation, ResourceNode
from models.faction import Faction
from models.corporation import Corporation
from models.event import HistoricalEvent
from models.person import Person

SPECTRAL_CLASSES = ["O", "B", "A", "F", "G", "K", "M"]
INDUSTRY_TYPES = [
    "core_world", "industrial_world", "agricultural_world",
    "mining_colony", "tech_hub", "military_base", "trade_station",
    "refinery", "research_station", "frontier_colony", "luxury_resort",
    "corporate_hq", "prison_colony", "freeport", "automated_mining"
]

COMMODITIES = [
    "mining_output", "industrial_goods", "agricultural",
    "high_tech", "luxury", "fuel", "medical", "weapons",
    "drugs", "blacknet"
]

FACTION_ARCHETYPES = [
    ("UTOPIAN DEMOCRACY", "representative_democracy"),
    ("CORPORATE OLIGARCHY", "corporate_council"),
    ("MILITARY HEGEMONY", "stratocracy"),
    ("TECHNOCRATIC COLLECTIVE", "technocracy"),
    ("FRONTIER CONFEDERACY", "confederation"),
    ("DYSTOPIAN AUTOCRACY", "autocracy"),
]

CORP_SECTORS = [
    "starship_manufacturing",
    "weapons_and_defense",
    "mining_and_resources",
    "energy_production",
    "technology_and_computing",
    "biotechnology",
    "luxury_goods",
    "shipping_and_logistics",
    "terraforming_and_construction",
    "banking_and_finance",
]

def _rand_name(prefix: str, idx: int) -> str:
    return f"{prefix}-{idx:03d}"

def generate_star_systems(rng: random.Random, count: int) -> List[StarSystem]:
    systems: List[StarSystem] = []
    angle_step = 2 * math.pi / max(count, 1)
    for i in range(count):
        angle = i * angle_step
        radius = rng.uniform(0.1, CONFIG["max_radius_ly"])
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = rng.uniform(-5.0, 5.0)

        sx = CONFIG["grid_center"][0] + x
        sy = CONFIG["grid_center"][1] + y

        spectral = rng.choice(SPECTRAL_CLASSES)
        distance = math.sqrt(x * x + y * y + z * z)

        sys_id = f"sys_{i+1:03d}"
        name = f"System {i+1:03d}"

        system = StarSystem(
            id=sys_id,
            name=name,
            real_name=name,
            position_3d=(x, y, z),
            position_2d=(sx, sy),
            spectral_class=spectral,
            distance_from_sol_ly=distance,
        )
        systems.append(system)

    # random inhabited locations
    for i, s in enumerate(systems):
        if rng.random() < 0.6:
            num = rng.randint(1, 4)
            for j in range(num):
                loc_id = f"loc_{i+1:03d}_{j+1}"
                ind = rng.choice(INDUSTRY_TYPES)
                pop = int(rng.uniform(5e4, 5e9))
                loc = InhabitedLocation(
                    id=loc_id,
                    system_id=s.id,
                    name=f"{s.name} Habitat {j+1}",
                    type="planet" if j == 0 else "station",
                    population=pop,
                    faction_id=None,
                    industry=ind,
                )
                s.inhabited_locations.append(loc)
                s.population += pop

        # a couple of resource nodes
        rn_count = rng.randint(0, 3)
        for k in range(rn_count):
            rn_id = f"res_{i+1:03d}_{k+1}"
            rn = ResourceNode(
                id=rn_id,
                system_id=s.id,
                name=f"{s.name} Node {k+1}",
                body_type=rng.choice(["asteroid", "ice_moon", "gas_giant"]),
                richness=rng.choice(["poor", "fair", "good", "rich"]),
            )
            s.resource_nodes.append(rn)

    return systems

def generate_factions(rng: random.Random, systems: List[StarSystem]) -> List[Faction]:
    factions: List[Faction] = []
    for idx, (arch, gov) in enumerate(FACTION_ARCHETYPES[:CONFIG["num_factions"]]):
        fac_id = f"fac_{idx+1:03d}"
        fac = Faction(
            id=fac_id,
            name=arch.title(),
            archetype=arch,
            government_type=gov,
        )
        factions.append(fac)

    # assign territory in round robin
    for i, s in enumerate(systems):
        fac = factions[i % len(factions)]
        fac.territory_system_ids.append(s.id)
        s.controlling_faction = fac.id
        fac.population += s.population

    return factions

def generate_corporations(rng: random.Random, systems: List[StarSystem]) -> List[Corporation]:
    corps: List[Corporation] = []
    for i in range(CONFIG["num_corporations"]):
        cid = f"corp_{i+1:03d}"
        sector = CORP_SECTORS[i % len(CORP_SECTORS)]
        hq = rng.choice(systems).id if systems else None
        commodity = rng.choice(COMMODITIES)
        corp = Corporation(
            id=cid,
            name=f"Corp {i+1:02d}",
            sector=sector,
            headquarters_system_id=hq,
            primary_commodity=commodity,
        )
        # reach: random handful of systems
        for s in rng.sample(systems, k=max(1, len(systems)//10)):
            corp.reach_system_ids.append(s.id)
        corps.append(corp)
    return corps

def generate_history(rng: random.Random, factions: List[Faction]) -> List[HistoricalEvent]:
    events: List[HistoricalEvent] = []
    eras = CONFIG_Eras()
    eid = 1
    for era in eras:
        # simple placeholder events
        for fac in factions:
            if rng.random() < 0.5:
                ev = HistoricalEvent(
                    id=f"evt_{eid:03d}",
                    name=f"{era['name']} {fac.name} Event",
                    event_type="political",
                    year=rng.randint(era["start"], era["end"]),
                    era_name=era["name"],
                    factions=[fac.id],
                    description=f"Generated placeholder event for {fac.name} in {era['name']}.",
                )
                events.append(ev)
                eid += 1
    return events

def CONFIG_Eras() -> List[Dict]:
    # mirror eras from CONFIG for convenience
    return [
        {"name": "First Expansion", "start": 2100, "end": 2200},
        {"name": "Colonial Period", "start": 2200, "end": 2300},
        {"name": "Consolidation and Conflict", "start": 2300, "end": 2400},
        {"name": "Modern Era", "start": 2400, "end": 2450},
    ]

def generate_people(rng: random.Random, factions: List[Faction]) -> List[Person]:
    people: List[Person] = []
    pid = 1
    for era in CONFIG_Eras():
        for fac in factions:
            for _ in range(2):  # 2 per faction per era
                name = f"{fac.name.split()[0]} Figure {pid}"
                p = Person(
                    id=f"per_{pid:03d}",
                    name=name,
                    birth_year=rng.randint(era["start"] - 40, era["start"]),
                    death_year=None,
                    role="leader",
                    faction_id=fac.id,
                )
                people.append(p)
                pid += 1
    return people

def generate_trade_routes(systems: List[StarSystem]) -> List[Dict]:
    # simple nearest-neighbour trade network
    routes: List[Dict] = []
    for i, s in enumerate(systems):
        if i == 0:
            continue
        prev = systems[i-1]
        routes.append({
            "id": f"route_{i:03d}",
            "from_system": prev.id,
            "to_system": s.id,
            "commodity": "industrial_goods",
            "volume": 100000,
            "status": "active",
            "risk_level": "medium",
        })
    return routes

def generate_universe(seed: int | None = None, systems_override: int | None = None) -> Dict:
    rng = random.Random(seed)
    num_systems = systems_override or rng.randint(CONFIG["min_systems"], CONFIG["max_systems"])
    systems = generate_star_systems(rng, num_systems)
    factions = generate_factions(rng, systems)
    corporations = generate_corporations(rng, systems)
    events = generate_history(rng, factions)
    people = generate_people(rng, factions)
    trade_routes = generate_trade_routes(systems)

    meta = {
        "seed": seed,
        "version": CONFIG["version"],
        "system_count": len(systems),
    }
    return {
        "metadata": meta,
        "systems": systems,
        "factions": factions,
        "corporations": corporations,
        "events": events,
        "people": people,
        "trade_routes": trade_routes,
    }
