"""Runner contract tests; these deliberately do not validate generator algorithms."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from universe_builder import __main__ as runner


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.source = self.directory / "source.csv"
        self.source.write_text("fixture input\n")
        self.config = json.loads((runner.PACKAGE / "configs/baseline.json").read_text())
        self.config["source_catalog"] = "source.csv"
        self.config_path = self.directory / "config.json"
        self.save_config()
        self.output = self.directory / "run"

    def save_config(self):
        self.config_path.write_text(json.dumps(self.config))

    def test_source_resolves_relative_to_config(self):
        _, source = runner.load_config(self.config_path)
        self.assertEqual(source, self.source.resolve())

    def test_invalid_config_creates_no_output(self):
        original = copy.deepcopy(self.config)
        cases = [("phase_0", "scale", 0), ("phase_0", "radius_ly", float("nan")),
                 ("phase_0", "max_stars", True), ("phase_1", "seed", -1),
                 ("phase_1", "max_objects_per_system", 6), ("phase_2", "artifact_rate", 1.1)]
        for phase, key, value in cases:
            with self.subTest(key=key):
                self.config = copy.deepcopy(original)
                self.config[phase][key] = value
                self.save_config()
                with self.assertRaises(ValueError):
                    runner.generate(self.config_path, self.output)
                self.assertFalse(self.output.exists())

    def test_unknown_setting_is_rejected(self):
        self.config["phase_2"]["artifcat_rate"] = 0.1
        self.save_config()
        with self.assertRaises(ValueError):
            runner.load_config(self.config_path)

    def test_existing_output_is_untouched(self):
        self.output.mkdir()
        sentinel = self.output / "sentinel"
        sentinel.write_text("keep")
        with patch.object(runner.subprocess, "run") as run:
            with self.assertRaises(ValueError):
                runner.generate(self.config_path, self.output)
            run.assert_not_called()
        self.assertEqual(sentinel.read_text(), "keep")

    def test_preserved_data_cannot_be_output(self):
        with self.assertRaises(ValueError):
            runner.generate(self.config_path, runner.PACKAGE / "data/baseline/new-run")

    def test_planned_phase_is_rejected(self):
        with self.assertRaises(ValueError):
            runner.generate(self.config_path, self.output, 3)
        self.assertFalse(self.output.exists())

    def fake_phase(self, job, **kwargs):
        for option in ("--csv-out", "--map-out", "--output-objects"):
            if option in job:
                Path(job[job.index(option) + 1]).write_text("fixture output\n")
        return subprocess.CompletedProcess(job, 0)

    def test_dependency_commands_and_provenance(self):
        with patch.object(runner.subprocess, "run", side_effect=self.fake_phase) as run:
            runner.generate(self.config_path, self.output)
        jobs = [call.args[0] for call in run.call_args_list]
        self.assertEqual(len(jobs), 3)
        self.assertEqual(jobs[1][jobs[1].index("--input-stars") + 1],
                         jobs[0][jobs[0].index("--csv-out") + 1])
        self.assertEqual(jobs[2][jobs[2].index("--input-objects") + 1],
                         jobs[1][jobs[1].index("--output-objects") + 1])
        self.assertTrue(jobs[2][1].endswith("phase_2_alien_artifacts.py"))
        manifest = json.loads((self.output / "manifest.json").read_text())
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(manifest["completed_phases"], [0, 1, 2])
        self.assertEqual(manifest["source"]["sha256"], runner.digest(self.source))
        self.assertEqual(len(manifest["implementations"]), 3)
        self.assertEqual(len(manifest["outputs"]), 4)
        for name, checksum in manifest["outputs"].items():
            self.assertEqual(runner.digest(self.output / name), checksum)

    def test_stop_after_phase_zero(self):
        with patch.object(runner.subprocess, "run", side_effect=self.fake_phase) as run:
            runner.generate(self.config_path, self.output, 0)
        self.assertEqual(run.call_count, 1)
        self.assertFalse((self.output / "phase_1").exists())

    def test_failure_records_completed_work(self):
        def fail_second(job, **kwargs):
            if "--input-stars" in job:
                raise subprocess.CalledProcessError(1, job)
            return self.fake_phase(job, **kwargs)
        with patch.object(runner.subprocess, "run", side_effect=fail_second):
            with self.assertRaises(subprocess.CalledProcessError):
                runner.generate(self.config_path, self.output)
        manifest = json.loads((self.output / "manifest.json").read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["completed_phases"], [0])
        self.assertTrue((self.output / "phase_0/star_catalog.csv").is_file())

    def test_missing_phase_output_marks_failure(self):
        with patch.object(runner.subprocess, "run"):
            with self.assertRaises(FileNotFoundError):
                runner.generate(self.config_path, self.output, 0)
        manifest = json.loads((self.output / "manifest.json").read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["completed_phases"], [])


if __name__ == "__main__":
    unittest.main()
