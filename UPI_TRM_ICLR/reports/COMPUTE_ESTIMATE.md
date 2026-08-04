# Confirmatory compute estimate

Status: the eight-cell, 80-run Sudoku matrix is registered but not authorized.
No confirmatory run has started. Eight seed-`9001` debug smokes have completed
and are excluded from confirmatory analysis.

## Available allocation

The current host exposes two NVIDIA PG509-210 GPUs, each with 81,920 MiB total
memory. No paid cloud allocation is authorized.

## Registered workload

The authoritative run matrix contains:

- six C1 bridge cells by ten confirmatory seeds: 60 runs;
- two C2 matched cells by ten confirmatory seeds: 20 runs.

The registered total is 80 runs at exactly 80,000 training environment
interactions each. The projection cross-design, persistent diagnostics, and
second domain are not cells in this matrix. Their compute requirements are
`not verifiable from supplied evidence` and are excluded from the totals
below.

## Historical planning range

Retained historical logs suggest 3.5 to 9.5 GPU-hours for one nominal full
run. Those records used different interaction semantics, hardware contexts,
depths, and algorithms, so the range is a planning anchor rather than a
comparable throughput measurement.

Applying that range to all 80 registered runs gives 280 to 760 GPU-hours. At
perfect utilization of both GPUs, this is 140 to 380 wall-clock hours, or 5.8
to 15.8 days. This idealized range excludes queue gaps, failed runs,
validation, artifact checks, and final analysis. Serial execution would take
11.7 to 31.7 days.

## Measured debug timings

The staged debug evidence contains one 80-interaction run for each cell, all
with seed `9001`, followed by evaluation of 256 validation records. Times come
directly from each staged `compute_snapshot.json`.

| Cell | Training seconds | Evaluation seconds | Total seconds | Rough full-schedule GPU-hours |
| --- | ---: | ---: | ---: | ---: |
| `B0_I00` | 1.993 | 38.511 | 40.505 | 0.639 |
| `Bz_I10` | 2.506 | 40.112 | 42.618 | 0.785 |
| `Bd_I01` | 1.819 | 46.480 | 48.299 | 0.609 |
| `Bt` | 1.936 | 44.755 | 46.691 | 0.637 |
| `Bb` | 15.642 | 40.060 | 55.703 | 4.434 |
| `I11` | 2.469 | 77.818 | 80.288 | 0.859 |
| `UPI_TRM` | 18.143 | 44.162 | 62.305 | 5.138 |
| `TRM_PPO` | 3.269 | 40.727 | 43.996 | 0.998 |

The last column is a mechanical projection:

```text
1000 * measured 80-interaction training time
+ 4 checkpoints * 2 * measured 256-record evaluation time
```

The factor 1,000 scales 80 interactions to 80,000. The factor 2 scales 256
validation records to 512 held-out records. Across all cells and ten seeds,
this calculation gives about 141 GPU-hours, or 2.9 days at perfect two-GPU
utilization.

This 141 GPU-hour number is a rough extrapolation, not a runtime forecast. Each
smoke contains only one optimizer update and one seed. It does not measure
long-run allocator behavior, checkpoint I/O, contention between concurrent
runs, analysis, failures, or diagnostics. The exact-baseline cells already
show that cell throughput differs by almost an order of magnitude. Use the
historical 280 to 760 GPU-hour range for scheduling until at least one full
debug-budget timing exists.

Measured CUDA reserved memory was 88 to 104 MiB per smoke process, and process
RSS was approximately 2.37 to 2.42 GiB. These short measurements show no
memory blocker, but they do not justify colocating multiple full runs on one
GPU without a longer contention test.

## Evidence identities

| Artifact | SHA-256 |
| --- | --- |
| Producer commit | `e4c924cc721e9f4f356789eba03a09f6c8ca1913` |
| Run matrix | `d2c064de22b6cb90a569f7b1000c2dd40087a40153a5070b0cdbd12ac0d22b81` |
| Debug lock index | `3b130e9441561f6ade7ffeba19780933f9ce27f5331874117c8952db6e641a5e` |
| Staged debug manifest | `056b98f4163aec9fede0d0b734006055b9f7b4bce2f21ee5edb8e107c73c63ca` |

## Execution gate

Confirmatory execution is blocked while the matrix status remains
`registered_not_authorized`. Before launch, verify both GPUs, the external
evidence root, all per-run locks, free disk space, and deterministic artifact
publication. Then run the complete ten-seed comparison matrix. A partial
subset remains `missing experiment` and cannot support a confirmatory claim.
