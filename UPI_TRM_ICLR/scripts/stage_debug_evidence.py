#!/usr/bin/env python3
"""Validate and stage anonymous debug-only evaluation evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any


ARTIFACT_NAMES = (
    "compute_snapshot.json",
    "evaluation_metadata.json",
    "per_instance.jsonl",
    "summary.json",
)


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


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


def require_equal(actual: Any, expected: Any, field: str, run_id: str) -> None:
    if actual != expected:
        raise RuntimeError(
            f"{field} mismatch for {run_id}: {actual!r} != {expected!r}."
        )


def validate_lock_bundle(bundle: Path) -> dict[str, Any]:
    index_path = bundle / "index.json"
    index = load_json(index_path)
    checksum = (bundle / "index.json.sha256").read_text(encoding="ascii").split()[0]
    require_equal(sha256_file(index_path), checksum, "lock index hash", "bundle")
    if index.get("tier") != "debug" or not index.get("excluded_from_confirmatory"):
        raise RuntimeError("Expected a debug-only lock bundle.")
    return index


def validate_and_copy_run(
    *,
    evidence_root: Path,
    stage: Path,
    execution_record: dict[str, Any],
    lock_record: dict[str, Any],
    producer_commit: str,
) -> dict[str, Any]:
    run_id = str(execution_record["run_id"])
    require_equal(lock_record["run_id"], run_id, "lock run ID", run_id)
    require_equal(execution_record["seed"], lock_record["seed"], "seed", run_id)
    require_equal(execution_record["cell"], lock_record["cell"], "cell", run_id)
    require_equal(
        execution_record["environment_interactions"],
        80,
        "training interactions",
        run_id,
    )
    if not execution_record.get("excluded_from_confirmatory"):
        raise RuntimeError(f"Run {run_id} is not marked debug-only.")

    artifact_source = (
        evidence_root
        / "evaluations"
        / run_id
        / "env_steps_000000000080"
    )
    if not artifact_source.is_dir():
        raise RuntimeError(f"Evaluation artifact directory is missing for {run_id}.")
    observed_names = sorted(path.name for path in artifact_source.iterdir())
    require_equal(observed_names, sorted(ARTIFACT_NAMES), "artifact inventory", run_id)
    expected_hashes = execution_record["artifact_files"]
    if sorted(expected_hashes) != sorted(ARTIFACT_NAMES):
        raise RuntimeError(f"Recorded artifact inventory is malformed for {run_id}.")
    for name in ARTIFACT_NAMES:
        require_equal(
            sha256_file(artifact_source / name),
            expected_hashes[name],
            f"{name} hash",
            run_id,
        )

    metadata = load_json(artifact_source / "evaluation_metadata.json")
    summary = load_json(artifact_source / "summary.json")
    compute = load_json(artifact_source / "compute_snapshot.json")
    require_equal(metadata["run_id"], run_id, "metadata run ID", run_id)
    require_equal(
        metadata["producer_git_commit"],
        producer_commit,
        "producer commit",
        run_id,
    )
    require_equal(
        metadata["effective_config_sha256"],
        lock_record["effective_config_sha256"],
        "effective config hash",
        run_id,
    )
    require_equal(metadata["checkpoint_environment_steps"], 80, "checkpoint", run_id)
    require_equal(metadata["dataset"]["split"], "validation", "split", run_id)
    require_equal(metadata["dataset"]["record_count"], 256, "record count", run_id)
    require_equal(summary["record_count"], 256, "summary record count", run_id)
    require_equal(
        summary["total_environment_interactions"],
        4096,
        "evaluation interactions",
        run_id,
    )
    require_equal(
        compute["progress"]["environment_interactions"],
        80,
        "compute interactions",
        run_id,
    )

    rows: list[dict[str, Any]] = []
    with (artifact_source / "per_instance.jsonl").open("r", encoding="ascii") as handle:
        for line in handle:
            row = json.loads(line)
            if not isinstance(row, dict):
                raise RuntimeError(f"Malformed per-instance row for {run_id}.")
            rows.append(row)
    require_equal(len(rows), 256, "per-instance row count", run_id)
    require_equal(
        [row["record_index"] for row in rows],
        list(range(256)),
        "record indices",
        run_id,
    )
    hashes = [row["record_sha256"] for row in rows]
    require_equal(len(set(hashes)), 256, "unique record count", run_id)
    require_equal(
        sum(int(bool(row["success"])) for row in rows),
        summary["solved_count"],
        "solved count",
        run_id,
    )

    checkpoint_root = evidence_root / "checkpoints" / run_id
    for name, expected_hash in execution_record["checkpoint_files"].items():
        require_equal(
            sha256_file(checkpoint_root / name),
            expected_hash,
            f"checkpoint {name} hash",
            run_id,
        )
    require_equal(
        metadata["checkpoint_sha256"],
        execution_record["checkpoint_files"]["rl_checkpoint_step_80.pt"],
        "evaluated checkpoint hash",
        run_id,
    )
    log_path = evidence_root / "logs" / execution_record["log_file"]
    require_equal(
        sha256_file(log_path),
        execution_record["log_sha256"],
        "log hash",
        run_id,
    )

    destination = stage / "runs" / run_id / "env_steps_000000000080"
    destination.mkdir(parents=True)
    for name in ARTIFACT_NAMES:
        shutil.copyfile(artifact_source / name, destination / name)
    return {
        "artifact_files": dict(expected_hashes),
        "cell": execution_record["cell"],
        "checkpoint_files": dict(execution_record["checkpoint_files"]),
        "effective_config_sha256": lock_record["effective_config_sha256"],
        "environment_interactions": 80,
        "evaluation_record_count": 256,
        "excluded_from_confirmatory": True,
        "log_sha256": execution_record["log_sha256"],
        "policy_mode": metadata["policy_mode"],
        "run_id": run_id,
        "seed": execution_record["seed"],
        "summary": summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--lock-bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    evidence_root = args.evidence_root.resolve()
    lock_bundle = args.lock_bundle.resolve()
    output = args.output.resolve()
    if output.exists():
        raise RuntimeError(f"Refusing to overwrite {output}.")
    lock_index = validate_lock_bundle(lock_bundle)
    execution_path = evidence_root / "debug_execution_index.json"
    execution = load_json(execution_path)
    require_equal(execution["tier"], "debug", "execution tier", "bundle")
    if not execution.get("excluded_from_confirmatory"):
        raise RuntimeError("Execution index is not marked debug-only.")
    require_equal(
        execution["lock_index_sha256"],
        sha256_file(lock_bundle / "index.json"),
        "execution lock hash",
        "bundle",
    )
    require_equal(
        execution["producer_git_commit"],
        lock_index["producer_git_commit"],
        "producer commit",
        "bundle",
    )
    require_equal(
        execution["registry_sha256"],
        lock_index["registry_sha256"],
        "registry hash",
        "bundle",
    )
    lock_by_run = {record["run_id"]: record for record in lock_index["runs"]}
    execution_runs = execution["runs"]
    require_equal(len(execution_runs), 8, "execution count", "bundle")
    require_equal(
        sorted(lock_by_run),
        sorted(record["run_id"] for record in execution_runs),
        "run inventory",
        "bundle",
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}.stage.", dir=output.parent))
    try:
        records = [
            validate_and_copy_run(
                evidence_root=evidence_root,
                stage=stage,
                execution_record=record,
                lock_record=lock_by_run[record["run_id"]],
                producer_commit=execution["producer_git_commit"],
            )
            for record in execution_runs
        ]
        records.sort(key=lambda record: record["run_id"])
        manifest = {
            "artifact_schema_version": 1,
            "description": "Debug-only pipeline smoke evidence; not confirmatory evidence.",
            "excluded_from_confirmatory": True,
            "external_execution_index_sha256": sha256_file(execution_path),
            "lock_index_sha256": execution["lock_index_sha256"],
            "producer_git_commit": execution["producer_git_commit"],
            "registry_sha256": execution["registry_sha256"],
            "run_count": len(records),
            "runs": records,
            "tier": "debug",
        }
        manifest_bytes = canonical_json_bytes(manifest)
        (stage / "MANIFEST.json").write_bytes(manifest_bytes)
        (stage / "MANIFEST.json.sha256").write_text(
            hashlib.sha256(manifest_bytes).hexdigest() + "  MANIFEST.json\n",
            encoding="ascii",
        )
        for path in stage.rglob("*"):
            if not path.is_file():
                continue
            contents = path.read_bytes()
            if b"/home/" in contents or b"buiksat" in contents:
                raise RuntimeError(f"Identity-bearing path survived staging in {path}.")
        stage.rename(output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    print(f"Staged debug evidence: {output}")
    print(f"Manifest SHA-256: {sha256_file(output / 'MANIFEST.json')}")


if __name__ == "__main__":
    main()
