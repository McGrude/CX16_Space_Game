#!/usr/bin/env python3
"""
Build a local star database for the game from a HYG-style star catalog.

Behavior:

- Load a HYG CSV (e.g. HYG 4.x).
- Filter stars within a given radius (in LIGHT-YEARS) from Sol.
- Convert parsecs → light-years (1 pc ≈ 3.26156 ly).
- Project (x_ly, y_ly) into a 2D 100×100 grid:
    - grid_x = round(50 + x_ly / scale)
    - grid_y = round(50 + y_ly / scale)
  where `scale` = light-years per grid cell.

- Stars whose projected grid_x/grid_y are outside [0, 99] are PRUNED.
- If more than one star lands in the same grid cell:
    - If Sol is in that cell, keep Sol and prune the rest.
    - Otherwise:
        1) Prefer stars with a non-empty proper name (from catalog).
        2) Among that subset, keep the "largest" star (see below).
        3) If none are named, pick the "largest" among all.

  "Largest" is determined by:
    1. lum (luminosity) if present (higher is brighter),
    2. else mag (apparent magnitude; lower is brighter),
    3. else fallback to distance.

- ASCII map rules:
    - Start as '.' everywhere.
    - 'X' = Sol
    - '*' = other stars (one per cell by construction)
    - After placing stars, any cell that is still '.' and whose center
      lies beyond the configured radius (in ly) becomes a space ' '.

CSV OUTPUT (for game use):

- Sorted by dist_ly ascending (Sol first).
- Columns:
    id, proper, dist_ly, grid_x, grid_y, spect
- `id` is a monotonic integer starting at 0 for Sol.
- `proper` is either:
    - the catalog's real proper name, if present, OR
    - a synthetic sector/cluster style name generated deterministically
      from the original catalog id (or HIP / coords if no id).
"""

import argparse
import csv
import math
import sys
import random
import hashlib
from typing import List, Dict, Any, Optional, Tuple

PC_TO_LY = 3.26156


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build star database and ASCII map from a HYG star catalog."
    )
    parser.add_argument(
        "--input-csv",
        required=True,
        help="Path to local HYG CSV file (e.g. HYG 4.x download).",
    )
    parser.add_argument(
        "--radius-ly",
        type=float,
        default=50.0,
        help="Maximum distance from Sol in light-years (default: 50).",
    )
    parser.add_argument(
        "--max-stars",
        type=int,
        default=150,
        help="Maximum number of stars to keep BEFORE projection (nearest first).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help=(
            "Light-years per grid cell (default: 1.0). "
            "Example: 0.5 = 0.5 ly per cell; 0.25 = 0.25 ly per cell."
        ),
    )
    parser.add_argument(
        "--csv-out",
        default=None,
        help="Path to output CSV file (default: stdout if not set).",
    )
    parser.add_argument(
        "--map-out",
        default="star_map.txt",
        help="Path to ASCII map output file (default: star_map.txt).",
    )
    return parser.parse_args()


def load_hyg_csv(path: str) -> List[Dict[str, Any]]:
    """Load stars from a HYG-style CSV file into a list of dicts."""
    stars: List[Dict[str, Any]] = []

    try:
        f = open(path, newline="", encoding="utf-8")
    except OSError as e:
        print(f"ERROR: Failed to open input CSV '{path}': {e}", file=sys.stderr)
        sys.exit(1)

    with f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Distance in parsecs (column name varies by version)
                dist_pc_str = row.get("dist") or row.get("Distance") or row.get("dist_pc")
                if not dist_pc_str:
                    # Fallback: derive distance from x,y,z if present
                    x_pc_str = row.get("x") or row.get("X")
                    y_pc_str = row.get("y") or row.get("Y")
                    z_pc_str = row.get("z") or row.get("Z")
                    if not (x_pc_str and y_pc_str and z_pc_str):
                        continue
                    x_pc = float(x_pc_str)
                    y_pc = float(y_pc_str)
                    z_pc = float(z_pc_str)
                    dist_pc = math.sqrt(x_pc * x_pc + y_pc * y_pc + z_pc * z_pc)
                else:
                    dist_pc = float(dist_pc_str)

                dist_ly = dist_pc * PC_TO_LY

                # Coordinates in parsecs (if available)
                x_pc_str = row.get("x") or row.get("X")
                y_pc_str = row.get("y") or row.get("Y")
                z_pc_str = row.get("z") or row.get("Z")

                if x_pc_str and y_pc_str and z_pc_str:
                    x_pc = float(x_pc_str)
                    y_pc = float(y_pc_str)
                    z_pc = float(z_pc_str)
                else:
                    # If coordinates missing, put star on x-axis at its distance.
                    x_pc, y_pc, z_pc = dist_pc, 0.0, 0.0

                x_ly = x_pc * PC_TO_LY
                y_ly = y_pc * PC_TO_LY
                z_ly = z_pc * PC_TO_LY

                # Optional luminosity and absolute magnitude if present
                lum_str = row.get("lum") or row.get("Lum")
                absmag_str = row.get("absmag") or row.get("AbsMag")

                stars.append(
                    {
                        "id": row.get("id") or row.get("ID") or "",
                        "hip": row.get("hip") or row.get("HIP") or "",
                        "proper": (
                            row.get("proper")
                            or row.get("ProperName")
                            or row.get("name")
                            or ""
                        ),
                        "ra": row.get("ra") or row.get("RA") or "",
                        "dec": row.get("dec") or row.get("Dec") or "",
                        "dist_pc": dist_pc,
                        "dist_ly": dist_ly,
                        "x_ly": x_ly,
                        "y_ly": y_ly,
                        "z_ly": z_ly,
                        "spect": row.get("spect") or row.get("SpectralType") or "",
                        "mag": row.get("mag") or row.get("Mag") or "",
                        "lum": lum_str or "",
                        "absmag": absmag_str or "",
                    }
                )
            except ValueError:
                # Bad numeric data; skip this row
                continue

    if not stars:
        print(
            f"ERROR: Loaded 0 stars from '{path}'. "
            "Check that it is a valid HYG CSV file.",
            file=sys.stderr,
        )
    return stars


