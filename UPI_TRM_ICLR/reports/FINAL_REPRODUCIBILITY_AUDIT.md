# Final reproducibility audit

Date: 2026-08-03, America/Los_Angeles

## Scope and decision

This audit covers the current paper evidence tree, implementation commit
`e4c924cc721e9f4f356789eba03a09f6c8ca1913`, the registered debug lock
bundle, the eight staged seed-9001 debug runs, the materialized confirmatory
dataset, and the retained theorem-pipeline outputs.

The retained debug and theorem artifacts are internally consistent and
content-addressed. The package is not release-ready. There is no current
anonymous supplement, no current paper build, and no anonymous implementation
archive. `artifacts/MANIFEST.json` correctly declares `complete=false` and
`anonymous_release_ready=false`.

## Source identity

- The implementation worktree was clean on branch
  `iclr-confirmatory-repair` at
  `e4c924cc721e9f4f356789eba03a09f6c8ca1913`.
- `configs/iclr_confirmatory/producer_source_manifest.json` has SHA-256
  `cde7db24bbc528019670cba82579d470d23390d44835554416c1545a597eec0f`.
  All 78 listed files existed and matched their recorded SHA-256 values.
- `configs/iclr_confirmatory/run_matrix.json` has SHA-256
  `d2c064de22b6cb90a569f7b1000c2dd40087a40153a5070b0cdbd12ac0d22b81`.
  This is the registry hash bound by every debug lock and index.
- The run matrix remains `registered_not_authorized`. It registers ten
  confirmatory seeds, `101` through `110`, and three debug seeds, `9001`
  through `9003`. No confirmatory training run is recorded.
- The paper evidence base is commit
  `c0c6acae8d591acbd99441eb3b17b6d2306df50d` plus uncommitted final audit and
  manuscript changes. The final working `main.tex` SHA-256 is
  `f1f7bb567578dbf1b4a3ab1d7c3db4cfdf3acee8b6e7fb9f818a8239550344e7`.
  A final immutable paper commit did not exist during this audit.

## Structured-file validation

All JSON files in the paper evidence scope, confirmatory code configuration,
materialized dataset metadata, and external debug evidence parsed
successfully. All JSONL files in the paper evidence and external debug scope
parsed line by line. No `NaN` or infinity token was found in those JSON or
JSONL files.

The run registry contains one metadata record, three theorem-unit-test
records, and eight debug-pipeline records. Its metadata correctly reports 11
runs, zero confirmatory training runs, and the
`registered_not_authorized` state.

## Dataset and registration

- The train, validation, and test manifest hashes are respectively
  `8def4f59387c1ab9466d043c40a7fdd3c7c670e2778b8d949295811ae7b6088a`,
  `4644a3b1bb8b6e384896888154c9e56252368c1fc2f32962b089ade95a5bc1f2`,
  and `163a083a9f5744b7cc485663b269b89acc3103d9e1ec64c7e93f78e36fa79d40`.
- Every entry in the dataset `CHECKSUMS.sha256` file passed.
- The split sizes are 1,024 train, 256 validation, and 512 test records.
  Pairwise record-hash and input-hash overlap is zero for all three split
  pairs.
- The staged debug rows contain exactly the ordered 256-record validation
  manifest list. No evaluation record is duplicated or cycled.

## Debug lock bundle

The lock index contains exactly eight schema-2 debug locks for `B0_I00`,
`Bz_I10`, `Bd_I01`, `Bt`, `Bb`, `I11`, `UPI_TRM`, and `TRM_PPO`, all at seed
`9001`. The index, its sidecar, every lock-file hash, every canonical effective
configuration hash, every ordered configuration-layer hash, the producer
commit, and the run-matrix hash agree.

Each lock registers exactly 80 training environment interactions and a
256-record validation evaluation. The bridge and matched-comparison policy
modes in the locks agree with the run registry and staged evaluation metadata.
These runs are marked `excluded_from_confirmatory` at every layer.

