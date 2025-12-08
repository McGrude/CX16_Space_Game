#!/usr/bin/env python3
"""
generate_system_objects.py

Generate natural system objects (planets, moons, asteroids) for each star
in a star catalog CSV produced by the star map generator.

Phase 1 responsibilities:
- Read star_catalog.csv (output of Phase 0).
- For each system, deterministically generate:
  - Primary natural objects (planets + at most one large asteroid).
  - Optional moons for planets.
- Apply deterministic attributes per object:
  - Local 2D coordinates in a 50x50 system map (local_x, local_y).
  - Ore and fuel richness (0–3).
  - Habitability and risk (0–100).
- Special-case Sol (system_id == 0) with a fixed set of objects.

The output is system_objects.csv.

Input CSV schema (from star_catalog.csv):
    id, proper, dist_ly, grid_x, grid_y, spect

Only the following columns are required:
    id, proper, spect
"""

import argparse
import csv
import hashlib
import math
import random
from typing import Dict, List, Optional, Sequence, Tuple


# -------------------------------
# Distributions and constants
# -------------------------------

# Per-system primary object count (planets + at most one asteroid).
# This is the target number of PRIMARY objects; moons are generated on top.
OBJECT_COUNT_DISTRIBUTION: Sequence[Tuple[int, int]] = [
    (0, 10),  # 10%
    (1, 25),  # 25%
    (2, 30),  # 30%
    (3, 20),  # 20%
    (4, 10),  # 10%
    (5, 5),   # 5%
]

# Primary planet type probabilities
PLANET_TYPE_DISTRIBUTION: Sequence[Tuple[str, int]] = [
    ("RP", 60),  # Rocky Planet
    ("DP", 15),  # Desert Planet
    ("IC", 15),  # Ice Planet
    ("GG", 10),  # Gas Giant
]

# Maximum moons per planet class
MAX_MOONS_PER_CLASS: Dict[str, int] = {
    "RP": 1,
    "DP": 1,
    "IC": 1,
    "GG": 3,
}

# Moon type probabilities for rocky parents
MOON_TYPES_ROCKY: Sequence[Tuple[str, int]] = [
    ("RM", 70),  # Rocky Moon
    ("IM", 30),  # Icy Moon
]

# Moon type probabilities for gas giants
MOON_TYPES_GG: Sequence[Tuple[str, int]] = [
    ("RM", 50),
    ("IM", 50),
]

# Spectral-based habitability and risk baselines
HAB_STAR_BASE: Dict[str, int] = {
    "O": 5,
    "B": 5,
    "A": 15,
    "F": 30,
    "G": 50,
    "K": 45,
    "M": 35,
}
RISK_STAR_BASE: Dict[str, int] = {
    "O": 25,
    "B": 25,
    "A": 15,
    "F": 10,
    "G": 0,
    "K": -5,
    "M": -10,
}

HAB_CLASS_MOD: Dict[str, int] = {
    "RP": 30,
    "DP": 10,
    "IC": 0,
    "GG": -25,
    "RM": 20,
    "IM": 0,
    "AS": -10,
}
RISK_CLASS_BASE: Dict[str, int] = {
    "RP": 40,
    "DP": 60,
    "IC": 50,
    "GG": 80,
    "RM": 45,
    "IM": 55,
    "AS": 65,
}

# Local system map constants
LOCAL_MAP_SIZE = 50
LOCAL_CENTER_X = LOCAL_MAP_SIZE // 2
LOCAL_CENTER_Y = LOCAL_MAP_SIZE // 2
LOCAL_ORBIT_RADII = [5, 8, 11, 14, 17, 20]


# -------------------------------
# Helper functions
# -------------------------------

def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def choose_weighted(rng: random.Random, table: Sequence[Tuple[int, int]]) -> int:
    """Choose a value from (value, weight) pairs using rng."""
    total = sum(weight for _, weight in table)
    r = rng.uniform(0, total)
    acc = 0.0
    for val, weight in table:
        acc += weight
        if r <= acc:
            return val
    # Fallback (should not happen due to floating point):
    return table[-1][0]


def generate_planet_type(rng: random.Random) -> str:
    """Weighted choice of primary planet class."""
    total = sum(w for _, w in PLANET_TYPE_DISTRIBUTION)
    r = rng.uniform(0, total)
    acc = 0.0
    for cls, w in PLANET_TYPE_DISTRIBUTION:
        acc += w
        if r <= acc:
            return cls
    return PLANET_TYPE_DISTRIBUTION[-1][0]