def select_stars_within_radius(
    stars: List[Dict[str, Any]], radius_ly: float, max_stars: int
) -> List[Dict[str, Any]]:
    """Filter stars within radius (LY) and limit count, always keeping the nearest (Sol)."""
    within = [s for s in stars if s["dist_ly"] <= radius_ly]

    if not within:
        return []

    # Sort by distance (nearest first)
    within.sort(key=lambda s: s["dist_ly"])

    if max_stars is not None and len(within) > max_stars:
        sol = within[0]
        others = within[1:max_stars]
        result = [sol] + others
    else:
        result = within

    # Tag the nearest as Sol explicitly
    result[0]["is_sol"] = True
    return result


def _size_metric(star: Dict[str, Any]) -> Tuple[int, float, float]:
    """
    Compute a tuple used to select the "largest" star in a cell.

    Priority:
      1) Has valid lum → use that (higher is better)
      2) Else has valid mag → use -mag (smaller mag = brighter)
      3) Else → fall back to inverse distance as a weak tie-breaker.

    Returns:
      (has_lum_flag, metric1, metric2)

    Comparison is lexicographic; higher tuple is considered "larger".
    """
    has_lum = 0
    metric1 = -1e9
    metric2 = -1e9

    # Try luminosity
    lum_str = star.get("lum", "")
    if lum_str:
        try:
            lum_val = float(lum_str)
            has_lum = 1
            metric1 = lum_val
            metric2 = 0.0
            return (has_lum, metric1, metric2)
        except ValueError:
            pass

    # Try magnitude
    mag_str = star.get("mag", "")
    if mag_str:
        try:
            mag_val = float(mag_str)
            has_lum = 0
            metric1 = -mag_val  # lower mag = brighter
            metric2 = 0.0
            return (has_lum, metric1, metric2)
        except ValueError:
            pass

    # Fallback: inverse distance (closer "wins" as tie-break)
    dist_ly = float(star.get("dist_ly", 1e9))
    has_lum = 0
    metric1 = 0.0
    metric2 = -dist_ly
    return (has_lum, metric1, metric2)


