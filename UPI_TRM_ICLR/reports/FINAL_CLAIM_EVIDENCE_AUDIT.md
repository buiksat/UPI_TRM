# Final Claim-Evidence Audit

Date: 2026-08-03, America/Los_Angeles

## Scope

This audit covers the current working-tree manuscript, claim-evidence ledger,
run registry, artifact manifests, retained numerical outputs, and named files
under `UPI_TRM_ICLR/`. It does not treat the seed-9001 debug runs as scientific
results. Mathematical proof validity is covered separately by
`reports/FINAL_PROOF_AUDIT.md`.

Audited manuscript SHA-256:

```text
f1f7bb567578dbf1b4a3ab1d7c3db4cfdf3acee8b6e7fb9f818a8239550344e7
```

The paper branch base HEAD during the audit was
`c0c6acae8d591acbd99441eb3b17b6d2306df50d`; the audited files contained
uncommitted revision work.

## Decision

After corrections made during this audit, no surviving unsupported
performance, sample-efficiency, contraction, held-out, interaction-matched, or
learned-model theorem-instantiation claim remains in `main.tex`. The active
empirical position is accurate: the historical learned records do not support
a method comparison, while the finite-state calculations are numerical
theorem-pipeline tests only.

The evidence package is not release-complete. A current PDF build and a
complete anonymous supplement are each
`not verifiable from supplied evidence`.

## Corrections During Audit

The following issues were reported and corrected before this report was
written:

1. The conclusion had categorically said that the episodic endpoint did not
   score the configured mixture. The retained rows identify only `greedy`
   mode, and the producing revision is unresolved. The paper now says that the
   endpoint does not establish that it scored the configured mixture.
2. The finite-MDP text called the surrogate gap positive for every tested
   mixture weight although the retained `alpha=0` row is exactly zero. The
   text now states positivity only for tested `alpha>0` and records the zero
   boundary explicitly.
3. Ledger row I05 had identified the historical evaluator as old-policy-only.
   It now records the checkpoint-level policy identity as
   `not verifiable from supplied evidence`.
4. The finite-MDP run registry recorded seed 7 although the command used the
   script default and every CSV row records seed 0. The registry now records
   seed 0.
5. The finite-MDP registry formerly implied one clean producer commit. It now
   distinguishes the execution base HEAD `896af29...` from the first complete
   two-script pipeline commit `77f73e1...` and records per-file commits.
6. The paper embedded legacy finite-MDP PNGs that were not bound to the
   registered reproduction. It now embeds the byte-reproduced PNGs under
   `results/finite_mdp_certificate_validation/`, and their hashes are in the
   manifest.

## Numerical Claims

### Historical episodic endpoint

- `per_seed_eval.jsonl` contains four nominal checkpoints for each seed 41
  through 50.
- All ten step-20,000 rows have success rate zero. The manuscript's `0.0%`
  over ten seeds is arithmetically verified.
- The rows record 50 episodes and `eval_policy_mode=greedy`, but do not identify
  which policy component supplied the greedy logits.
- Checkpoints, raw producer logs, the historical hard-suite dataset, ordered
  evaluation hashes, and the exact producer revision are absent. Policy
  identity, independent regeneration, and held-out interpretation are
  `not verifiable from supplied evidence`.

### Historical persistent record

The active manuscript does not print the historical 57.4% result, the PPO
aggregate, the factorial contrasts, or historical inferential statistics. It
labels the retained persistent record in-sample and unmatched. This agrees
with the provenance audit: 50 evaluations cycled over 32 training records,
and the historical checkpoints, ordered outcomes, exact interaction counters,
hard-suite data, and producer revision are absent.

### Finite-MDP unit test

The retained CSV has 101 data rows: 80 `value_curve` rows and 21 `cpi_curve`
rows. Both certificate flags equal one in all 101 rows. The retained
configuration values and manuscript text agree:

- 64 states and 4 actions;
- `gamma=0.9`, `K=3`, and `sigma_xi=0.05` for the value slice;
- four `L_z` values and 20 depths;
- `L_z=0.2`, `n=16`, `sigma_xi=0.1`, and `beta=1` for the CPI slice;
- 21 mixture weights, including the exactly zero `alpha=0` boundary.

An independent current-tree execution of

```text
python3 experiments/finite_mdp_certificate.py --outdir <temporary-directory>
```

reproduced the CSV byte-for-byte with SHA-256
`52875311ee5d7144ffce5afc2853c746440de5810836c631bc69f8fdb85996d6`.
It also byte-reproduced both paper-visible PNGs:

```text
fig_value_decomposition.png  e2d6e1fcf9be297ca76d114ba4a0fd57bba7aa6f6120010f513d306d778cc26f
fig_cpi_certificate.png       2b2b37d6dd9b956cbf40ec7456ddb2ecf4e7173fc35b04a855d3b2e26ee4e661
```

These outputs support a numerical theorem-pipeline unit test, not learned-model
validation.

### Finite-horizon regression

An independent execution of