def choose_num_moons(rng: random.Random, parent_class: str) -> int:
    """Choose how many moons a planet gets, respecting its maximum."""
    max_m = MAX_MOONS_PER_CLASS.get(parent_class, 0)
    if max_m == 0:
        return 0

    if parent_class == "GG":
        # Gas giant: 0–3 with a bias toward 1–2
        choices = [(0, 20), (1, 40), (2, 30), (3, 10)]
    else:
        # Rocky/desert/ice planets: 0 or 1
        choices = [(0, 50), (1, 50)]

    # Filter choices to respect max_m
    filtered = [(val, w) for val, w in choices if val <= max_m]
    total = sum(w for _, w in filtered)
    r = rng.uniform(0, total)
    acc = 0.0
    for val, w in filtered:
        acc += w
        if r <= acc:
            return val
    return filtered[-1][0]


def choose_moon_class(rng: random.Random, parent_class: str) -> str:
    """Choose moon class based on parent planet type."""
    if parent_class == "GG":
        table = MOON_TYPES_GG
    else:
        table = MOON_TYPES_ROCKY

    total = sum(w for _, w in table)
    r = rng.uniform(0, total)
    acc = 0.0
    for cls, w in table:
        acc += w
        if r <= acc:
            return cls
    return table[-1][0]


def parse_spectral_letter(spect: str) -> str:
    """Extract the first alphabetic spectral type letter (O, B, A, F, G, K, M)."""
    for ch in spect.upper():
        if ch.isalpha():
            return ch
    return "?"


def compute_attributes(
    system_id: int,
    object_id: int,
    obj_class: str,
    spect: str,
) -> Tuple[int, int, int, int]:
    """
    Compute (habitability, risk, ore_richness, fuel_richness) for a single object.

    - habitability: 0–100, higher is better for human life.
    - risk: 0–100, higher is more dangerous.
    - ore_richness: 0–3.
    - fuel_richness: 0–3.
    """
    # Stable 32-bit hash derived from system_id, object_id, class
    key = f"{system_id}:{object_id}:{obj_class}".encode("utf-8")
    h_bytes = hashlib.sha256(key).digest()
    h32 = int.from_bytes(h_bytes[:4], "big")

    spect_letter = parse_spectral_letter(spect)
    hab_star = HAB_STAR_BASE.get(spect_letter, 30)
    risk_star = RISK_STAR_BASE.get(spect_letter, 0)

    hab_class = HAB_CLASS_MOD.get(obj_class, 0)
    risk_class = RISK_CLASS_BASE.get(obj_class, 50)

    # Habitability with small deterministic jitter
    hab_raw = hab_star + hab_class
    delta_h = (h32 & 0x0F) - 8  # -8..+7
    habitability = clamp(hab_raw + delta_h, 0, 100)

    # Risk with small deterministic jitter
    risk_raw = risk_class + risk_star
    delta_r = ((h32 >> 4) & 0x0F) - 8
    risk = clamp(risk_raw + delta_r, 0, 100)

    # Ore and fuel richness from separate bits
    ore_byte = (h32 >> 8) & 0xFF
    fuel_byte = (h32 >> 16) & 0xFF

    # Ore richness by class
    if obj_class in ("RP", "DP", "RM", "AS"):
        if ore_byte < 25:
            ore = 0
        elif ore_byte < 100:
            ore = 1
        elif ore_byte < 200:
            ore = 2
        else:
            ore = 3
    elif obj_class in ("IC", "IM"):
        if ore_byte < 80:
            ore = 0
        elif ore_byte < 180:
            ore = 1
        elif ore_byte < 230:
            ore = 2
        else:
            ore = 3
    else:
        # Gas giants and unknowns: no meaningful ore
        ore = 0

    # Fuel richness
    if obj_class == "GG":
        # Gas giants are prime fuel sources
        fuel = 2 if fuel_byte < 128 else 3
    else:
        if fuel_byte < 40:
            fuel = 0
        elif fuel_byte < 160:
            fuel = 1
        elif fuel_byte < 230:
            fuel = 2
        else:
            fuel = 3

    return habitability, risk, ore, fuel


def assign_names_for_system(
    system_name: str,
    objects: List[Dict],
    primary_indices: List[int],
) -> None:
    """Assign names to primary objects and moons for a system (non-Sol)."""
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    primary_name_map: Dict[int, str] = {}

    # Primary objects first
    for idx, primary_idx in enumerate(primary_indices):
        obj = objects[primary_idx]
        if obj["class"] == "AS":
            obj_name = f"{system_name} Asteroid"
        else:
            rn = roman[idx] if idx < len(roman) else f"{idx+1}"
            obj_name = f"{system_name} {rn}"
        obj["name"] = obj_name
        primary_name_map[primary_idx] = obj_name

    # Moons
    moon_counters_per_parent: Dict[int, int] = {}
    for obj in objects:
        if obj["is_moon"] != 1:
            continue
        parent_idx = obj["parent_object_id"]
        base = primary_name_map.get(parent_idx, system_name)
        count = moon_counters_per_parent.get(parent_idx, 0) + 1
        moon_counters_per_parent[parent_idx] = count
        suffix = chr(ord("a") + (count - 1))  # a, b, c, ...
        obj["name"] = f"{base}-{suffix}"


