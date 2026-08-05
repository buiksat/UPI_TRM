#!/usr/bin/env python3
"""Focused standard-library tests for registered confirmatory execution."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).with_name("run_registered_matrix.py")
SPEC = importlib.util.spec_from_file_location("run_registered_matrix", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {SCRIPT_PATH}.")
MATRIX_RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATRIX_RUNNER)


class FakeConfirmatoryProcess:
    def __init__(self, *, fail_run_id: str | None = None) -> None:
        self.fail_run_id = fail_run_id
        self._lock = threading.Lock()
        self._active_devices: set[str] = set()
        self.max_global_concurrency = 0
        self.max_device_concurrency: dict[str, int] = {}
        self.starts: dict[str, list[str]] = {}
        self.call_count = 0

    @staticmethod
    def _argument(command: list[str], flag: str) -> str:
        return command[command.index(flag) + 1]

    def __call__(
        self,
        command: list[str],
        *,
        cwd: Path,
        env: dict[str, str],
        stdout: object,
        stderr: object,
    ) -> subprocess.CompletedProcess[bytes]:
        del cwd, stderr
        run_id = self._argument(command, "--run-id")
        seed = int(self._argument(command, "--seed"))
        attempt = int(self._argument(command, "--attempt-index"))
        commit = self._argument(command, "--expected-producer-git-commit")
        config_hash = self._argument(command, "--expected-effective-config-sha256")
        eval_manifest = self._argument(command, "--eval-manifest-sha256")
        eval_split = self._argument(command, "--eval-split")
        eval_count = int(self._argument(command, "--eval-pool-size"))
        budget = int(self._argument(command, "--env-step-budget"))
        eval_interval = int(self._argument(command, "--eval-env-interval"))
        save_interval = int(self._argument(command, "--save-env-interval"))
        device = env["CUDA_VISIBLE_DEVICES"]
        self.assert_confirmatory_command(command)

        with self._lock:
            if device in self._active_devices:
                raise AssertionError(f"Concurrent runs on CUDA binding {device}.")
            self._active_devices.add(device)
            self.max_global_concurrency = max(
                self.max_global_concurrency, len(self._active_devices)
            )
            self.max_device_concurrency[device] = max(
                self.max_device_concurrency.get(device, 0), 1
            )
            self.starts.setdefault(device, []).append(run_id)
            self.call_count += 1
        try:
            time.sleep(0.02)
            stdout.write(f"mock run {run_id}\n".encode("ascii"))
            if run_id == self.fail_run_id:
                return subprocess.CompletedProcess(command, 17)
            checkpoint_root = (
                Path(self._argument(command, "--checkpoint-dir"))
                / f"attempt_{attempt:04d}"
            )
            evaluation_root = (
                Path(self._argument(command, "--evaluation-artifact-dir"))
                / run_id
                / f"attempt_{attempt:04d}"
            )
            checkpoint_root.mkdir(parents=True)
            evaluation_root.mkdir(parents=True)
            for milestone in range(save_interval, budget + 1, save_interval):
                checkpoint = checkpoint_root / f"rl_checkpoint_step_{milestone}.pt"
                checkpoint.write_bytes(f"{run_id}:{milestone}\n".encode("ascii"))
            for milestone in range(eval_interval, budget + 1, eval_interval):
                checkpoint = checkpoint_root / f"rl_checkpoint_step_{milestone}.pt"
                artifact_dir = evaluation_root / f"env_steps_{milestone:012d}"
                artifact_dir.mkdir()
                metadata = {
                    "checkpoint_environment_steps": milestone,
                    "checkpoint_outer_steps": milestone // eval_interval,
                    "checkpoint_sha256": MATRIX_RUNNER.sha256_file(checkpoint),
                    "dataset": {
                        "manifest_sha256": eval_manifest,
                        "record_count": eval_count,
                        "split": eval_split,
                    },
                    "effective_config_sha256": config_hash,
                    "producer_git_commit": commit,
                    "run_id": run_id,
                    "training_seed": seed,
                }
                compute = {
                    "progress": {
                        "environment_interactions": milestone,
                        "optimizer_steps_by_kind": {
                            "policy": milestone // eval_interval
                        },
                        "optimizer_steps_total": milestone // eval_interval,
                        "outer_updates": milestone // eval_interval,
                    }
                }
                metadata_path = artifact_dir / "evaluation_metadata.json"
                compute_path = artifact_dir / "compute_snapshot.json"
                per_instance_path = artifact_dir / "per_instance.jsonl"
                metadata_path.write_bytes(MATRIX_RUNNER.canonical_json_bytes(metadata))
                compute_path.write_bytes(MATRIX_RUNNER.canonical_json_bytes(compute))
                per_instance_path.write_text(
                    "".join(
                        json.dumps({"record": index, "solved": False}) + "\n"
                        for index in range(eval_count)
                    ),
                    encoding="ascii",
                )
                summary = {
                    "compute_snapshot_sha256": MATRIX_RUNNER.sha256_file(compute_path),
                    "metadata_sha256": MATRIX_RUNNER.sha256_file(metadata_path),
                    "per_instance_sha256": MATRIX_RUNNER.sha256_file(per_instance_path),
                    "record_count": eval_count,
                    "total_environment_interactions": eval_count * 2,
                }
                (artifact_dir / "summary.json").write_bytes(
                    MATRIX_RUNNER.canonical_json_bytes(summary)
                )
            return subprocess.CompletedProcess(command, 0)
        finally:
            with self._lock:
                self._active_devices.remove(device)

    @staticmethod
    def assert_confirmatory_command(command: list[str]) -> None:
        if "--confirmatory" not in command:
            raise AssertionError("Mock received a non-confirmatory command.")
        tier_index = command.index("--confirmatory-tier")
        if command[tier_index + 1] != "confirmatory":
            raise AssertionError("Mock received the wrong execution tier.")


class ConfirmatoryExecutionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.code_root = self.root / "code"
        self.config_root = self.code_root / "configs" / "iclr_confirmatory"
        self.config_root.mkdir(parents=True)
        self.evidence_root = self.root / "evidence"
        self.bundle = self.root / "locks"
        self.par = self.root / "trainer.par"
        self.par.write_text("#!/bin/sh\nexit 99\n", encoding="ascii")
        self.par.chmod(0o755)
        self.commit = "a" * 40
        self.matrix = {
            "architecture_cli": {
                "backbone": "trm",
                "h_cycles": 2,
                "hidden_size": 8,
                "l_cycles": 2,
                "l_layers": 1,
                "puzzle_emb_ndim": 0,
            },
            "bridge_cells": {"A": ["a.yaml"]},
            "confirmatory_seeds": [1, 2],
            "dataset": {
                "root": "data",
                "test_count": 2,
                "test_manifest_sha256": "b" * 64,
                "test_split": "test",
                "train_count": 4,
                "train_manifest_sha256": "c" * 64,
                "train_split": "train",
            },
            "environment_interactions": 20,
            "evaluation_environment_interval": 10,
            "log_environment_interval": 10,
            "matched_cells": {"B": ["b.yaml"]},
            "reported_environment_checkpoints": [10, 20],
            "run_id_templates": {
                "confirmatory": "{cell_lower}-seed{seed}",
                "debug": "debug-{cell_lower}-seed{seed}",
            },
            "save_environment_interval": 10,
            "save_outer_interval": 0,
            "status": "authorized",
        }
        self.matrix_path = self.config_root / "run_matrix.json"
        self._write_matrix()
        self._write_lock_bundle()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_matrix(self) -> None:
        self.matrix_path.write_bytes(MATRIX_RUNNER.canonical_json_bytes(self.matrix))

    def _write_lock_bundle(self) -> None:
        if self.bundle.exists():
            shutil.rmtree(self.bundle)
        self.bundle.mkdir()
        registry_hash = MATRIX_RUNNER.sha256_file(self.matrix_path)
        records = []
        assignments = [("A", 1, "0"), ("A", 2, "1"), ("B", 1, "0"), ("B", 2, "1")]
        for cell, seed, device in assignments:
            run_id = f"{cell.lower()}-seed{seed}"
            effective_config = {"registration": {"run_id": run_id}}
            config_hash = MATRIX_RUNNER.canonical_json_value_sha256(effective_config)
            lock = {
                "attempt_index": 0,
                "confirmatory_cell": cell,
                "confirmatory_tier": "confirmatory",
                "effective_config": effective_config,
                "effective_config_sha256": config_hash,
                "lock_schema_version": 3,
                "producer_git_commit": self.commit,
                "registry_sha256": registry_hash,
                "run_id": run_id,
                "training_seed": seed,
            }
            lock_name = f"{run_id}.lock.json"
            lock_bytes = MATRIX_RUNNER.canonical_json_bytes(lock)
            (self.bundle / lock_name).write_bytes(lock_bytes)
            records.append(
                {
                    "attempt_index": 0,
                    "cell": cell,
                    "config_layers": [f"{cell.lower()}.yaml"],
                    "cuda_visible_devices": device,
                    "effective_config_sha256": config_hash,
                    "lock_file": lock_name,
                    "lock_sha256": MATRIX_RUNNER.sha256_bytes(lock_bytes),
                    "run_id": run_id,
                    "seed": seed,
                }
            )
        index = {
            "attempt_index": 0,
            "bundle_schema_version": 2,
            "excluded_from_confirmatory": False,
            "producer_git_commit": self.commit,
            "registry_sha256": registry_hash,
            "run_count": len(records),
            "runs": records,
            "tier": "confirmatory",
        }
        self._rewrite_bundle_index(index)

    def _rewrite_bundle_index(self, index: dict[str, object]) -> None:
        index_bytes = MATRIX_RUNNER.canonical_json_bytes(index)
        (self.bundle / "index.json").write_bytes(index_bytes)
        (self.bundle / "index.json.sha256").write_text(
            MATRIX_RUNNER.sha256_bytes(index_bytes) + "  index.json\n",
            encoding="ascii",
        )

    def _arguments(self) -> argparse.Namespace:
        return argparse.Namespace(
            code_root=self.code_root,
            evidence_root=self.evidence_root,
            lock_bundle=self.bundle,
            par=self.par,
        )

    def test_executes_device_queues_and_publishes_hashed_index(self) -> None:
        fake = FakeConfirmatoryProcess()
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            MATRIX_RUNNER.execute_confirmatory(self._arguments())

        output = self.evidence_root / "confirmatory_execution_attempt_0000_index.json"
        self.assertTrue(output.is_file())
        execution = MATRIX_RUNNER.load_json(output)
        self.assertEqual(execution["run_count"], 4)
        self.assertEqual(execution["tier"], "confirmatory")
        self.assertIs(execution["excluded_from_confirmatory"], False)
        self.assertEqual(
            [record["run_id"] for record in execution["runs"]],
            ["a-seed1", "a-seed2", "b-seed1", "b-seed2"],
        )
        for record in execution["runs"]:
            self.assertEqual(
                [
                    item["checkpoint_environment_steps"]
                    for item in record["evaluations"]
                ],
                [10, 20],
            )
            self.assertEqual(
                record["evaluations"][-1]["progress_counters"][
                    "environment_interactions"
                ],
                20,
            )
        self.assertEqual(fake.max_global_concurrency, 2)
        self.assertEqual(fake.max_device_concurrency, {"0": 1, "1": 1})
        self.assertEqual(fake.starts["0"], ["a-seed1", "b-seed1"])
        self.assertEqual(fake.starts["1"], ["a-seed2", "b-seed2"])
        self.assertEqual(
            output.read_bytes(), MATRIX_RUNNER.canonical_json_bytes(execution)
        )

        calls_before_retry = fake.call_count
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
                MATRIX_RUNNER.execute_confirmatory(self._arguments())
        self.assertEqual(fake.call_count, calls_before_retry)

    def test_failure_retains_log_and_does_not_publish_index(self) -> None:
        fake = FakeConfirmatoryProcess(fail_run_id="a-seed1")
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            with self.assertRaisesRegex(
                RuntimeError, "no execution index was published"
            ):
                MATRIX_RUNNER.execute_confirmatory(self._arguments())

        self.assertFalse(
            (
                self.evidence_root / "confirmatory_execution_attempt_0000_index.json"
            ).exists()
        )
        failed_log = (
            self.evidence_root / "logs" / "a-seed1" / "attempt_0000" / "run.log"
        )
        self.assertEqual(failed_log.read_text(encoding="ascii"), "mock run a-seed1\n")

    def test_rejects_partial_registered_product_before_launch(self) -> None:
        index = MATRIX_RUNNER.load_json(self.bundle / "index.json")
        index["runs"] = index["runs"][:-1]
        index["run_count"] = len(index["runs"])
        self._rewrite_bundle_index(index)
        fake = FakeConfirmatoryProcess()
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "complete registered"):
                MATRIX_RUNNER.execute_confirmatory(self._arguments())
        self.assertEqual(fake.call_count, 0)

    def test_rejects_overlapping_and_malformed_cuda_bindings(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "overlapping bindings"):
            MATRIX_RUNNER.normalize_cuda_devices(["0", "0"])
        for binding in ("0,1", "00", "-1", "all", " GPU-ignored"):
            with self.subTest(binding=binding), self.assertRaises(RuntimeError):
                MATRIX_RUNNER.normalize_cuda_device(binding)

        index = MATRIX_RUNNER.load_json(self.bundle / "index.json")
        index["runs"][0]["cuda_visible_devices"] = "0,1"
        self._rewrite_bundle_index(index)
        fake = FakeConfirmatoryProcess()
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "one canonical"):
                MATRIX_RUNNER.execute_confirmatory(self._arguments())
        self.assertEqual(fake.call_count, 0)

    def test_atomic_publish_does_not_replace_a_racing_writer(self) -> None:
        output = self.root / "published.json"
        payloads = (b'{"writer":1}\n', b'{"writer":2}\n')
        barrier = threading.Barrier(2)
        successes: list[bytes] = []
        failures: list[Exception] = []
        outcome_lock = threading.Lock()

        def publish(payload: bytes) -> None:
            barrier.wait()
            try:
                MATRIX_RUNNER.publish_bytes_no_replace(output, payload)
            except Exception as exc:
                with outcome_lock:
                    failures.append(exc)
            else:
                with outcome_lock:
                    successes.append(payload)

        threads = [
            threading.Thread(target=publish, args=(payload,)) for payload in payloads
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(successes), 1)
        self.assertEqual(len(failures), 1)
        self.assertIsInstance(failures[0], RuntimeError)
        self.assertEqual(output.read_bytes(), successes[0])
        self.assertEqual(list(output.parent.glob(f".{output.name}.stage.*")), [])

    def test_separates_save_and_evaluation_milestones(self) -> None:
        self.matrix["save_environment_interval"] = 5
        self._write_matrix()
        self._write_lock_bundle()
        fake = FakeConfirmatoryProcess()
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            MATRIX_RUNNER.execute_confirmatory(self._arguments())

        output = self.evidence_root / "confirmatory_execution_attempt_0000_index.json"
        execution = MATRIX_RUNNER.load_json(output)
        for record in execution["runs"]:
            self.assertEqual(
                sorted(record["checkpoint_files"]),
                [
                    "rl_checkpoint_step_10.pt",
                    "rl_checkpoint_step_15.pt",
                    "rl_checkpoint_step_20.pt",
                    "rl_checkpoint_step_5.pt",
                ],
            )
            self.assertEqual(
                [
                    evaluation["checkpoint_environment_steps"]
                    for evaluation in record["evaluations"]
                ],
                [10, 20],
            )

    def test_rejects_unauthorized_matrix_before_launch(self) -> None:
        self.matrix["status"] = "registered_not_authorized"
        self._write_matrix()
        fake = FakeConfirmatoryProcess()
        with mock.patch.object(
            MATRIX_RUNNER, "producer_commit", return_value=self.commit
        ), mock.patch.object(MATRIX_RUNNER.subprocess, "run", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "status exactly authorized"):
                MATRIX_RUNNER.execute_confirmatory(self._arguments())
        self.assertEqual(fake.call_count, 0)


if __name__ == "__main__":
    unittest.main()
