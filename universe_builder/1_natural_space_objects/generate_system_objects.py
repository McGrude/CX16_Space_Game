#!/usr/bin/env python3
"""
generate_system_objects.py

Generate natural system objects (planets, moons, asteroids) for each star
in a star catalog CSV produced by the star map generator.

Special handling:
- For SOL (system_id == 0), natural objects are fixed:
    0: Earth (RP)
    1: Luna  (RM, moon of Earth)
    2: Mars  (RP)
    3: Ceres (AS)

Input CSV schema (from star_catalog.csv):
    id, proper, dist_ly, grid_x, grid_y, spect

Output CSV schema (system_objects.csv):
    system_id, object_id, name, class, parent_object_id, is_moon

Object classes:
    RP  = Rocky Planet
    DP  = Desert Planet
    IC  = Ice Planet
    GG  = Gas Giant
    RM  = Rocky Moon
    IM  = Icy Moon
    AS  = Large Asteroid
"""

import argparse
import csv
import random
from typing import List, Dict, Optional

# -------------------------------
# Configurable distributions
# -------------------------------

# Number of natural objects per system (including moons)
OBJECT_COUNT_DISTRIBUTION = [
    (0, 0.10),
    (1, 0.25),
    (2, 0.30),
    (3, 0.20),
    (4, 0.10),
    (5, 0.05),
]

# Planet type distribution (primary objects)
PLANET_TYPE_DISTRIBUTION = [
    ("RP", 0.60),  # Rocky Planet
    ("DP", 0.15),  # Desert Planet
    ("IC", 0.15),  # Ice Planet
    ("GG", 0.10),  # Gas Giant
]

# Chance to include a Large Asteroid if system has >= 2 primary planets
ASTEROID_PROB_IF_2PLUS_PLANETS = 0.20

# Moon counts per planet type (max values)
MAX_MOONS_PER_CLASS = {
    "RP": 1,
    "DP": 1,
    "IC": 1,
    "GG": 3,
}

# Moon type probabilities
MOON_TYPE_DISTRIBUTION_ROCKY_PARENT = [
    ("RM", 0.70),
    ("IM", 0.30),
]

MOON_TYPE_DISTRIBUTION_GAS_PARENT = [
    ("RM", 0.50),
    ("IM", 0.50),
]

MAX_OBJECTS_PER_SYSTEM_DEFAULT = 5


# -------------------------------
# Utility functions
# -------------------------------

def choose_weighted(rng: random.Random, choices: List[tuple]):
    """
    choices: list of (value, weight)
    Returns one value according to normalized weights.
    """
    total = sum(w for _, w in choices)
    r = rng.random() * total
    acc = 0.0
    for value, weight in choices:
        acc += weight
        if r <= acc:
            return value
    # Fallback to last
    return choices[-1][0]


def int_to_roman(n: int) -> str:
    """
    Convert integer to Roman numeral (1..3999).
    We only need small values here.
    """
    vals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I"),
    ]
    result = []
    for val, sym in vals:
        while n >= val:
            n -= val
            result.append(sym)
    return "".join(result)


def generate_planet_type(rng: random.Random) -> str:
    return choose_weighted(rng, PLANET_TYPE_DISTRIBUTION)


def generate_moon_type(rng: random.Random, parent_class: str) -> str:
    if parent_class == "GG":
        return choose_weighted(rng, MOON_TYPE_DISTRIBUTION_GAS_PARENT)
    else:
        return choose_weighted(rng, MOON_TYPE_DISTRIBUTION_ROCKY_PARENT)


# -------------------------------
# Core generation logic
# -------------------------------

