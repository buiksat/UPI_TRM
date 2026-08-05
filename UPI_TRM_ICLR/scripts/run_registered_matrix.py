#!/usr/bin/env python3
"""Prepare immutable run locks and execute registered experiment runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Sequence


LOCK_PREFIX = "[CONFIRMATORY_LOCK] "


def validate_attempt_index(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RuntimeError("Attempt index must be a non-negative integer.")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def canonical_json_value_sha256(value: Any) -> str:
    try:
        encoded = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Hash-linked value is not canonical JSON.") from exc
    return sha256_bytes(encoded)


def is_lower_hex(value: object, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def normalize_cuda_device(value: object) -> str:
    """Return one canonical CUDA device identifier or fail closed."""

    if not isinstance(value, str) or not value:
        raise RuntimeError("CUDA binding must name exactly one device.")
    if value.isascii() and value.isdecimal():
        normalized = str(int(value, 10))
        if value != normalized:
            raise RuntimeError(f"CUDA binding is a noncanonical alias: {value!r}.")
        return normalized
    match = re.fullmatch(
        r"GPU-([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        value,
    )
    if match is None:
        raise RuntimeError(
            "CUDA binding must be one canonical non-negative ordinal or GPU UUID."
        )
    normalized = f"GPU-{match.group(1).lower()}"
    if value != normalized:
        raise RuntimeError(f"CUDA binding is a noncanonical alias: {value!r}.")
    return normalized


def normalize_cuda_devices(values: Sequence[object]) -> list[str]:
    devices = [normalize_cuda_device(value) for value in values]
    if not devices:
        raise RuntimeError("CUDA device list must be nonempty.")
    if len(devices) != len(set(devices)):
        raise RuntimeError("CUDA device list contains overlapping bindings.")
    namespaces = {
        "uuid" if device.startswith("GPU-") else "ordinal" for device in devices
    }
    if len(namespaces) != 1:
        raise RuntimeError(
            "CUDA bindings must use one identifier namespace so overlap is decidable."
        )
    return devices


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


def registered_run_id(matrix: dict[str, Any], tier: str, cell: str, seed: int) -> str:
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
    attempt_index: int,
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
        "--attempt-index",
        str(validate_attempt_index(attempt_index)),
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
        command.extend(["--expected-effective-config-sha256", effective_config_sha256])
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
    devices = normalize_cuda_devices(args.cuda_visible_devices)
    attempt_index = validate_attempt_index(args.attempt_index)
    if args.tier == "confirmatory" and (
        set(cells) != set(cells_by_name) or set(seeds) != set(spec["seeds"])
    ):
        raise RuntimeError(
            "Confirmatory lock preparation requires the complete registered "
            "cell-by-seed product."
        )
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
    stage = Path(
        tempfile.mkdtemp(prefix=f".{args.output.name}.stage.", dir=args.output.parent)
    )
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
                attempt_index=attempt_index,
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
                "attempt_index": attempt_index,
                "producer_git_commit": commit,
                "registry_sha256": registry_sha256,
                "lock_schema_version": 3,
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
                runtime_environment = runtime_fingerprint["determinism_environment"]
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
                    "attempt_index": attempt_index,
                    "lock_file": lock_name,
                    "lock_sha256": sha256_bytes(lock_bytes),
                    "run_id": run_id,
                    "seed": seed,
                }
            )

        index = {
            "bundle_schema_version": 2,
            "attempt_index": attempt_index,
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
    checksum_fields = expected_line.split()
    if len(checksum_fields) != 2 or checksum_fields[1] != "index.json":
        raise RuntimeError("Lock index checksum file is malformed.")
    expected_hash = checksum_fields[0]
    if not is_lower_hex(expected_hash, 64):
        raise RuntimeError("Lock index checksum is malformed.")
    if sha256_file(index_path) != expected_hash:
        raise RuntimeError("Lock index checksum mismatch.")
    runs = index.get("runs")
    attempt_index = validate_attempt_index(index.get("attempt_index"))
    if not isinstance(runs, list) or len(runs) != index.get("run_count"):
        raise RuntimeError("Lock index run count is inconsistent.")
    for record in runs:
        if not isinstance(record, dict):
            raise RuntimeError("Malformed lock index record.")
        if validate_attempt_index(record.get("attempt_index")) != attempt_index:
            raise RuntimeError("Lock record attempt differs from its bundle.")
        lock_file = record.get("lock_file")
        if not isinstance(lock_file, str) or Path(lock_file).name != lock_file:
            raise RuntimeError("Lock index contains an unsafe lock filename.")
        lock_sha256 = record.get("lock_sha256")
        if not is_lower_hex(lock_sha256, 64):
            raise RuntimeError("Lock index contains a malformed lock checksum.")
        lock_path = bundle / lock_file
        if sha256_file(lock_path) != lock_sha256:
            raise RuntimeError(f"Lock checksum mismatch: {lock_path.name}.")
    return index, runs


def _scheduled_milestones(matrix: dict[str, Any], field: str) -> list[int]:
    budget = int(matrix["environment_interactions"])
    if budget <= 0:
        raise RuntimeError("Confirmatory interaction budget must be positive.")
    interval = int(matrix[field])
    if interval <= 0 or budget % interval != 0:
        raise RuntimeError(
            f"Registered {field} must be positive and divide the budget."
        )
    return list(range(interval, budget + 1, interval))


def expected_milestone_schedules(
    matrix: dict[str, Any],
) -> tuple[list[int], list[int]]:
    """Return independent checkpoint and evaluation schedules."""

    save_milestones = _scheduled_milestones(matrix, "save_environment_interval")
    evaluation_milestones = _scheduled_milestones(
        matrix, "evaluation_environment_interval"
    )
    if not set(evaluation_milestones).issubset(save_milestones):
        raise RuntimeError(
            "Every registered evaluation milestone must also save a checkpoint."
        )
    reported = matrix.get("reported_environment_checkpoints")
    if not isinstance(reported, list) or not all(
        isinstance(value, int) and not isinstance(value, bool) for value in reported
    ):
        raise RuntimeError("Registered reporting checkpoints are malformed.")
    if (
        len(reported) != len(set(reported))
        or not set(reported).issubset(evaluation_milestones)
        or int(matrix["environment_interactions"]) not in reported
    ):
        raise RuntimeError(
            "Reporting checkpoints must be distinct evaluation milestones and include "
            "the budget."
        )
    return save_milestones, evaluation_milestones


def validate_confirmatory_bundle(
    *,
    bundle: Path,
    index: dict[str, Any],
    records: list[dict[str, Any]],
    matrix: dict[str, Any],
) -> None:
    """Bind every confirmatory lock record to its live registration."""

    if index.get("tier") != "confirmatory":
        raise RuntimeError(
            "Confirmatory execution requires a confirmatory lock bundle."
        )
    if index.get("excluded_from_confirmatory") is not False:
        raise RuntimeError(
            "Confirmatory lock bundle must not be excluded from analysis."
        )
    if matrix.get("status") != "authorized":
        raise RuntimeError(
            "Confirmatory execution requires matrix status exactly authorized."
        )
    if index.get("bundle_schema_version") != 2 or not records:
        raise RuntimeError("Confirmatory lock bundle schema or run set is invalid.")
    if not is_lower_hex(index.get("producer_git_commit"), 40):
        raise RuntimeError("Lock bundle producer commit is malformed.")
    if not is_lower_hex(index.get("registry_sha256"), 64):
        raise RuntimeError("Lock bundle registry hash is malformed.")

    cells_by_name = matrix_cells(matrix)
    registered_seeds = matrix.get("confirmatory_seeds")
    if (
        not isinstance(registered_seeds, list)
        or not registered_seeds
        or not all(
            isinstance(seed, int) and not isinstance(seed, bool)
            for seed in registered_seeds
        )
        or len(registered_seeds) != len(set(registered_seeds))
    ):
        raise RuntimeError("Confirmatory seed registration is malformed.")
    expected_assignments = {
        (cell, seed) for cell in cells_by_name for seed in registered_seeds
    }
    seen_assignments: set[tuple[str, int]] = set()
    seen_run_ids: set[str] = set()
    device_namespaces: set[str] = set()
    for record in records:
        cell = record.get("cell")
        seed = record.get("seed")
        run_id = record.get("run_id")
        device = record.get("cuda_visible_devices")
        if cell not in cells_by_name or seed not in registered_seeds:
            raise RuntimeError(f"Unregistered confirmatory assignment: {cell}/{seed}.")
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise RuntimeError("Confirmatory lock seed must be an integer.")
        expected_run_id = registered_run_id(matrix, "confirmatory", cell, seed)
        if run_id != expected_run_id:
            raise RuntimeError(
                f"Lock run identifier {run_id!r} does not match {expected_run_id!r}."
            )
        assignment = (cell, seed)
        if assignment in seen_assignments or run_id in seen_run_ids:
            raise RuntimeError(f"Duplicate confirmatory lock assignment: {run_id}.")
        seen_assignments.add(assignment)
        seen_run_ids.add(str(run_id))
        normalized_device = normalize_cuda_device(device)
        if normalized_device != device:
            raise RuntimeError(f"Invalid CUDA binding for {run_id}.")
        device_namespaces.add(
            "uuid" if normalized_device.startswith("GPU-") else "ordinal"
        )
        expected_layers = cells_by_name[cell]
        if record.get("config_layers") != expected_layers:
            raise RuntimeError(f"Config layers differ from registration for {run_id}.")

        lock_name = record.get("lock_file")
        if (
            not isinstance(lock_name, str)
            or Path(lock_name).name != lock_name
            or lock_name != f"{run_id}.lock.json"
        ):
            raise RuntimeError(f"Unsafe lock filename for {run_id}.")
        lock = load_json(bundle / lock_name)
        expected_lock_fields = {
            "attempt_index": validate_attempt_index(index.get("attempt_index")),
            "confirmatory_cell": cell,
            "confirmatory_tier": "confirmatory",
            "effective_config_sha256": record.get("effective_config_sha256"),
            "lock_schema_version": 3,
            "producer_git_commit": index.get("producer_git_commit"),
            "registry_sha256": index.get("registry_sha256"),
            "run_id": run_id,
            "training_seed": seed,
        }
        for field, expected in expected_lock_fields.items():
            if lock.get(field) != expected:
                raise RuntimeError(
                    f"Lock field {field} differs from its index for {run_id}."
                )
        if validate_attempt_index(record.get("attempt_index")) != (
            expected_lock_fields["attempt_index"]
        ):
            raise RuntimeError(f"Attempt index differs for {run_id}.")
        config_hash = record.get("effective_config_sha256")
        if not is_lower_hex(config_hash, 64):
            raise RuntimeError(f"Effective-config hash is malformed for {run_id}.")
        effective_config = lock.get("effective_config")
        if not isinstance(effective_config, dict):
            raise RuntimeError(f"Effective config is missing from lock for {run_id}.")
        if canonical_json_value_sha256(effective_config) != config_hash:
            raise RuntimeError(f"Effective config hash is wrong for {run_id}.")

    if seen_assignments != expected_assignments:
        missing = sorted(expected_assignments - seen_assignments)
        extra = sorted(seen_assignments - expected_assignments)
        raise RuntimeError(
            "Confirmatory lock bundle must contain the complete registered "
            f"cell-by-seed product; missing={missing}, extra={extra}."
        )
    if len(device_namespaces) != 1:
        raise RuntimeError(
            "CUDA bindings must use one identifier namespace so overlap is decidable."
        )
    expected_milestone_schedules(matrix)


def _jsonl_record_count(path: Path) -> int:
    count = 0
    with path.open("r", encoding="ascii") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                raise RuntimeError(f"Blank JSONL row in {path} at line {line_number}.")
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Malformed JSONL row in {path} at line {line_number}."
                ) from exc
            count += 1
    return count


def _regular_files(directory: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(directory.iterdir()):
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"Unexpected non-regular evidence entry: {path}.")
        files.append(path)
    return files


def collect_confirmatory_artifacts(
    *,
    record: dict[str, Any],
    index: dict[str, Any],
    matrix: dict[str, Any],
    evidence_root: Path,
    log_path: Path,
) -> dict[str, Any]:
    """Validate and hash every scheduled artifact for one completed run."""

    run_id = str(record["run_id"])
    seed = int(record["seed"])
    attempt_index = validate_attempt_index(record.get("attempt_index"))
    attempt_name = f"attempt_{attempt_index:04d}"
    checkpoint_dir = evidence_root / "checkpoints" / run_id / attempt_name
    evaluation_dir = evidence_root / "evaluations" / run_id / attempt_name
    if not checkpoint_dir.is_dir() or not evaluation_dir.is_dir():
        raise RuntimeError(f"Attempt artifact roots are missing for {run_id}.")

    required_artifact_names = {
        "compute_snapshot.json",
        "evaluation_metadata.json",
        "per_instance.jsonl",
        "summary.json",
    }
    eval_count = int(matrix["dataset"]["test_count"])
    eval_manifest = str(matrix["dataset"]["test_manifest_sha256"])
    effective_config_sha256 = str(record["effective_config_sha256"])
    checkpoints: dict[str, str] = {}
    evaluations: list[dict[str, Any]] = []
    save_milestones, evaluation_milestones = expected_milestone_schedules(matrix)
    expected_evaluation_dirs = {
        f"env_steps_{milestone:012d}" for milestone in evaluation_milestones
    }
    observed_evaluation_dirs = set()
    for path in sorted(evaluation_dir.iterdir()):
        if path.is_symlink() or not path.is_dir():
            raise RuntimeError(f"Unexpected evaluation evidence entry: {path}.")
        observed_evaluation_dirs.add(path.name)
    if observed_evaluation_dirs != expected_evaluation_dirs:
        raise RuntimeError(
            f"Evaluation milestone inventory is wrong for {run_id}: "
            f"observed={sorted(observed_evaluation_dirs)}."
        )

    for milestone in save_milestones:
        checkpoint_path = checkpoint_dir / f"rl_checkpoint_step_{milestone}.pt"
        if not checkpoint_path.is_file():
            raise RuntimeError(
                f"Registered checkpoint {milestone} is missing for {run_id}."
            )
        checkpoint_sha256 = sha256_file(checkpoint_path)
        checkpoints[checkpoint_path.name] = checkpoint_sha256

    for milestone in evaluation_milestones:
        checkpoint_path = checkpoint_dir / f"rl_checkpoint_step_{milestone}.pt"
        checkpoint_sha256 = checkpoints[checkpoint_path.name]
        artifact_dir = evaluation_dir / f"env_steps_{milestone:012d}"
        if not artifact_dir.is_dir():
            raise RuntimeError(
                f"Registered evaluation {milestone} is missing for {run_id}."
            )
        artifact_files = _regular_files(artifact_dir)
        artifact_names = {path.name for path in artifact_files}
        missing = sorted(required_artifact_names - artifact_names)
        if missing:
            raise RuntimeError(
                f"Evaluation {milestone} for {run_id} is missing {missing}."
            )
        metadata = load_json(artifact_dir / "evaluation_metadata.json")
        summary = load_json(artifact_dir / "summary.json")
        compute = load_json(artifact_dir / "compute_snapshot.json")
        dataset = metadata.get("dataset")
        expected_metadata = {
            "checkpoint_environment_steps": milestone,
            "checkpoint_sha256": checkpoint_sha256,
            "effective_config_sha256": effective_config_sha256,
            "producer_git_commit": index["producer_git_commit"],
            "run_id": run_id,
            "training_seed": seed,
        }
        for field, expected in expected_metadata.items():
            if metadata.get(field) != expected:
                raise RuntimeError(
                    f"Evaluation metadata field {field} is wrong for "
                    f"{run_id} at {milestone}."
                )
        if (
            not isinstance(dataset, dict)
            or dataset.get("split") != matrix["dataset"]["test_split"]
        ):
            raise RuntimeError(
                f"Evaluation split is wrong for {run_id} at {milestone}."
            )
        if (
            dataset.get("manifest_sha256") != eval_manifest
            or dataset.get("record_count") != eval_count
        ):
            raise RuntimeError(
                f"Evaluation dataset binding is wrong for {run_id} at {milestone}."
            )
        progress = compute.get("progress")
        if (
            not isinstance(progress, dict)
            or progress.get("environment_interactions") != milestone
        ):
            raise RuntimeError(
                f"Compute interaction counter is wrong for {run_id} at {milestone}."
            )
        if summary.get("record_count") != eval_count:
            raise RuntimeError(
                f"Evaluation record count is wrong for {run_id} at {milestone}."
            )
        per_instance = artifact_dir / "per_instance.jsonl"
        if _jsonl_record_count(per_instance) != eval_count:
            raise RuntimeError(
                f"Per-instance row count is wrong for {run_id} at {milestone}."
            )
        linked_hashes = {
            "compute_snapshot_sha256": sha256_file(
                artifact_dir / "compute_snapshot.json"
            ),
            "metadata_sha256": sha256_file(artifact_dir / "evaluation_metadata.json"),
            "per_instance_sha256": sha256_file(per_instance),
        }
        for field, expected in linked_hashes.items():
            if summary.get(field) != expected:
                raise RuntimeError(
                    f"Summary hash {field} is wrong for {run_id} at {milestone}."
                )
        evaluations.append(
            {
                "artifact_files": {
                    path.name: sha256_file(path) for path in artifact_files
                },
                "checkpoint_environment_steps": milestone,
                "checkpoint_outer_steps": metadata.get("checkpoint_outer_steps"),
                "evaluation_record_count": summary["record_count"],
                "evaluation_total_environment_interactions": summary.get(
                    "total_environment_interactions"
                ),
                "progress_counters": progress,
            }
        )

    for path in _regular_files(checkpoint_dir):
        if path.name not in checkpoints:
            checkpoints[path.name] = sha256_file(path)
    return {
        "attempt_index": attempt_index,
        "cell": record["cell"],
        "checkpoint_files": checkpoints,
        "cuda_visible_devices": record["cuda_visible_devices"],
        "effective_config_sha256": effective_config_sha256,
        "environment_interactions": int(matrix["environment_interactions"]),
        "evaluations": evaluations,
        "excluded_from_confirmatory": False,
        "log_file": log_path.relative_to(evidence_root / "logs").as_posix(),
        "log_sha256": sha256_file(log_path),
        "run_id": run_id,
        "seed": seed,
    }


def execute_one_confirmatory(
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
    attempt_index = validate_attempt_index(record.get("attempt_index"))
    command = run_command(
        par=par,
        code_root=code_root,
        evidence_root=evidence_root,
        matrix=matrix,
        tier="confirmatory",
        cell=str(record["cell"]),
        seed=int(record["seed"]),
        layers=cells_by_name[str(record["cell"])],
        attempt_index=attempt_index,
        expected_commit=str(index["producer_git_commit"]),
        effective_config_sha256=str(record["effective_config_sha256"]),
    )
    attempt_name = f"attempt_{attempt_index:04d}"
    log_path = evidence_root / "logs" / run_id / attempt_name / "run.log"
    checkpoint_path = evidence_root / "checkpoints" / run_id / attempt_name
    evaluation_path = evidence_root / "evaluations" / run_id / attempt_name
    for path in (log_path, checkpoint_path, evaluation_path):
        if path.exists():
            raise RuntimeError(f"Refusing to overwrite confirmatory evidence {path}.")
    log_path.parent.mkdir(parents=True, exist_ok=False)
    environment = os.environ.copy()
    environment["CUDA_VISIBLE_DEVICES"] = device
    environment["PYTHONUNBUFFERED"] = "1"
    print(f"[CONFIRMATORY_RUN] {run_id} CUDA_VISIBLE_DEVICES={device}", flush=True)
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
        raise RuntimeError(
            f"Confirmatory run failed for {run_id}; retained log: {log_path}."
        )
    return collect_confirmatory_artifacts(
        record=record,
        index=index,
        matrix=matrix,
        evidence_root=evidence_root,
        log_path=log_path,
    )


def _fsync_directory(directory: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(directory, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_bytes_no_replace(output_path: Path, output_bytes: bytes) -> None:
    """Durably publish bytes without ever replacing an existing path."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staged_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.stage.", dir=output_path.parent
    )
    staged_output = Path(staged_name)
    published = False
    try:
        with os.fdopen(descriptor, "wb") as output_handle:
            output_handle.write(output_bytes)
            output_handle.flush()
            os.fsync(output_handle.fileno())
        try:
            os.link(staged_output, output_path, follow_symlinks=False)
        except FileExistsError as exc:
            raise RuntimeError(f"Refusing to overwrite {output_path}.") from exc
        published = True
        _fsync_directory(output_path.parent)
    finally:
        staged_output.unlink(missing_ok=True)
        if published:
            _fsync_directory(output_path.parent)