Seven locks embed a runtime-fingerprint object whose canonical hash matches
the recorded fingerprint hash. The `UPI_TRM` lock retains only the matching
GPU-0 fingerprint hash; the same fingerprint object is materialized in the
other GPU-0 locks.

## Staged debug evidence

The staged debug manifest has SHA-256
`056b98f4163aec9fede0d0b734006055b9f7b4bce2f21ee5edb8e107c73c63ca`,
and its sidecar matches. The staged `execution_index.json` has SHA-256
`a87adfa399296fd9f1af5903e66ea54cb92042d728364938e89cf732b07ab9ab`
and is byte-identical to the external execution index.

The stage contains 32 evaluation files, four for each of eight runs. Every
staged file is byte-identical to its external source and matches the nested
manifest, execution index, and run-registry hashes.

The eight `per_instance.jsonl` files contain 256 rows each, for 2,048 rows
total. Independent validation checked all 2,048 rows for:

- canonical JSON encoding and exact record order;
- record-local evaluation-seed derivation;
- action bounds, disabled-STOP exclusion, and sequence lengths;
- environment-interaction and budget termination consistency;
- reward sums and undiscounted shaped returns;
- final-plan hashes;
- recomputed Sudoku filled-cell, violation, zero-candidate, and success data;
- summary recomputation and content hashes; and
- compute progress, empty uninstrumented-role lists, and checkpoint identity.

No discrepancy was found. Every run records 4,096 evaluation interactions,
for 32,768 across the eight debug runs. All eight runs solve 0 of 256 records.
They are pipeline smoke tests, not performance evidence.

## External debug bytes

The external evidence root contains all 13 declared checkpoint files and all
eight declared logs. Their hashes agree with the execution index, nested
manifest, and run registry.

- Checkpoints: 13 files, 390,267,885 bytes. All are valid ZIP containers with
  no archive-integrity error.
- Logs: 8 files, 40,303 bytes.

The checkpoint and log bytes are not in the paper artifact tree. Every log
contains absolute `/home/buiksat/...` paths and must be anonymized before
release. This audit checked checkpoint hash and container integrity, not a
`torch.load` and exact-resume cycle for each external checkpoint.

The complete 397-test Buck event log also remains outside the paper tree at
2,046,752 bytes, SHA-256
`37edc90f302cae5505103f8b8d4ccd1f20b9256b7e2d1710baf1a82fa35905f9`.
The retained paper report records 397 passed, zero failed, zero timed out, and
zero build failures, but the raw log is not staged because it contains
workstation and internal build metadata.

## Theorem-pipeline reproduction

Independent reruns used temporary output directories and left no generated
file in the repository.

- The finite-MDP generator reproduced the 101-row CSV, generated TeX table,
  CPI PNG, and value-decomposition PNG byte for byte. Their hashes are
  `52875311ee5d7144ffce5afc2853c746440de5810836c631bc69f8fdb85996d6`,
  `cbad8dd1f651acd0f46ca4fdd6ecc33e0087bcba20b13e99fd4f65c5d7f821dd`,
  `2b2b37d6dd9b956cbf40ec7456ddb2ecf4e7173fc35b04a855d3b2e26ee4e661`,
  and `e2d6e1fcf9be297ca76d114ba4a0fd57bba7aa6f6120010f513d306d778cc26f`.
- The finite-MDP boundary suite passed all seven groups and reproduced the
  retained JSON byte for byte at
  `ee0867af8e24fce5e8b047b08d32fed3225db98c1bb2699e23dd8616dbc9512a`.
- The official 200-case finite-horizon run reproduced its stdout byte for byte
  at `2bcd3fadd5ad7094b397e492b711d524f65c52d7fe6efea6062922e105a0d8e6`
  with 26,686 checks.