def project_to_grid(
    stars: List[Dict[str, Any]], scale: float
) -> List[Dict[str, Any]]:
    """
    Map x_ly, y_ly → 100x100 grid centered on Sol at (50, 50).

    scale = light-years per grid cell.

    Stars whose projected position falls outside [0, 99] in either axis
    are PRUNED.

    If multiple stars land in the same (grid_x, grid_y):
      - If one of them is Sol, keep Sol and drop the rest.
      - Else:
          1) Prefer stars with a non-empty proper name (from catalog).
          2) Among those, keep the "largest" by _size_metric().
          3) If none are named, keep the "largest" among all.
    """
    cell_map: Dict[Tuple[int, int], List[Dict[str, Any]]] = {}
    off_map_count = 0

    for s in stars:
        x_ly = s["x_ly"]
        y_ly = s["y_ly"]

        gx = int(round(50.0 + (x_ly / scale)))
        gy = int(round(50.0 + (y_ly / scale)))

        if gx < 0 or gx > 99 or gy < 0 or gy > 99:
            off_map_count += 1
            continue

        s["grid_x"] = gx
        s["grid_y"] = gy

        key = (gx, gy)
        cell_map.setdefault(key, []).append(s)

    if off_map_count:
        print(
            f"Pruned {off_map_count} stars that projected outside the 100x100 grid.",
            file=sys.stderr,
        )

    survivors: List[Dict[str, Any]] = []
    pruned_collisions = 0

    for (gx, gy), cell_stars in cell_map.items():
        if not cell_stars:
            continue

        # If Sol is in this cell, it wins automatically
        sol_in_cell = [s for s in cell_stars if s.get("is_sol")]
        if sol_in_cell:
            chosen = sol_in_cell[0]
        else:
            # Prefer stars with catalog proper names (not synthetic)
            named = [s for s in cell_stars if (s.get("proper") or "").strip() != ""]
            if named:
                chosen = max(named, key=_size_metric)
            else:
                chosen = max(cell_stars, key=_size_metric)

        survivors.append(chosen)
        pruned_here = len(cell_stars) - 1
        pruned_collisions += max(0, pruned_here)

    if pruned_collisions:
        print(
            f"Pruned {pruned_collisions} stars due to grid cell collisions "
            f"(one star per cell retained, preferring catalog-named stars).",
            file=sys.stderr,
        )

    return survivors


# ---------- Synthetic naming helpers ----------

_SECTOR_PREFIXES = [
    "Helion",
    "Koros",
    "Velarn",
    "Nadir",
    "Procyon",
    "Altaris",
    "Veyra",
    "Talios",
    "Meridian",
    "Triarch",
    "Nomad",
    "Aurigon",
    "Serpentis",
    "Draxis",
    "Cygnera",
    "Luyten",
    "Epsara",
    "Tauven",
    "Sigmar",
    "Zethys",
    "Khoras",
    "Frontier",
    "Pioneer",
    "Arcturon",
    "Vegaine",
]

_SECTOR_TYPES = [
    "Sector",
    "Cluster",
    "Reach",
    "Arc",
    "Belt",
    "Verge",
    "Expanse",
]


def _seed_from_star(star: Dict[str, Any]) -> int:
    """
    Build a deterministic RNG seed from:
      - original catalog id, if present
      - else HIP number
      - else hashed coordinates.
    """
    base = (
        (star.get("id") or "").strip()
        or (star.get("hip") or "").strip()
        or f"{star.get('x_ly', 0.0):.5f},{star.get('y_ly', 0.0):.5f},{star.get('z_ly', 0.0):.5f}"
    )

    # If base is purely numeric, use it directly (clamped to 32-bit).
    if base.isdigit():
        return int(base) & 0x7FFFFFFF

    # Otherwise, hash it to an int.
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()
    return int(h[:16], 16) & 0x7FFFFFFF


def generate_synthetic_name(star: Dict[str, Any]) -> str:
    """
    Generate a synthetic sector/cluster style name for a star, deterministically
    based on its original catalog id (or fallback seed).

    Examples:
        Helion Sector-17
        Koros Cluster-03
        Velarn Arc-81
    """
    seed = _seed_from_star(star)
    rng = random.Random(seed)

    prefix = _SECTOR_PREFIXES[rng.randrange(len(_SECTOR_PREFIXES))]
    kind = _SECTOR_TYPES[rng.randrange(len(_SECTOR_TYPES))]
    number = rng.randrange(1, 100)  # 01-99

    return f"{prefix} {kind}-{number:02d}"


# ---------- CSV / map output ----------

def write_star_csv(stars: List[Dict[str, Any]], path: Optional[str]) -> None:
    """
    Write compact, game-ready CSV catalog.

    Rules:
    - Sort by dist_ly ascending (Sol/nearest first).
    - Replace 'id' with monotonic integer starting at 0.
      (0 will be Sol if distances are correct.)
    - Columns:
        id, proper, dist_ly, grid_x, grid_y, spect

    The `proper` column is:
      - the real catalog proper name if present, else
      - a synthetic sector/cluster name deterministically generated
        from the original catalog id (or HIP/coords fallback).
    """
    fieldnames = [
        "id",
        "proper",
        "dist_ly",
        "grid_x",
        "grid_y",
        "spect",
    ]

    # Sort by distance from Sol
    stars_sorted = sorted(stars, key=lambda s: float(s["dist_ly"]))

    out_file = None
    if path:
        out_file = open(path, "w", newline="", encoding="utf-8")
        writer_target = out_file
    else:
        writer_target = sys.stdout

    try:
        writer = csv.DictWriter(writer_target, fieldnames=fieldnames)
        writer.writeheader()
        for new_id, s in enumerate(stars_sorted):
            raw_proper = (s.get("proper") or "").strip()
            if raw_proper:
                name = raw_proper
            else:
                name = generate_synthetic_name(s)

            row = {
                "id": new_id,
                "proper": name,
                "dist_ly": s.get("dist_ly", ""),
                "grid_x": s.get("grid_x", ""),
                "grid_y": s.get("grid_y", ""),
                "spect": s.get("spect", ""),
            }
            writer.writerow(row)
    finally:
        if out_file is not None:
            out_file.close()