def execute_confirmatory(args: argparse.Namespace) -> None:
    bundle = args.lock_bundle.resolve()
    index, records = validate_lock_bundle(bundle)
    code_root = args.code_root.resolve()
    par = args.par.resolve()
    evidence_root = args.evidence_root.resolve()
    matrix_path = code_root / "configs" / "iclr_confirmatory" / "run_matrix.json"
    matrix = load_json(matrix_path)
    validate_confirmatory_bundle(
        bundle=bundle,
        index=index,
        records=records,
        matrix=matrix,
    )
    if not par.is_file() or not os.access(par, os.X_OK):
        raise RuntimeError(f"PAR is missing or not executable: {par}.")
    if producer_commit(code_root) != index.get("producer_git_commit"):
        raise RuntimeError("Producer commit differs from the lock bundle.")
    if sha256_file(matrix_path) != index.get("registry_sha256"):
        raise RuntimeError("Run matrix differs from the lock bundle.")

    attempt_index = validate_attempt_index(index.get("attempt_index"))
    output_path = evidence_root / (
        f"confirmatory_execution_attempt_{attempt_index:04d}_index.json"
    )
    if output_path.exists():
        raise RuntimeError(f"Refusing to overwrite {output_path}.")
    for record in records:
        run_id = str(record["run_id"])
        attempt_name = f"attempt_{attempt_index:04d}"
        prospective_paths = (
            evidence_root / "logs" / run_id / attempt_name,
            evidence_root / "checkpoints" / run_id / attempt_name,
            evidence_root / "evaluations" / run_id / attempt_name,
        )
        existing = [path for path in prospective_paths if path.exists()]
        if existing:
            raise RuntimeError(
                f"Refusing to start with existing evidence paths for {run_id}: "
                f"{existing}."
            )

    cells_by_name = matrix_cells(matrix)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault(str(record["cuda_visible_devices"]), []).append(record)

    results: list[dict[str, Any]] = []
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=len(grouped)) as executor:
        futures = []
        for device_records in grouped.values():

            def run_device_queue(
                queue: list[dict[str, Any]] = device_records,
            ) -> list[dict[str, Any]]:
                return [
                    execute_one_confirmatory(
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
            try:
                results.extend(future.result())
            except Exception as exc:
                failures.append(str(exc))
    if failures:
        raise RuntimeError(
            "Confirmatory execution failed; no execution index was published. "
            "All existing attempt evidence was retained. Failures:\n"
            + "\n".join(sorted(failures))
        )
    if len(results) != len(records):
        raise RuntimeError("Not every locked confirmatory run produced a result.")

    results.sort(key=lambda value: str(value["run_id"]))
    execution = {
        "attempt_index": attempt_index,
        "execution_schema_version": 3,
        "excluded_from_confirmatory": False,
        "lock_index_sha256": sha256_file(bundle / "index.json"),
        "producer_git_commit": index["producer_git_commit"],
        "registry_sha256": index["registry_sha256"],
        "run_count": len(results),
        "runs": results,
        "tier": "confirmatory",
    }
    output_bytes = canonical_json_bytes(execution)
    publish_bytes_no_replace(output_path, output_bytes)
    print(
        f"[CONFIRMATORY_EXECUTION] {output_path} "
        f"sha256={sha256_bytes(output_bytes)}",
        flush=True,
    )


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
    attempt_index = validate_attempt_index(record.get("attempt_index"))
    command = run_command(
        par=par,
        code_root=code_root,
        evidence_root=evidence_root,
        matrix=matrix,
        tier="debug",
        cell=str(record["cell"]),
        seed=int(record["seed"]),
        layers=cells_by_name[str(record["cell"])],
        attempt_index=attempt_index,
        expected_commit=str(index["producer_git_commit"]),
        effective_config_sha256=str(record["effective_config_sha256"]),
    )
    attempt_name = f"attempt_{attempt_index:04d}"
    log_dir = evidence_root / "logs" / run_id / attempt_name
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "run.log"
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
    artifact_dir = (
        evidence_root / "evaluations" / run_id / attempt_name / "env_steps_000000000080"
    )
    checkpoint_dir = evidence_root / "checkpoints" / run_id / attempt_name
    if not artifact_dir.is_dir():
        raise RuntimeError(f"Debug evaluation artifact is missing for {run_id}.")
    checkpoints = sorted(path for path in checkpoint_dir.iterdir() if path.is_file())
    if not checkpoints:
        raise RuntimeError(f"Debug checkpoint is missing for {run_id}.")
    artifact_files = sorted(path for path in artifact_dir.iterdir() if path.is_file())
    return {
        "artifact_files": {path.name: sha256_file(path) for path in artifact_files},
        "attempt_index": attempt_index,
        "cell": record["cell"],
        "checkpoint_files": {path.name: sha256_file(path) for path in checkpoints},
        "environment_interactions": 80,
        "excluded_from_confirmatory": True,
        "log_file": log_path.relative_to(evidence_root / "logs").as_posix(),
        "log_sha256": sha256_file(log_path),
        "run_id": run_id,
        "seed": record["seed"],
    }


def execute_debug(args: argparse.Namespace) -> None:
    bundle = args.lock_bundle.resolve()
    index, records = validate_lock_bundle(bundle)
    if index.get("tier") != "debug" or not index.get("excluded_from_confirmatory"):
        raise RuntimeError(
            "Only debug-only lock bundles may be executed by this command."
        )
    code_root = args.code_root.resolve()
    par = args.par.resolve()
    evidence_root = args.evidence_root.resolve()
    matrix_path = code_root / "configs" / "iclr_confirmatory" / "run_matrix.json"
    matrix = load_json(matrix_path)
    if matrix.get("status") != "registered_not_authorized":
        raise RuntimeError(
            "Debug execution expects the unauthorized registration state."
        )
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
        "execution_schema_version": 2,
        "attempt_index": validate_attempt_index(index.get("attempt_index")),
        "excluded_from_confirmatory": True,
        "lock_index_sha256": sha256_file(bundle / "index.json"),
        "producer_git_commit": index["producer_git_commit"],
        "registry_sha256": index["registry_sha256"],
        "run_count": len(results),
        "runs": results,
        "tier": "debug",
    }
    output_path = evidence_root / (
        f"debug_execution_attempt_{index['attempt_index']:04d}_index.json"
    )
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
    prepare.add_argument(
        "--attempt-index",
        type=int,
        default=0,
        help=(
            "Execution attempt bound into locks and evidence paths. Use 0 for "
            "the initial run and a new higher value for each documented retry."
        ),
    )
    prepare.set_defaults(handler=prepare_locks)

    execute = subparsers.add_parser("execute-debug")
    execute.add_argument("--code-root", type=Path, required=True)
    execute.add_argument("--par", type=Path, required=True)
    execute.add_argument("--evidence-root", type=Path, required=True)
    execute.add_argument("--lock-bundle", type=Path, required=True)
    execute.set_defaults(handler=execute_debug)

    execute_confirm = subparsers.add_parser("execute-confirmatory")
    execute_confirm.add_argument("--code-root", type=Path, required=True)
    execute_confirm.add_argument("--par", type=Path, required=True)
    execute_confirm.add_argument("--evidence-root", type=Path, required=True)
    execute_confirm.add_argument("--lock-bundle", type=Path, required=True)
    execute_confirm.set_defaults(handler=execute_confirmatory)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
