"""Supported CLI for the preserved physical-generation implementations."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "universe_builder"
PHASES = (
    ("star_catalog", "existing; validation pending"),
    ("system_objects", "existing; validation pending"),
    ("alien_artifacts", "existing; validation pending"),
    ("initial_scenario", "planned — M2"),
    ("history_simulation", "planned — M3–M6"),
    ("world_snapshot", "planned — M7"),
    ("game_export", "planned — M8"),
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exact_keys(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f"{label} must contain exactly: {', '.join(keys)}")


def number(value, label, minimum, maximum=None, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    if integer and not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    if not math.isfinite(value) or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{label} is outside its permitted range")


def load_config(path):
    path = Path(path).resolve()
    config = json.loads(path.read_text())
    exact_keys(config, ("schema_version", "source_catalog", "phase_0", "phase_1", "phase_2"), "config")
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ValueError("Only config schema_version 1 is supported")
    exact_keys(config["phase_0"], ("radius_ly", "max_stars", "scale"), "phase_0")
    exact_keys(config["phase_1"], ("max_objects_per_system", "seed"), "phase_1")
    exact_keys(config["phase_2"], ("artifact_rate", "seed"), "phase_2")
    for key in ("radius_ly", "scale"):
        number(config["phase_0"][key], f"phase_0.{key}", 0)
        if config["phase_0"][key] == 0:
            raise ValueError(f"phase_0.{key} must be positive")
    number(config["phase_0"]["max_stars"], "phase_0.max_stars", 1, integer=True)
    number(config["phase_1"]["max_objects_per_system"], "phase_1.max_objects_per_system", 0, 5, integer=True)
    number(config["phase_2"]["artifact_rate"], "phase_2.artifact_rate", 0, 1)
    for phase in ("phase_1", "phase_2"):
        number(config[phase]["seed"], f"{phase}.seed", 0, 2**32 - 1, integer=True)
    if not isinstance(config["source_catalog"], str) or not config["source_catalog"]:
        raise ValueError("source_catalog must be a nonempty path string")
    source = (path.parent / config["source_catalog"]).resolve()
    if not source.is_file():
        raise ValueError(f"Source catalog does not exist: {source}")
    return config, source


def verify_baseline():
    manifest = json.loads((PACKAGE / "data/baseline/manifest.json").read_text())
    failures = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or digest(path) != item["sha256"]:
            failures.append(item["path"])
    if failures:
        raise ValueError("Baseline preservation check failed: " + ", ".join(failures))
    print(f"Verified {len(manifest['files'])} preserved source/baseline files; phase correctness remains unvalidated.")


def commands(config, source, output, through):
    p0, p1, p2 = (config[f"phase_{i}"] for i in range(3))
    args = [
        ["--input-csv", str(source), "--radius-ly", str(p0["radius_ly"]),
         "--max-stars", str(p0["max_stars"]), "--scale", str(p0["scale"]),
         "--csv-out", str(output / "phase_0/star_catalog.csv"),
         "--map-out", str(output / "phase_0/star_map.txt")],
        ["--input-stars", str(output / "phase_0/star_catalog.csv"),
         "--output-objects", str(output / "phase_1/system_objects.csv"),
         "--max-objects-per-system", str(p1["max_objects_per_system"]), "--seed", str(p1["seed"])],
        ["--input-objects", str(output / "phase_1/system_objects.csv"),
         "--output-objects", str(output / "phase_2/system_objects.csv"),
         "--artifact-rate", str(p2["artifact_rate"]), "--seed", str(p2["seed"])],
    ]
    return [
        [sys.executable, str(PACKAGE / "phases" / f"phase_{i}_{PHASES[i][0]}.py"), *args[i]]
        for i in range(through + 1)
    ]


def generate(config_path, output, through=2):
    if type(through) is not int or through not in (0, 1, 2):
        raise ValueError("Only phases 0–2 are implemented")
    config, source = load_config(config_path)
    output = Path(output).resolve()
    data = (PACKAGE / "data").resolve()
    if output == data or data in output.parents:
        raise ValueError("Generation output cannot be inside preserved source/baseline data")
    if output.exists():
        raise ValueError(f"Output directory already exists; choose a new directory: {output}")
    jobs = commands(config, source, output, through)
    manifest = {
        "schema_version": 1,
        "status": "running",
        "python_version": platform.python_version(),
        "config": config,
        "source": {"path": str(source), "sha256": digest(source)},
        "runner_sha256": digest(__file__),
        "implementations": {str(Path(job[1]).relative_to(ROOT)): digest(job[1]) for job in jobs},
        "through_phase": through,
        "completed_phases": [],
        "commands": jobs,
        "outputs": {},
    }
    output.mkdir(parents=True, exist_ok=False)
    manifest_path = output / "manifest.json"

    def save_manifest():
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    save_manifest()
    try:
        for i, job in enumerate(jobs):
            phase_dir = output / f"phase_{i}"
            phase_dir.mkdir()
            subprocess.run(job, check=True, cwd=output)
            expected = ("star_catalog.csv", "star_map.txt") if i == 0 else ("system_objects.csv",)
            for name in expected:
                path = phase_dir / name
                manifest["outputs"][str(path.relative_to(output))] = digest(path)
            manifest["completed_phases"].append(i)
            save_manifest()
    except (Exception, KeyboardInterrupt) as exc:
        manifest["status"] = "failed"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        save_manifest()
        raise
    manifest["status"] = "complete"
    save_manifest()
    print(f"Generated phases 0–{through} in {output}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="Show implemented and planned phase status")
    sub.add_parser("verify-baseline", help="Read-only preservation hash check")
    run = sub.add_parser("generate", help="Generate implemented phases into a new directory")
    run.add_argument("--config", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--through", type=int, choices=(0, 1, 2), default=2)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for i, (name, status) in enumerate(PHASES):
                print(f"{i}: {name} — {status}")
        elif args.command == "verify-baseline":
            verify_baseline()
        else:
            generate(args.config, args.output, args.through)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