def write_ascii_map(
    stars: List[Dict[str, Any]], path: str, scale: float, radius_ly: float
) -> None:
    """
    Create a 100x100 ASCII map.

    Rules:
    - Start with '.' in every cell.
    - Place 'X' at Sol's cell.
    - Place '*' for other stars (one per cell by construction).
    - After placing stars, any cell still '.' whose center is beyond
      radius_ly is turned into a space ' '.
    """
    # Initialize map with dots
    grid = [["." for _ in range(100)] for _ in range(100)]

    # Find Sol
    sol_star = None
    for s in stars:
        if s.get("is_sol"):
            sol_star = s
            break

    if sol_star is None:
        # Fallback: choose nearest star as Sol if flag missing
        sol_star = min(stars, key=lambda s: s["dist_ly"])
        sol_star["is_sol"] = True

    sol_x = sol_star["grid_x"]
    sol_y = sol_star["grid_y"]

    # Mark Sol
    grid[sol_y][sol_x] = "X"

    # Mark other stars
    for s in stars:
        if s is sol_star:
            continue
        gx = s["grid_x"]
        gy = s["grid_y"]
        if 0 <= gx < 100 and 0 <= gy < 100:
            if grid[gy][gx] == ".":
                grid[gy][gx] = "*"
            # If grid[gy][gx] is 'X', leave it alone (Sol wins)

    # Now mask cells beyond radius_ly as spaces, but only for empty cells
    for gy in range(100):
        for gx in range(100):
            if grid[gy][gx] != ".":
                continue  # don't overwrite stars or Sol
            dx_cells = gx - sol_x
            dy_cells = gy - sol_y
            # Distance (in ly) from Sol based on cell offset and scale
            dist_ly = math.sqrt(dx_cells * dx_cells + dy_cells * dy_cells) * scale
            if dist_ly > radius_ly:
                grid[gy][gx] = " "

    # Write file
    try:
        with open(path, "w", encoding="utf-8") as f:
            for y in range(100):
                f.write("".join(grid[y]) + "\n")
    except OSError as e:
        print(f"ERROR: Failed to write ASCII map to '{path}': {e}", file=sys.stderr)


def main() -> None:
    args = parse_args()

    if args.scale <= 0:
        print("ERROR: --scale must be > 0.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading HYG catalog from {args.input_csv} ...", file=sys.stderr)
    stars_all = load_hyg_csv(args.input_csv)
    print(f"Loaded {len(stars_all)} stars total.", file=sys.stderr)

    print(
        f"Filtering stars within {args.radius_ly} light-years of Sol...",
        file=sys.stderr,
    )
    stars = select_stars_within_radius(stars_all, args.radius_ly, args.max_stars)

    if not stars:
        print(
            "ERROR: No stars found within the specified radius. "
            "Either the catalog is wrong or the radius is too small.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Selected {len(stars)} stars (before projection).", file=sys.stderr)

    print(
        f"Projecting to 100x100 grid with scale {args.scale} ly/cell, "
        f"pruning off-map stars and enforcing 1 star per cell (real catalog names preferred)...",
        file=sys.stderr,
    )
    stars = project_to_grid(stars, args.scale)

    if not stars:
        print(
            "ERROR: All stars were pruned during projection and collision pruning. "
            "Your --radius-ly and --scale combination leaves nothing on the map.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"{len(stars)} stars remain after projection and pruning.", file=sys.stderr)

    if args.csv_out:
        print(f"Writing star catalog CSV to {args.csv_out} ...", file=sys.stderr)
    else:
        print("Writing star catalog CSV to stdout ...", file=sys.stderr)

    write_star_csv(stars, args.csv_out)

    print(f"Writing ASCII map to {args.map_out} ...", file=sys.stderr)
    write_ascii_map(stars, args.map_out, args.scale, args.radius_ly)

    print("Done.", file=sys.stderr)


if __name__ == "__main__":
    main()
