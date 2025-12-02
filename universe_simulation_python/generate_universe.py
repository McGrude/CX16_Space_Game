
import argparse
import json
import os
from dataclasses import asdict, is_dataclass
from typing import Any

from config import CONFIG
from generators.universe import generate_universe

def to_serializable(obj: Any):
    if is_dataclass(obj):
        return {k: to_serializable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, (list, tuple)):
        return [to_serializable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    return obj

def write_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def write_summary(path: str, universe: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("UNIVERSE CHRONICLE\n")
        f.write("===================\n\n")
        f.write(f"Systems: {len(universe['systems'])}\n")
        f.write(f"Factions: {len(universe['factions'])}\n")
        f.write(f"Corporations: {len(universe['corporations'])}\n")
        f.write(f"Events: {len(universe['events'])}\n")
        f.write(f"People: {len(universe['people'])}\n")

def write_csvs(outdir: str, universe: dict):
    import csv
    os.makedirs(outdir, exist_ok=True)

    # systems.csv
    with open(os.path.join(outdir, "systems.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["system_id", "name", "x", "y", "spectral_class", "population", "faction"])
        for s in universe["systems"]:
            w.writerow([
                s.id,
                s.name,
                s.position_2d[0],
                s.position_2d[1],
                s.spectral_class,
                s.population,
                s.controlling_faction or "",
            ])

    # factions.csv
    with open(os.path.join(outdir, "factions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["faction_id", "name", "government", "archetype", "population", "territory_count"])
        for fac in universe["factions"]:
            w.writerow([fac.id, fac.name, fac.government_type, fac.archetype, fac.population, len(fac.territory_system_ids)])

    # corporations.csv
    with open(os.path.join(outdir, "corporations.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["corp_id", "name", "sector", "hq_system", "primary_commodity", "reach_count"])
        for c in universe["corporations"]:
            w.writerow([c.id, c.name, c.sector, c.headquarters_system_id or "", c.primary_commodity or "", len(c.reach_system_ids)])

    # trade_routes.csv
    with open(os.path.join(outdir, "trade_routes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["route_id", "from_system", "to_system", "commodity", "volume", "status", "risk_level"])
        for r in universe["trade_routes"]:
            w.writerow([r["id"], r["from_system"], r["to_system"], r["commodity"], r["volume"], r["status"], r["risk_level"]])

    # history.csv (very simple)
    with open(os.path.join(outdir, "history.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["event_id", "year", "era", "name", "type", "description"])
        for e in universe["events"]:
            w.writerow([e.id, e.year, e.era_name, e.name, e.event_type, e.description])

def write_star_map(path: str, universe: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    systems = universe["systems"]
    with open(path, "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800">\n')
        f.write('<rect x="0" y="0" width="800" height="800" fill="black" />\n')
        for s in systems:
            x = s.position_2d[0] * 8
            y = s.position_2d[1] * 8
            f.write(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="white" />\n')
        f.write("</svg>\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", type=int, default=None, help="Number of systems (override config range)")
    ap.add_argument("--seed", type=int, default=None, help="Random seed")
    ap.add_argument("--output", type=str, default="output", help="Output directory")
    args = ap.parse_args()

    seed = args.seed if args.seed is not None else CONFIG["seed"]
    universe = generate_universe(seed=seed, systems_override=args.systems)
    serial = {
        "metadata": universe["metadata"],
        "systems": [to_serializable(s) for s in universe["systems"]],
        "factions": [to_serializable(f) for f in universe["factions"]],
        "corporations": [to_serializable(c) for c in universe["corporations"]],
        "events": [to_serializable(e) for e in universe["events"]],
        "people": [to_serializable(p) for p in universe["people"]],
        "trade_routes": universe["trade_routes"],
    }

    outdir = args.output
    write_json(os.path.join(outdir, "universe.json"), serial)
    write_summary(os.path.join(outdir, "summary.txt"), universe)
    write_csvs(os.path.join(outdir, "game_data"), universe)
    write_star_map(os.path.join(outdir, "star_map.svg"), universe)
    print(f"Generated universe with {len(universe['systems'])} systems into '{outdir}'.")

if __name__ == "__main__":
    main()