```text
python3 experiments/finite_horizon_theory_checks.py \
  --seed 20260803 --random-cases 200
```

returned `PASS` with 26,686 assertions and the boundary cases named in the
paper. Its output agrees with
`reports/finite_horizon_theory_checks.stdout.json`, SHA-256
`2bcd3fadd5ad7094b397e492b711d524f65c52d7fe6efea6062922e105a0d8e6`.

## Dataset and Debug Evidence

The immutable confirmatory corpus is present in the code repository. Direct
manifest inspection found 1,024 train, 256 validation, and 512 test records;
every split has unique input and record hashes, and all three pairwise overlap
counts are zero. The three manifest hashes match the paper registry.

The run registry contains exactly three theorem-unit-test runs and eight
debug-pipeline smokes, with zero confirmatory training runs. For every debug
cell checked:

- `excluded_from_confirmatory=true`;
- seed is 9001;
- training interaction count is exactly 80;
- evaluation contains 256 unique validation records and 4,096 interactions;
- all four staged evaluation files match their registered SHA-256 values.

`main.tex` contains no occurrence of `debug`, `smoke`, `9001`, or any debug
outcome. The claim ledger and registry consistently say that these runs test
execution mechanics only. They are not promoted into bridge, PPO-comparison,
performance, or theorem-facing learned evidence.

## Artifact and Supply Audit

All directly resolvable working-manifest entries matched their recorded hashes
at the time checked. The manifest's `main.tex` entry now records the audited
SHA-256 above. The two recorded pre-repair build files are absent and are
explicitly marked `not verifiable from supplied evidence`.

Every file named in `main.tex` was found and was nonempty. In particular:

- `reports/ARCHIVED_EXPERIMENTS.md`;
- `experiments/finite_horizon_theory_checks.py`;
- `reports/THEORY_EXTENSION_DERIVATION.md`;
- `experiments/finite_mdp_certificate.py`;
- `results/finite_mdp_certificate_validation/finite_mdp_summary.csv`;
- `reports/finite_mdp_certificate_validation.log`;
- both finite-MDP figure PNGs.

The manuscript makes no positive claim that these files are in a submitted
archive. Its only review-package statement uses the required wording:
`not verifiable from supplied evidence`.

The nested debug manifest and checksum are internally consistent. It binds the
staged execution index, all 32 staged evaluation files, eight effective
configurations, and external checkpoint/log hashes. The external checkpoint
and log bytes are not staged, which the top-level manifest states explicitly.

The older Git bundle
`handoff/trm_bellman_iclr-confirmatory-repair.bundle` is thin and requires
commit `6d5a241027fe72921d5fc039dd6a12434999088b`. It must not be used as the
standalone implementation handoff. The replacement
`handoff/trm_bellman_iclr-confirmatory-repair_e4c924c_full.bundle` has SHA-256
`5a357c0caa118907426da517aa0a7dc8df4f980fbe38ae9f8a13d0a6035e5ed4`.
`git bundle verify` reports complete history. A fetch into an empty repository
resolved head `e4c924cc721e9f4f356789eba03a09f6c8ca1913` and tree
`c1eeed790105ca63e77e937db794cdfa305e92a5`, matching the live producer
repository. This verifies standalone reconstruction. It does not establish
anonymous release suitability: the Git history contains author names, email
addresses, and internal hostnames. The full bundle is a current-code handoff,
not an anonymous reviewer supplement.

## Required-Term Search

The Phase 17 search produced the following disposition:

- `submitted`: three occurrences, all disclaiming supply or using exactly
  `not verifiable from supplied evidence`.
- `included`, `verified`, `significant`, `outperforms`, `state of the art`,
  `all seeds`, and `pre-registered`: no occurrences.
- `certified`: three occurrences, all conditional mathematical language or an
  explicit statement that local proxies certify neither global factor.
- `contraction`: formal Bellman/recurrent assumptions, proved conditional
  propositions, or explicit empirical disclaimers. Empirical interventions are
  called `clamping enabled` or contraction-oriented, not certified contraction.
- `held-out` and `interaction-matched`: only requirements or explicit missing-
  evidence statements. The paper says no such learned-model comparison exists.
- `debug` and `smoke`: no manuscript occurrences.

## Remaining Blockers

1. The host lacks a TeX engine, `pdfinfo`, and `pdffonts`. A current source PDF,
   page count, resolved-reference check, font check, and visual inspection are
   `not verifiable from supplied evidence`.
2. `artifacts/MANIFEST.json` declares `complete=false` and
   `anonymous_release_ready=false`. No complete anonymous supplement exists.
3. No successful persistent checkpoint exists for augmented residual,
   centering, deployment-gap, or slow-drift diagnostics.
4. The one-factor bridge, equal-interaction UPI--TRM/PPO comparison, projection
   cross-design, and second-domain experiment remain `missing experiment`.

These blockers do not create a hidden positive claim in the current
manuscript. They prevent a submission-ready evidence bundle and leave the
reviewers' empirical decision boundary unmet.