def generate_objects_for_system(
    system_id: int,
    system_name: str,
    rng: random.Random,
    max_objects_per_system: int,
) -> List[Dict]:
    """
    Generate natural objects for a single system.

    For SOL (system_id == 0), returns:
        0: Earth  (RP)
        1: Luna   (RM, moon of Earth)
        2: Mars   (RP)
        3: Ceres  (AS)

    For all other systems, generates up to max_objects_per_system objects.

    Returns list of dicts:
        {
            "system_id": int,
            "object_id": int,         # 0..N-1 within system
            "name": str,
            "class": str,             # RP, DP, IC, GG, RM, IM, AS
            "parent_object_id": Optional[int],
            "is_moon": int            # 0 or 1
        }
    """

    # ---- Special case: Sol / home system ----
    if system_id == 0:
        # We ignore object_budget and distributions here.
        # Civilization-era code can later rename or mark these as inhabited.
        return [
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
                "parent_object_id": 0,  # moon of Earth
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

    # ---- Normal systems below ----

    objects: List[Dict] = []

    # 1) Decide total object budget for this system
    object_budget = choose_weighted(rng, OBJECT_COUNT_DISTRIBUTION)

    if object_budget == 0 or max_objects_per_system == 0:
        return []

    object_budget = min(object_budget, max_objects_per_system)

    # 2) Generate primary planets first
    primary_planets_indices: List[int] = []

    # Strategy: generate at least 1 primary if budget > 0.
    primary_target = object_budget

    for _ in range(primary_target):
        planet_class = generate_planet_type(rng)
        obj = {
            "system_id": system_id,
            "object_id": len(objects),
            "name": "",  # to be set later
            "class": planet_class,
            "parent_object_id": None,
            "is_moon": 0,
        }
        objects.append(obj)
        primary_planets_indices.append(obj["object_id"])

    # 3) Possibly convert one slot into an asteroid if >= 2 planets
    if len(primary_planets_indices) >= 2:
        if rng.random() < ASTEROID_PROB_IF_2PLUS_PLANETS:
            # Replace a random planet with an asteroid
            idx_to_replace = rng.choice(primary_planets_indices)
            objects[idx_to_replace]["class"] = "AS"
            # Remove it from primary planets list
            primary_planets_indices = [
                idx for idx in primary_planets_indices if idx != idx_to_replace
            ]

    # 4) Add moons, respecting total object budget
    while len(objects) < object_budget:
        if not primary_planets_indices:
            break  # nothing to orbit

        parent_idx = rng.choice(primary_planets_indices)
        parent = objects[parent_idx]
        parent_class = parent["class"]

        if parent_class not in MAX_MOONS_PER_CLASS:
            # e.g. AS asteroid, skip / try another / maybe exit
            viable_parents = [
                idx for idx in primary_planets_indices
                if objects[idx]["class"] in MAX_MOONS_PER_CLASS
            ]
            if not viable_parents:
                break
            parent_idx = rng.choice(viable_parents)
            parent = objects[parent_idx]
            parent_class = parent["class"]

        # Count existing moons of this parent
        current_moons = sum(
            1 for o in objects
            if o["parent_object_id"] == parent_idx and o["is_moon"] == 1
        )
        max_moons = MAX_MOONS_PER_CLASS.get(parent_class, 0)

        if current_moons >= max_moons or max_moons == 0:
            viable_parents = [
                idx for idx in primary_planets_indices
                if objects[idx]["class"] in MAX_MOONS_PER_CLASS and
                sum(1 for o in objects
                    if o["parent_object_id"] == idx and o["is_moon"] == 1)
                < MAX_MOONS_PER_CLASS[objects[idx]["class"]]
            ]
            if not viable_parents:
                break
            parent_idx = rng.choice(viable_parents)
            parent = objects[parent_idx]
            parent_class = parent["class"]
            current_moons = sum(
                1 for o in objects
                if o["parent_object_id"] == parent_idx and o["is_moon"] == 1
            )
            max_moons = MAX_MOONS_PER_CLASS.get(parent_class, 0)
            if current_moons >= max_moons or max_moons == 0:
                break  # still no room

        # Random chance to actually add a moon
        if parent_class == "GG":
            add_moon_chance = 0.7  # giants often have moons
        else:
            add_moon_chance = 0.4  # others less likely

        if rng.random() > add_moon_chance:
            break

        moon_class = generate_moon_type(rng, parent_class)
        moon_obj = {
            "system_id": system_id,
            "object_id": len(objects),
            "name": "",  # to be assigned later
            "class": moon_class,
            "parent_object_id": parent_idx,
            "is_moon": 1,
        }
        objects.append(moon_obj)

        if len(objects) >= object_budget:
            break

    # 5) Assign names based on system_name and local ordering
    # Primary objects: Name + Roman numeral
    # Moons: Primary name + lowercase letter suffix
    # Asteroids: Name + " Asteroid"

    primary_indices_ordered = [
        i for i, o in enumerate(objects) if o["parent_object_id"] is None
    ]
    primary_indices_ordered.sort()

    planet_counter = 0
    primary_name_map: Dict[int, str] = {}

    for idx in primary_indices_ordered:
        obj = objects[idx]
        if obj["class"] == "AS":
            obj_name = f"{system_name} Asteroid"
        else:
            planet_counter += 1
            rn = int_to_roman(planet_counter)
            obj_name = f"{system_name} {rn}"

        obj["name"] = obj_name
        primary_name_map[idx] = obj_name

    moon_counters_per_parent: Dict[int, int] = {}

    for obj in objects:
        if obj["is_moon"] != 1:
            continue
        parent_idx = obj["parent_object_id"]
        base = primary_name_map.get(parent_idx, system_name)
        count = moon_counters_per_parent.get(parent_idx, 0) + 1
        moon_counters_per_parent[parent_idx] = count
        suffix = chr(ord('a') + (count - 1))  # a, b, c...
        obj["name"] = f"{base}-{suffix}"

    return objects


# -------------------------------
# Main program
# -------------------------------

def parse_args():
    ap = argparse.ArgumentParser(
        description="Generate natural system objects (planets, moons, asteroids) "
                    "for each star in a star catalog CSV."
    )
    ap.add_argument(
        "--input-stars",
        required=True,
        help="Path to input star CSV (star_catalog.csv from previous step)."
    )
    ap.add_argument(
        "--output-objects",
        default="system_objects.csv",
        help="Path to output system objects CSV (default: system_objects.csv)."
    )
    ap.add_argument(
        "--max-objects-per-system",
        type=int,
        default=MAX_OBJECTS_PER_SYSTEM_DEFAULT,
        help="Maximum total natural objects per system (default: 5)."
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Global seed offset for deterministic generation (default: 0)."
    )
    return ap.parse_args()


def main():
    args = parse_args()

    stars = []
    with open(args.input_stars, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_cols = {"id", "proper"}
        missing = required_cols - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(
                f"Input star CSV is missing required columns: {', '.join(sorted(missing))}"
            )
        for row in reader:
            try:
                sid = int(row["id"])
            except ValueError:
                continue
            proper = row.get("proper", "").strip()
            if not proper:
                proper = f"System-{sid}"
            stars.append({"id": sid, "proper": proper})

    if not stars:
        raise SystemExit("No stars loaded from input CSV.")

    # Sort by system id just to keep order stable and intuitive
    stars.sort(key=lambda s: s["id"])

    all_objects: List[Dict] = []

    for star in stars:
        system_id = star["id"]
        system_name = star["proper"]

        # System-specific RNG: combine global seed with system_id
        rng = random.Random(args.seed ^ (system_id * 0x9E3779B1))

        objects = generate_objects_for_system(
            system_id=system_id,
            system_name=system_name,
            rng=rng,
            max_objects_per_system=args.max_objects_per_system,
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
                    "" if obj["parent_object_id"] is None
                    else obj["parent_object_id"]
                ),
                "is_moon": obj["is_moon"],
            }
            writer.writerow(row)

    print(
        f"Generated {len(all_objects)} natural objects "
        f"across {len(stars)} systems into {args.output_objects}"
    )


if __name__ == "__main__":
    main()