def assign_local_coordinates(
    system_id: int,
    objects: List[Dict],
) -> None:
    """Assign local_x/local_y for each object in a 50x50 system map."""
    # First, assign coordinates for primaries on concentric orbits
    primary_indices = [i for i, o in enumerate(objects) if o["is_moon"] == 0]

    for orbit_idx, obj_idx in enumerate(primary_indices):
        radius = LOCAL_ORBIT_RADII[min(orbit_idx, len(LOCAL_ORBIT_RADII) - 1)]
        key = f"orbit:{system_id}:{obj_idx}".encode("utf-8")
        h_bytes = hashlib.sha256(key).digest()
        h32 = int.from_bytes(h_bytes[:4], "big")

        angle = 2.0 * math.pi * (h32 / (2**32))
        x_f = LOCAL_CENTER_X + radius * math.cos(angle)
        y_f = LOCAL_CENTER_Y + radius * math.sin(angle)

        x = clamp(int(round(x_f)), 0, LOCAL_MAP_SIZE - 1)
        y = clamp(int(round(y_f)), 0, LOCAL_MAP_SIZE - 1)
        objects[obj_idx]["local_x"] = x
        objects[obj_idx]["local_y"] = y

    # Then, assign coordinates for moons clustered near parents
    for obj in objects:
        if obj["is_moon"] != 1:
            continue
        parent_idx = obj["parent_object_id"]
        parent = objects[parent_idx]
        px = parent.get("local_x", LOCAL_CENTER_X)
        py = parent.get("local_y", LOCAL_CENTER_Y)

        key = f"moonpos:{system_id}:{obj['object_id']}".encode("utf-8")
        h_bytes = hashlib.sha256(key).digest()
        h16 = int.from_bytes(h_bytes[:2], "big")

        dx = (h16 & 0x03) - 1        # -1..2
        dy = ((h16 >> 2) & 0x03) - 1 # -1..2

        x = clamp(px + dx, 0, LOCAL_MAP_SIZE - 1)
        y = clamp(py + dy, 0, LOCAL_MAP_SIZE - 1)
        obj["local_x"] = x
        obj["local_y"] = y


# -------------------------------
# Core generation logic
# -------------------------------

def generate_objects_for_system(
    system_id: int,
    system_name: str,
    spect: str,
    global_seed: int,
    max_primaries: int,
) -> List[Dict]:
    """
    Generate natural objects for a single system.

    For SOL (system_id == 0), returns fixed objects:
        0: Earth  (RP)
        1: Luna   (RM, moon of Earth)
        2: Mars   (RP)
        3: Ceres  (AS)

    For all other systems, generates up to max_primaries primary objects
    (planets and at most one large asteroid), plus possible moons.
    """
    # ---- Special case: Sol / home system ----
    if system_id == 0:
        objects: List[Dict] = [
            {
                "system_id": 0,
                "object_id": 0,
                "name": "Earth",
                "class": "RP",
                "parent_object_id": None,
                "is_moon": 0,
            },
            {
                "system_id": 0,
                "object_id": 1,
                "name": "Luna",
                "class": "RM",
                "parent_object_id": 0,
                "is_moon": 1,
            },
            {
                "system_id": 0,
                "object_id": 2,
                "name": "Mars",
                "class": "RP",
                "parent_object_id": None,
                "is_moon": 0,
            },
            {
                "system_id": 0,
                "object_id": 3,
                "name": "Ceres",
                "class": "AS",
                "parent_object_id": None,
                "is_moon": 0,
            },
        ]

        # Decorate with attributes and local coordinates
        for obj in objects:
            habitability, risk, ore, fuel = compute_attributes(
                system_id=obj["system_id"],
                object_id=obj["object_id"],
                obj_class=obj["class"],
                spect=spect,
            )
            obj["habitability"] = habitability
            obj["risk"] = risk
            obj["ore_richness"] = ore
            obj["fuel_richness"] = fuel

        assign_local_coordinates(system_id, objects)
        return objects

    # ---- Normal systems below ----

    rng_seed = global_seed ^ (system_id * 0x9E3779B1)
    rng = random.Random(rng_seed)

    objects: List[Dict] = []

    # 1) Decide number of primary objects for this system
    primary_budget = choose_weighted(rng, OBJECT_COUNT_DISTRIBUTION)
    if primary_budget <= 0 or max_primaries <= 0:
        return []
    primary_budget = min(primary_budget, max_primaries)

    # 2) Generate primary planets first
    primary_indices: List[int] = []
    for _ in range(primary_budget):
        planet_class = generate_planet_type(rng)
        obj = {
            "system_id": system_id,
            "object_id": len(objects),
            "name": "",  # to be assigned later
            "class": planet_class,
            "parent_object_id": None,
            "is_moon": 0,
        }
        objects.append(obj)
        primary_indices.append(obj["object_id"])

    # 3) Optionally replace one primary with a large asteroid (AS)
    if len(primary_indices) >= 2:
        if rng.random() < 0.20:  # 20% chance
            idx = rng.choice(primary_indices)
            objects[idx]["class"] = "AS"

    # 4) Generate moons for eligible primaries
    for parent_idx in primary_indices:
        parent = objects[parent_idx]
        parent_class = parent["class"]
        if parent_class not in MAX_MOONS_PER_CLASS:
            continue

        num_moons = choose_num_moons(rng, parent_class)
        for _ in range(num_moons):
            moon_class = choose_moon_class(rng, parent_class)
            moon_obj = {
                "system_id": system_id,
                "object_id": len(objects),
                "name": "",  # assigned later
                "class": moon_class,
                "parent_object_id": parent_idx,
                "is_moon": 1,
            }
            objects.append(moon_obj)

    # 5) Assign names (non-Sol systems)
    assign_names_for_system(system_name, objects, primary_indices)

    # 6) Compute attributes (habitability, risk, ore, fuel)
    for obj in objects:
        habitability, risk, ore, fuel = compute_attributes(
            system_id=obj["system_id"],
            object_id=obj["object_id"],
            obj_class=obj["class"],
            spect=spect,
        )
        obj["habitability"] = habitability
        obj["risk"] = risk
        obj["ore_richness"] = ore
        obj["fuel_richness"] = fuel

    # 7) Assign local map coordinates
    assign_local_coordinates(system_id, objects)

    return objects