- The 2,000-case stress run reproduced its stdout byte for byte at
  `d2d4b47d08cde84536053fb06aa3c4180a2ea239dd7daa60deb3248f1d0d2da4`
  with 261,814 checks.

The finite-MDP registry now distinguishes execution base commit `896af29`
from complete-pipeline commit `77f73e1`, and records the generator and boundary
suite source commits separately. This resolves the earlier single-commit
provenance ambiguity. These runs remain numerical theorem-pipeline unit tests,
not learned-model validation.

## Bundles and anonymity

The current recovery bundle is
`handoff/trm_bellman_iclr-confirmatory-repair_e4c924c_full.bundle`, 91,779,510
bytes, SHA-256
`5a357c0caa118907426da517aa0a7dc8df4f980fbe38ae9f8a13d0a6035e5ed4`.
Its sidecar matches. `git bundle verify` reports complete history and the sole
branch head is the required `e4c924c` commit.

This full Git bundle is a valid recovery artifact, not an anonymous release
artifact. Its history contains author names, personal and corporate email
addresses, and internal hostnames. The older thin bundle ends at `8d79ba7` and
the old 70 MB repository ZIP predates the confirmatory run matrix, producer
manifest, and dataset. Neither old artifact reproduces the current code.

The staged debug tree, lock bundle, source manifest, and run matrix contain no
match for the scanned local-home, user, email, credential, or internal-path
patterns. The complete paper tree does contain absolute protected paths in
historical provenance files and cannot be archived wholesale without staged
anonymization.

The current anonymous-archive attempt failed closed. Its content scan matched
the literal guard string `b'/home/'` in
`tests/test_persistent_checkpoint_diagnostics_unittest.py`,
`tests/test_config_integrity.py`, and
`scripts/persistent_checkpoint_diagnostics.py` after sanitization. This is a
sanitizer false positive, but it is still a release blocker. No archive was
published.

## Paper build

The host has no `pdflatex`, `latexmk`, `tectonic`, `lualatex`, `xelatex`,
`pdfinfo`, `pdffonts`, or `qpdf`. `make pdf` therefore fails before parsing the
manuscript with exit 127. `build/main_iclr_final.pdf` does not exist. The
ignored `main.pdf` predates the current `main.tex` and is not a final build.

Current page count, reference resolution, font status, PDF anonymity, and
rendered-layout inspection are **not verifiable from supplied evidence**. The
recorded pre-repair PDF and log bytes are also absent; their historical build
claims remain **not verifiable from supplied evidence**.

## Open blockers

1. Produce a clean current PDF with an ICLR-compatible TeX toolchain, then
   inspect references, fonts, page count, anonymity, and every rendered table
   and figure.
2. Fix the archive scanner's literal-guard false positive and build an
   identity-free, history-free supplement twice with byte-identical output.
3. Decide whether the debug checkpoints are part of the release. If retained,
   stage all 13 bytes, load-test them, and record anonymous paths and checksums.
   If excluded, keep the paper explicit that the debug smoke cannot be replayed
   from the supplement alone.
4. Stage sanitized producer logs and a sanitized 397-test log, or explicitly
   exclude them from the release manifest. The current logs reveal local and
   internal paths.
5. Add an environment lock matching the actual Buck runtime. The repository
   `requirements.txt` is unpinned, while `artifact/requirements-artifact.txt`
   names older Torch and NumPy versions than the recorded runtime.
6. GPU debug training was run with deterministic algorithms and cuDNN
   determinism disabled. Seeds and checkpoints permit continuation, but a
   byte-identical fresh GPU retrain is not guaranteed.
7. Commit the final paper evidence tree and refresh every hash after the last
   manuscript or report edit. Until then, a final immutable paper source is
   **not verifiable from supplied evidence**.
8. Confirmatory bridge, matched PPO, projection cross-design, persistent
   checkpoint diagnostics, and second-domain results have not run. This is a
   scientific evidence gap, not a failure of the verified debug artifacts.
