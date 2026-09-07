#!/usr/bin/env python3
"""generate_alien_artifacts.py

Phase 2: Alien Ruins & Artifacts Generator.

Reads a Phase-1 `system_objects.csv` (natural objects only) and writes an
augmented CSV that includes:

    artifact_flag  (0/1)
    artifact_type  (ARC, RUI, FAC, BEA, ENG, TEC, or empty)

Artifact placement is deterministic and based solely on (system_id, object_id)
and object class, so it is stable across runs and independent of Phase-1 RNG.
"""

import argparse
import csv
import hashlib
from typing import List, Tuple


# Eligible classes for artifacts (non–gas giant)
ELIGIBLE_CLASSES = {"RP", "DP", "IC", "RM", "IM", "AS"}

# Artifact type distribution: (code, weight)
ARTIFACT_TYPES: List[Tuple[str, int]] = [
    ("ARC", 40),  # Alien Relic / Data Crystal
    ("RUI", 25),  # Ruined Surface Complex
    ("FAC", 15),  # Abandoned Orbital Facility
    ("BEA", 10),  # Beacon / Signal Source
    ("ENG", 7),   # Exotic Energy Node
    ("TEC", 3),   # Technology Cache
]


def hash32(key: str) -> int:
    """Return a 32-bit integer hash from SHA-256(key)."""
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big")


def choose_artifact_type(h_extra: int) -> str:
    """Choose an artifact type from ARTIFACT_TYPES using h_extra as a source of entropy."""
    total = sum(weight for _, weight in ARTIFACT_TYPES)
    r = h_extra % total
    acc = 0
    for code, weight in ARTIFACT_TYPES:
        acc += weight
        if r < acc:
            return code
    return ARTIFACT_TYPES[-1][0]


def process_file(input_path: str, output_path: str, rate: float, seed: int) -> None:
    with open(input_path, newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        if reader.fieldnames is None:
            raise SystemExit("Input system_objects.csv has no header row.")

        fieldnames = list(reader.fieldnames)
        # Append artifact columns if not already present
        if "artifact_flag" not in fieldnames:
            fieldnames.append("artifact_flag")
        if "artifact_type" not in fieldnames:
            fieldnames.append("artifact_type")

        rows = list(reader)

    out_rows = []
    for row in rows:
        cls = (row.get("class") or "").strip().upper()
        sid = (row.get("system_id") or "").strip()
        oid = (row.get("object_id") or "").strip()

        # Include the global seed in the hash key so different seeds
        # produce different—but still deterministic—artifact layouts.
        key = f"{seed}:{sid}:{oid}:artifact"
        h = hashlib.sha256(key.encode("utf-8")).digest()
        h_main = int.from_bytes(h[:4], "big")
        h_extra = int.from_bytes(h[4:8], "big")

        eligible = cls in ELIGIBLE_CLASSES

        if not eligible:
            # No artifacts on ineligible classes (e.g., gas giants)
            row["artifact_flag"] = "0"
            row["artifact_type"] = ""
        else:
            p = h_main / (2 ** 32)
            if p < rate:
                row["artifact_flag"] = "1"
                row["artifact_type"] = choose_artifact_type(h_extra)
            else:
                row["artifact_flag"] = "0"
                row["artifact_type"] = ""

        out_rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in out_rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Phase 2: Add alien artifact flags/types to a Phase-1 system_objects.csv "
            "in a deterministic way."
        )
    )
    ap.add_argument(
        "--input-objects",
        required=True,
        help="Path to input system_objects.csv (Phase-1 output).",
    )
    ap.add_argument(
        "--output-objects",
        required=True,
        help="Path to output augmented system_objects.csv (Phase-2 output).",
    )
    ap.add_argument(
        "--artifact-rate",
        type=float,
        default=0.02,
        help=(
            "Per-object probability for eligible classes to host artifacts, "
            "used as a deterministic threshold on hash-derived p (default: 0.02)."
        ),
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=0,
        help=("Global deterministic seed offset mixed into artifact hashing (default: 0)."),
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    if not (0.0 <= args.artifact_rate <= 1.0):
        raise SystemExit("--artifact-rate must be between 0.0 and 1.0")
    process_file(args.input_objects, args.output_objects, args.artifact_rate, args.seed)


if __name__ == "__main__":
    main()