# -------------------------------
# CLI and main program
# -------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Generate natural system objects (planets, moons, asteroids) "
            "for each star in a star catalog CSV."
        )
    )
    ap.add_argument(
        "--input-stars",
        required=True,
        help="Path to input star CSV (star_catalog.csv from Phase 0).",
    )
    ap.add_argument(
        "--output-objects",
        default="system_objects.csv",
        help="Path to output system objects CSV (default: system_objects.csv).",
    )
    ap.add_argument(
        "--max-objects-per-system",
        type=int,
        default=5,
        help=(
            "Maximum number of PRIMARY objects per system "
            "(planets + large asteroid). Moons are generated on top "
            "(default: 5)."
        ),
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Global seed offset for deterministic generation (default: 0).",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    # Load stars
    stars: List[Dict] = []
    with open(args.input_stars, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_cols = {"id", "proper", "spect"}
        if reader.fieldnames is None:
            raise SystemExit("Input star CSV has no header row.")
        missing = required_cols - set(reader.fieldnames)
        if missing:
            raise SystemExit(
                f"Input star CSV missing required columns: {', '.join(sorted(missing))}"
            )

        for row in reader:
            try:
                system_id = int(row["id"])
            except (ValueError, TypeError):
                continue
            name = (row.get("proper") or "").strip()
            if not name:
                name = f"System {system_id}"
            spect = (row.get("spect") or "").strip()
            stars.append(
                {
                    "id": system_id,
                    "proper": name,
                    "spect": spect,
                }
            )

    # Generate objects for all systems
    all_objects: List[Dict] = []
    for star in stars:
        system_id = star["id"]
        name = star["proper"]
        spect = star["spect"]
        objects = generate_objects_for_system(
            system_id=system_id,
            system_name=name,
            spect=spect,
            global_seed=args.seed,
            max_primaries=args.max_objects_per_system,
        )
        all_objects.extend(objects)

    # Write output CSV
    fieldnames = [
        "system_id",
        "object_id",
        "name",
        "class",
        "parent_object_id",
        "is_moon",
        "local_x",
        "local_y",
        "ore_richness",
        "fuel_richness",
        "habitability",
        "risk",
    ]

    with open(args.output_objects, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for obj in all_objects:
            row = {
                "system_id": obj["system_id"],
                "object_id": obj["object_id"],
                "name": obj["name"],
                "class": obj["class"],
                "parent_object_id": (
                    "" if obj.get("parent_object_id") is None
                    else obj["parent_object_id"]
                ),
                "is_moon": obj["is_moon"],
                "local_x": obj.get("local_x", ""),
                "local_y": obj.get("local_y", ""),
                "ore_richness": obj.get("ore_richness", 0),
                "fuel_richness": obj.get("fuel_richness", 0),
                "habitability": obj.get("habitability", 0),
                "risk": obj.get("risk", 0),
            }
            writer.writerow(row)

    print(
        f"Generated {len(all_objects)} natural objects "
        f"across {len(stars)} systems into {args.output_objects}"
    )


if __name__ == "__main__":
    main()
