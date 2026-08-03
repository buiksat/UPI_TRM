# Confirmatory compute estimate

Status: preliminary estimate from retained historical logs. No confirmatory
run has started.

## Available allocation

The current host exposes one NVIDIA GPU with 81,920 MiB total memory. No new
paid cloud allocation is authorized.

## Measured historical anchors

Retained logs show substantial runtime variation by algorithm and depth:

- in-house DQN, 80,000 interactions: about 3 hours 38 minutes for one retained
  seed;
- five-step DQN, 80,000 interactions: about 8 hours 44 minutes for one
  retained seed;
- nominal 20,000-update PPO records: about 9 hours 30 minutes for one retained
  run;
- nominal 20,000-update A2C records: about 3 hours 5 minutes for one retained
  run.

These records do not provide a scientifically comparable throughput benchmark.
They use different interaction semantics, hardware contexts, and algorithms.
They are used only to establish that the full registered matrix cannot finish
promptly on one GPU.

## Lower-bound workload

Before the interaction cell, projection design, diagnostics, and second domain,
the registered Sudoku work contains:

- bridge: 5 primary cells by 10 seeds, or 50 runs;
- matched comparison: 2 methods by 10 seeds, or 20 runs.

At an optimistic 3.5 GPU-hours per run, these 70 runs require at least 245
serial GPU-hours, or 10.2 days. At 9.5 GPU-hours per run, they require 665
serial GPU-hours, or 27.7 days. The interaction cells add up to 40 runs if they
cannot reuse primary bridge cells. The projection training design adds 20
runs. The second domain adds at least 30 runs after its smoke test. Diagnostics
also add inference time.

The full matrix therefore exceeds the available single-host execution window.
Running a subset and calling it confirmatory would violate the registry.

## Execution gate

This revision will:

1. repair and test the code paths;
2. generate and hash the immutable datasets;
3. create exact launch configurations and commands;
4. run debug-only smoke tests with seeds `9001` to `9003` as time permits;
5. measure smoke throughput and replace this preliminary estimate;
6. leave confirmatory statuses as `missing experiment` until every registered
   seed in a comparison is complete.

Any request to run the full matrix needs either a multi-GPU allocation or an
explicitly accepted multi-week serial schedule. No paper claim will be inferred
from smoke tests.
