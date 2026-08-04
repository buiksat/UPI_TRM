#!/usr/bin/env python3
"""Prepare immutable run locks and execute registered debug-only smoke runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Sequence


LOCK_PREFIX = "[CONFIRMATORY_LOCK] "


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="ascii"))
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object in {path}.")
    return value


def producer_commit(code_root: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(code_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    commit = completed.stdout.strip()
    if len(commit) != 40:
        raise RuntimeError("Producer Git commit is not a full 40-character hash.")
    return commit


def matrix_cells(matrix: dict[str, Any]) -> dict[str, list[str]]:
    cells: dict[str, list[str]] = {}
    for section in ("bridge_cells", "matched_cells"):
        raw = matrix.get(section)
        if not isinstance(raw, dict):
            raise RuntimeError(f"Run matrix is missing {section}.")
        for cell, layers in raw.items():
            if not isinstance(cell, str) or not isinstance(layers, list):
                raise RuntimeError(f"Malformed cell in {section}.")
            if not all(isinstance(layer, str) for layer in layers):
                raise RuntimeError(f"Malformed config layers for {cell}.")
            cells[cell] = list(layers)
    return cells


def tier_spec(matrix: dict[str, Any], tier: str) -> dict[str, Any]:
    dataset = matrix["dataset"]
    if tier == "debug":
        debug = matrix["debug_runs"]
        return {
            "seeds": list(debug["seeds"]),
            "eval_split": str(debug["evaluation_split"]),
            "eval_count": int(dataset["validation_count"]),
            "eval_manifest": str(dataset["validation_manifest_sha256"]),
            "extra_layers": list(debug["config_layers"]),
            "budget": int(debug["environment_interactions"]),
            "log_interval": int(debug["log_environment_interval"]),
            "eval_interval": int(debug["evaluation_environment_interval"]),
            "save_interval": int(debug["save_environment_interval"]),
            "save_outer_interval": int(debug["save_outer_interval"]),
        }
    if matrix.get("status") != "authorized":
        raise RuntimeError(
            "Confirmatory locks require an authorized, frozen run matrix. "
            f"Current status is {matrix.get('status')!r}."
        )
    return {
        "seeds": list(matrix["confirmatory_seeds"]),
        "eval_split": str(dataset["test_split"]),
        "eval_count": int(dataset["test_count"]),
        "eval_manifest": str(dataset["test_manifest_sha256"]),
        "extra_layers": [],
        "budget": int(matrix["environment_interactions"]),
        "log_interval": int(matrix["log_environment_interval"]),
        "eval_interval": int(matrix["evaluation_environment_interval"]),
        "save_interval": int(matrix["save_environment_interval"]),
        "save_outer_interval": int(matrix["save_outer_interval"]),
    }


def registered_run_id(
    matrix: dict[str, Any], tier: str, cell: str, seed: int
) -> str:
    template = matrix["run_id_templates"][tier]
    return str(template).format(cell_lower=cell.lower(), seed=seed)


def run_command(
    *,
    par: Path,
    code_root: Path,
    evidence_root: Path,
    matrix: dict[str, Any],
    tier: str,
    cell: str,
    seed: int,
    layers: Sequence[str],
    expected_commit: str,
    effective_config_sha256: str | None,
) -> list[str]:
    dataset = matrix["dataset"]
    spec = tier_spec(matrix, tier)
    architecture = matrix["architecture_cli"]
    run_id = registered_run_id(matrix, tier, cell, seed)
    command = [
        str(par),
        "--dataset-paths",
        str((code_root / dataset["root"]).resolve()),
        "--train-split",
        str(dataset["train_split"]),
        "--eval-split",
        str(spec["eval_split"]),
        "--train-pool-size",
        str(dataset["train_count"]),
        "--eval-pool-size",
        str(spec["eval_count"]),
        "--seed",
        str(seed),
        "--run-id",
        run_id,
        "--confirmatory",
        "--confirmatory-cell",
        cell,
        "--confirmatory-tier",
        tier,
        "--evaluation-artifact-dir",
        str((evidence_root / "evaluations").resolve()),
        "--expected-producer-git-commit",
        expected_commit,
        "--train-manifest-sha256",
        str(dataset["train_manifest_sha256"]),
        "--eval-manifest-sha256",
        str(spec["eval_manifest"]),
        "--producer-repo-root",
        str(code_root),
        "--checkpoint-dir",
        str((evidence_root / "checkpoints" / run_id).resolve()),
        "--save-interval",
        str(spec["save_outer_interval"]),
        "--env-step-budget",
        str(spec["budget"]),
        "--log-env-interval",
        str(spec["log_interval"]),
        "--eval-env-interval",
        str(spec["eval_interval"]),
        "--save-env-interval",
        str(spec["save_interval"]),
        "--backbone",
        str(architecture["backbone"]),
        "--hidden-size",
        str(architecture["hidden_size"]),
        "--h-cycles",
        str(architecture["h_cycles"]),
        "--l-cycles",
        str(architecture["l_cycles"]),
        "--l-layers",
        str(architecture["l_layers"]),
        "--puzzle-emb-ndim",
        str(architecture["puzzle_emb_ndim"]),
    ]
    if effective_config_sha256 is None:
        command.append("--prepare-confirmatory-lock")
    else:
        command.extend(
            ["--expected-effective-config-sha256", effective_config_sha256]
        )
    config_dir = code_root / "configs" / "iclr_confirmatory"
    for layer in [*layers, *spec["extra_layers"]]:
        command.extend(["--config", str((config_dir / layer).resolve())])
    return command


def select_requested(
    registered: Sequence[Any], requested: Sequence[Any] | None, kind: str
) -> list[Any]:
    selected = list(registered if requested is None else requested)
    unknown = [value for value in selected if value not in registered]
    if unknown:
        raise RuntimeError(f"Unregistered {kind}: {unknown}.")
    if len(selected) != len(set(selected)):
        raise RuntimeError(f"Duplicate {kind} requested.")
    return selected


def prepare_locks(args: argparse.Namespace) -> None:
    code_root = args.code_root.resolve()
    par = args.par.resolve()
    evidence_root = args.evidence_root.resolve()
    matrix_path = code_root / "configs" / "iclr_confirmatory" / "run_matrix.json"
    matrix = load_json(matrix_path)
    cells_by_name = matrix_cells(matrix)
    spec = tier_spec(matrix, args.tier)
    cells = select_requested(list(cells_by_name), args.cells, "cells")
    seeds = select_requested(spec["seeds"], args.seeds, "seeds")
    devices = list(args.cuda_visible_devices)
    if not devices or len(devices) != len(set(devices)):
        raise RuntimeError("CUDA device list must be nonempty and unique.")
    if args.output.exists():
        raise RuntimeError(f"Refusing to overwrite lock bundle {args.output}.")
    if not par.is_file() or not os.access(par, os.X_OK):
        raise RuntimeError(f"PAR is missing or not executable: {par}.")

    commit = producer_commit(code_root)
    registry_sha256 = sha256_file(matrix_path)
    planned = [
        (cell, seed, devices[index % len(devices)])
        for index, (cell, seed) in enumerate(
            (cell, seed) for cell in cells for seed in seeds
        )
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{args.output.name}.stage.", dir=args.output.parent))
    try:
        records: list[dict[str, Any]] = []
        for cell, seed, device in planned:
            run_id = registered_run_id(matrix, args.tier, cell, seed)
            command = run_command(
                par=par,
                code_root=code_root,
                evidence_root=evidence_root,
                matrix=matrix,
                tier=args.tier,
                cell=cell,
                seed=seed,
                layers=cells_by_name[cell],
                expected_commit=commit,
                effective_config_sha256=None,
            )
            environment = os.environ.copy()
            environment["CUDA_VISIBLE_DEVICES"] = device
            environment["PYTHONUNBUFFERED"] = "1"
            print(f"[LOCK] {run_id} CUDA_VISIBLE_DEVICES={device}", flush=True)
            completed = subprocess.run(
                command,
                cwd=code_root,
                env=environment,
                capture_output=True,
                text=True,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    f"Lock preflight failed for {run_id}.\n"
                    f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
                )
            lock_lines = [
                line[len(LOCK_PREFIX) :]
                for line in completed.stdout.splitlines()
                if line.startswith(LOCK_PREFIX)
            ]
            if len(lock_lines) != 1:
                raise RuntimeError(
                    f"Expected one lock for {run_id}; observed {len(lock_lines)}."
                )
            lock = json.loads(lock_lines[0])
            if not isinstance(lock, dict):
                raise RuntimeError(f"Malformed lock for {run_id}.")
            expected_fields = {
                "confirmatory_cell": cell,
                "confirmatory_tier": args.tier,
                "run_id": run_id,
                "training_seed": seed,
                "producer_git_commit": commit,
                "registry_sha256": registry_sha256,
            }
            for field, expected in expected_fields.items():
                if lock.get(field) != expected:
                    raise RuntimeError(
                        f"Lock field {field} for {run_id} is {lock.get(field)!r}; "
                        f"expected {expected!r}."
                    )
            effective_config = lock.get("effective_config")
            if not isinstance(effective_config, dict):
                raise RuntimeError(f"Lock effective config is missing for {run_id}.")
            runtime_fingerprint = effective_config.get("runtime_fingerprint")
            if runtime_fingerprint is not None:
                runtime_environment = runtime_fingerprint[
                    "determinism_environment"
                ]
                if runtime_environment.get("CUDA_VISIBLE_DEVICES") != device:
                    raise RuntimeError(f"Lock GPU binding is wrong for {run_id}.")
            else:
                runtime_hash = effective_config.get("runtime_fingerprint_sha256")
                if not isinstance(runtime_hash, str) or len(runtime_hash) != 64:
                    raise RuntimeError(
                        f"Lock runtime fingerprint hash is missing for {run_id}."
                    )
            lock_bytes = canonical_json_bytes(lock)
            lock_name = f"{run_id}.lock.json"
            (stage / lock_name).write_bytes(lock_bytes)
            records.append(
                {
                    "cell": cell,
                    "config_layers": [
                        *cells_by_name[cell],
                        *spec["extra_layers"],
                    ],
                    "cuda_visible_devices": device,
                    "effective_config_sha256": lock["effective_config_sha256"],
                    "lock_file": lock_name,
                    "lock_sha256": sha256_bytes(lock_bytes),
                    "run_id": run_id,
                    "seed": seed,
                }
            )

        index = {
            "bundle_schema_version": 1,
            "excluded_from_confirmatory": args.tier == "debug",
            "producer_git_commit": commit,
            "registry_sha256": registry_sha256,
            "run_count": len(records),
            "runs": records,
            "tier": args.tier,
        }
        index_bytes = canonical_json_bytes(index)
        (stage / "index.json").write_bytes(index_bytes)
        (stage / "index.json.sha256").write_text(
            sha256_bytes(index_bytes) + "  index.json\n", encoding="ascii"
        )
        stage.rename(args.output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise

    print(
        f"[LOCK_BUNDLE] {args.output} sha256={sha256_bytes(index_bytes)}",
        flush=True,
    )


def validate_lock_bundle(bundle: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    index_path = bundle / "index.json"
    index = load_json(index_path)
    expected_line = (bundle / "index.json.sha256").read_text(encoding="ascii").strip()
    expected_hash = expected_line.split()[0]
    if sha256_file(index_path) != expected_hash:
        raise RuntimeError("Lock index checksum mismatch.")
    runs = index.get("runs")
    if not isinstance(runs, list) or len(runs) != index.get("run_count"):
        raise RuntimeError("Lock index run count is inconsistent.")
    for record in runs:
        if not isinstance(record, dict):
            raise RuntimeError("Malformed lock index record.")
        lock_path = bundle / str(record["lock_file"])
        if sha256_file(lock_path) != record["lock_sha256"]:
            raise RuntimeError(f"Lock checksum mismatch: {lock_path.name}.")
    return index, runs


def execute_one_debug(
    *,
    record: dict[str, Any],
    index: dict[str, Any],
    matrix: dict[str, Any],
    cells_by_name: dict[str, list[str]],
    par: Path,
    code_root: Path,
    evidence_root: Path,
) -> dict[str, Any]:
    run_id = str(record["run_id"])
    device = str(record["cuda_visible_devices"])
    command = run_command(
        par=par,
        code_root=code_root,
        evidence_root=evidence_root,
        matrix=matrix,
        tier="debug",
        cell=str(record["cell"]),
        seed=int(record["seed"]),
        layers=cells_by_name[str(record["cell"])],
        expected_commit=str(index["producer_git_commit"]),
        effective_config_sha256=str(record["effective_config_sha256"]),
    )
    log_dir = evidence_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{run_id}.log"
    if log_path.exists():
        raise RuntimeError(f"Refusing to overwrite debug log {log_path}.")
    environment = os.environ.copy()
    environment["CUDA_VISIBLE_DEVICES"] = device
    environment["PYTHONUNBUFFERED"] = "1"
    print(f"[RUN] {run_id} CUDA_VISIBLE_DEVICES={device}", flush=True)
    with log_path.open("xb") as log_handle:
        completed = subprocess.run(
            command,
            cwd=code_root,
            env=environment,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
        )
        log_handle.flush()
        os.fsync(log_handle.fileno())
    if completed.returncode != 0:
        raise RuntimeError(f"Debug run failed for {run_id}; see {log_path}.")
    artifact_dir = evidence_root / "evaluations" / run_id / "env_steps_000000000080"
    checkpoint_dir = evidence_root / "checkpoints" / run_id
    if not artifact_dir.is_dir():
        raise RuntimeError(f"Debug evaluation artifact is missing for {run_id}.")
    checkpoints = sorted(path for path in checkpoint_dir.iterdir() if path.is_file())
    if not checkpoints:
        raise RuntimeError(f"Debug checkpoint is missing for {run_id}.")
    artifact_files = sorted(path for path in artifact_dir.iterdir() if path.is_file())
    return {
        "artifact_files": {
            path.name: sha256_file(path) for path in artifact_files
        },
        "cell": record["cell"],
        "checkpoint_files": {
            path.name: sha256_file(path) for path in checkpoints
        },
        "environment_interactions": 80,
        "excluded_from_confirmatory": True,
        "log_file": log_path.name,
        "log_sha256": sha256_file(log_path),
        "run_id": run_id,
        "seed": record["seed"],
    }


def execute_debug(args: argparse.Namespace) -> None:
    bundle = args.lock_bundle.resolve()
    index, records = validate_lock_bundle(bundle)
    if index.get("tier") != "debug" or not index.get("excluded_from_confirmatory"):
        raise RuntimeError("Only debug-only lock bundles may be executed by this command.")
    code_root = args.code_root.resolve()
    par = args.par.resolve()
    evidence_root = args.evidence_root.resolve()
    matrix_path = code_root / "configs" / "iclr_confirmatory" / "run_matrix.json"
    matrix = load_json(matrix_path)
    if matrix.get("status") != "registered_not_authorized":
        raise RuntimeError("Debug execution expects the unauthorized registration state.")
    if producer_commit(code_root) != index.get("producer_git_commit"):
        raise RuntimeError("Producer commit differs from the lock bundle.")
    if sha256_file(matrix_path) != index.get("registry_sha256"):
        raise RuntimeError("Run matrix differs from the lock bundle.")
    cells_by_name = matrix_cells(matrix)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault(str(record["cuda_visible_devices"]), []).append(record)

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=len(grouped)) as executor:
        futures = []
        for device_records in grouped.values():
            def run_device_queue(
                queue: list[dict[str, Any]] = device_records,
            ) -> list[dict[str, Any]]:
                return [
                    execute_one_debug(
                        record=record,
                        index=index,
                        matrix=matrix,
                        cells_by_name=cells_by_name,
                        par=par,
                        code_root=code_root,
                        evidence_root=evidence_root,
                    )
                    for record in queue
                ]

            futures.append(executor.submit(run_device_queue))
        for future in as_completed(futures):
            results.extend(future.result())

    results.sort(key=lambda value: str(value["run_id"]))
    execution = {
        "execution_schema_version": 1,
        "excluded_from_confirmatory": True,
        "lock_index_sha256": sha256_file(bundle / "index.json"),
        "producer_git_commit": index["producer_git_commit"],
        "registry_sha256": index["registry_sha256"],
        "run_count": len(results),
        "runs": results,
        "tier": "debug",
    }
    output_path = evidence_root / "debug_execution_index.json"
    if output_path.exists():
        raise RuntimeError(f"Refusing to overwrite {output_path}.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(canonical_json_bytes(execution))
    print(
        f"[DEBUG_EXECUTION] {output_path} sha256={sha256_file(output_path)}",
        flush=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare-locks")
    prepare.add_argument("--code-root", type=Path, required=True)
    prepare.add_argument("--par", type=Path, required=True)
    prepare.add_argument("--evidence-root", type=Path, required=True)
    prepare.add_argument("--output", type=Path, required=True)
    prepare.add_argument("--tier", choices=("confirmatory", "debug"), required=True)
    prepare.add_argument("--cells", nargs="+")
    prepare.add_argument("--seeds", nargs="+", type=int)
    prepare.add_argument("--cuda-visible-devices", nargs="+", default=["0"])
    prepare.set_defaults(handler=prepare_locks)

    execute = subparsers.add_parser("execute-debug")
    execute.add_argument("--code-root", type=Path, required=True)
    execute.add_argument("--par", type=Path, required=True)
    execute.add_argument("--evidence-root", type=Path, required=True)
    execute.add_argument("--lock-bundle", type=Path, required=True)
    execute.set_defaults(handler=execute_debug)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
