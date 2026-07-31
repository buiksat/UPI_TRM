# UPI-TRM Repair Review

> ## Re-review (round 2) — supersedes the round-1 verdict below
>
> **Updated verdict: APPROVE WITH NON-BLOCKING FOLLOW-UPS.** All three round-1 blockers (B1, B2, B3) are fixed and independently verified; every code fix claimed by the fix-round (N1–N8, N10) is verified correct **and** complete. The code branch is safe to commit/push, and both archives are safe to use as the submitted artifact. The remaining items are non-blocking hygiene.
>
> **Blockers — verified fixed:**
> - **B1 (de-anonymization):** both archives now contain **0** files with `/home/`, `buiksat`, or `UPI_TRM_NIPS` (scanned by extracting and grepping). Checksums match the fix-round report and the sidecars (paper `bcaa06a2…`, code `075f1416…`), and sidecars now store basenames only. `scripts/build_artifact_zip.sh` was rewritten to stage a copy, anonymize file **contents and path names**, and **fail the build (exit 1) if any identifier survives** (lines 88–96) — the exact bundle-lint gate recommended in B1. Rebuilding twice is byte-identical and reproduces the committed `075f1416…`, so the shipped code artifact provably matches current source.
> - **B2 (supplement filename):** `main.tex:1244` now cites `diagnostics_summary.json`; all four cited files (`diagnostics_summary.json`, `cpi_penalty_grid.json`, `per_seed_diagnostics.jsonl`, `EPISODIC_Z_RUN_LOG.md`) ship in the bundle.
> - **B3 (in-sample table):** `table_hard4x4_trusted_baselines.tex` is unbolded, relabeled "Historical record … not a method comparison," with the row as "UPI--TRM (in-sample)."
>
> **Non-blocking fixes — verified:** N1 CleanRL now builds a disjoint eval split, rejects equal split names / too-small pools / train–eval hash overlap, and all three eval paths use `bundle.eval_dataset` (`ppo_trm.py:326`, `dqn_trm.py:201`, `dqn_inhouse_wrapper.py:141`). N2 `_mean_categorical_kl` masks both log tensors on the reference support (no `0*inf`) with a NaN guard. N3 PPO keeps the truncation reward correction **and** cuts the GAE trace via `next_done = _episode_done_flags(terminated, truncated)`. N4 DQN epsilon-random samples from valid actions (`_sample_random_action`). N5 checkpoints save/restore python+numpy+torch-CPU+CUDA RNG with a schema-version legacy fail-closed. N6 checkpoints persist `dataset_provenance` and raise on mismatch at resume. N7 sudoku **and** maze builders use seeded `np.random.default_rng`. N8 hardcoded `/home/buiksat` script defaults are gone (0 in the code artifact). N10 archive is byte-reproducible.
>
> **Re-validation (first-hand):** `py_compile` 78/78 OK; `git diff --check` clean; finite-MDP CSV in the new bundle 101/101/101; provenance unit tests **5/5 pass** (`python3 -m unittest tests.test_result_provenance_unittest` — order-sensitive hashing, portable-zip builder, budget-unit separation, fail-closed pool provenance); both archive checksums match; archive reproducible.
>
> **Still open (non-blocking, mostly not claimed fixed):** N9 — 43 root `*.log` files remain git-tracked (they now ship **anonymized**, so cosmetic; `slurm_error_trm.txt`/`slurm_output_trm.txt` are removed from the working tree but their deletion is not yet staged, and `AUDIT_REPORT.md:108`'s "removed temporary logs" is still slightly overstated). N11–N16 nits (dead `_project_to_ball`, stale `validate_theory_alignment` docstring, `_QNetworkEvalAdapter` drops `z`, stray annotations, diagnostics default `--paper-root`, central no-cycling guard) were not part of the fix-round and remain optional cleanup.
>
> **Not independently runnable in this sandbox** (no torch / not a Buck cell / no LaTeX): the fix-round's "Buck 33/33", torch unit tests, and "PDF 38 pages, clean refs/fonts". The compiled `UPI_TRM_ICLR/main.pdf` (1.17 MB) is present in the bundle; page count and reference log were not re-verified here.
>
> **Next actions before landing:** (1) commit both repos (working trees are uncommitted — `trm_bellman` at `6d5a241` +148 changes, `UPI_TRM` at `2a86aae`), staging the `slurm_*` deletions; (2) optionally address N9/N11–N16; (3) the shipped archives already match their sidecars, so no rebuild is required unless the source changes again.
>
> ---

Reviewer: independent adversarial review (RL correctness, ML-systems, artifact integrity).
Scope: `/home/buiksat/trm_bellman` working tree vs `6d5a241027fe72921d5fc039dd6a12434999088b` (branch `feature/upi-trm-clean`), and `/home/buiksat/UPI_TRM` working tree (branch `iclr-revision`, HEAD `2a86aae`), including `UPI_TRM_ICLR/main.tex`, `UPI_TRM_ICLR_COMPLETE.zip`, and `artifact/upi_trm_repository.zip`.
Method: change-set classification, first-hand tracing of the highest-risk paths, a 10-lens adversarial subagent review with per-finding default-reject verification (32 agents, 0 errors), and bounded deterministic validation. `AUDIT_REPORT.md`/`README.md` were treated as claims to verify, not truth.

---

## 1. Verdict

**REQUEST CHANGES** — narrowly, and only on the *submitted paper bundle*, not the code.

The correctness repairs are real and hold up under tracing. Every high-risk RL path I checked (exact probability-space mixture deployment, exact statewise centering with post-clip re-centering, K-step targets with terminal masking and incomplete-segment rejection, budget-exhaustion-as-terminal, ordered-pool SHA-256 provenance, the fail-closed hard-suite aggregator, checkpoint contents, projection joint-norm) matches what the audit and paper claim. The paper has been honestly rewritten: it now labels 57.4% as in-sample, the 0% episodic endpoint as old-policy-only, disclaims the Welch statistic, and demotes the theory to a conditional decomposition. The headline statistics reproduce to the digit, and the finite-MDP certificate CSV has 101/101 rows with both flags true.

What blocks using the current `UPI_TRM_ICLR_COMPLETE.zip` **as a double-blind ICLR artifact**:

- **B1 (major):** the submitted bundle ships nine files containing the author's home path `/home/buiksat/...` and the prior venue tag `UPI_TRM_NIPS`. `main.tex` is scrubbed; the artifacts it points reviewers to are not. This is a de-anonymization / desk-reject risk.
- **B2 (minor):** `main.tex` cites a supplement file (`episodic_diagnostics_summary.json`) that ships under a different name (`diagnostics_summary.json`).
- **B3 (minor):** a shipped result table still bolds the in-sample 57.4% as beating held-out baselines, contradicting the corrected in-sample framing everywhere else.

**Safe to commit/push the code branch:** yes — the code repairs are correct, `git diff --check` is clean, and all changed Python compiles. **Safe to use the zips as the submitted artifact:** not yet — fix B1–B3 and rebuild both archives + sidecars first. None of the blockers is a scientific-correctness or algorithm-behavior defect.

---

## 2. Blocking findings

### B1 — Submitted double-blind bundle leaks author identity and prior venue (major)
- **File/evidence:** inside `UPI_TRM_ICLR_COMPLETE.zip` (verified with `unzip -p`):
  - `UPI_TRM_ICLR/EPISODIC_Z_RUN_LOG.md` — 29 occurrences of `/home/buiksat`, 24 of `UPI_TRM_NIPS`; e.g. line 10 `Locked protocol: /home/buiksat/UPI_TRM/UPI_TRM_NIPS/EXPERIMENTS_PROTOCOL.md`, line 13, line 62.
  - `UPI_TRM_ICLR/results/episodic_z_hard_suite_20k_seed41_50/per_seed_diagnostics.jsonl` — per-row `"checkpoint": "/home/buiksat/trm_bellman/checkpoints/..."`, `"diagnostics_path": "/home/buiksat/UPI_TRM/UPI_TRM_NIPS/..."`.
  - Also leaking and bundled: `REEVAL_LOG.md`, `TABLE1_PROVENANCE.md`, `reports/ICLR_EXPERIMENT_PLAN.md`, `reports/ICLR_FINAL_VALIDATION.md`, `reports/finite_mdp_certificate_validation.log`, `results/.../per_seed_eval.jsonl`, `results/.../summary.json`.
- **Affected claim/path:** the paper cites these as submitted evidence (`main.tex:1243` "The supplement includes `EPISODIC_Z_RUN_LOG.md`, ..." and ~`main.tex:869` "the submitted `finite_mdp_certificate_validation.log`"). `main.tex` itself is anon (`\author{Anonymous Author(s)}`, `iclr2026_conference` anon default), so the leak is entirely in the cited supplement.
- **Why it matters:** the Unix username `buiksat` in absolute paths plus the `UPI_TRM_NIPS` tag de-anonymize the submission and reveal a prior NeurIPS attempt of the same work — a plausible desk reject at a double-blind venue. `.gitignore` force-includes `reports/finite_mdp_certificate_validation.log` (`!/reports/...`), so these are intentional bundle contents, not scratch.
- **Smallest fix:** rewrite absolute paths to repo-relative and `UPI_TRM_NIPS`→`<anon>` in every bundled artifact (and regenerate them from anonymized sources going forward), then rebuild `UPI_TRM_ICLR_COMPLETE.zip` and its `.sha256`. The prior-venue tree `UPI_TRM_NIPS/` exists in the paper repo working tree but is *not* in the zip (verified: 0 entries) — keep it out.
- **Regression test:** a bundle-lint check that greps the file list of the built zip for `/home/`, a home username, and known prior-venue tags, failing the build on any hit. (Applies equally to `artifact/upi_trm_repository.zip`; several tracked scripts embed `/home/buiksat` defaults — see N8.)

### B2 — Paper cites a supplement filename that is not in the bundle under that name (minor)
- **File:** `UPI_TRM_ICLR/main.tex:1243` lists `episodic_diagnostics_summary.json`; the file shipped in the zip is `UPI_TRM_ICLR/results/episodic_z_hard_suite_20k_seed41_50/diagnostics_summary.json`.
- **Evidence:** the same edit that renamed the sibling (`episodic_per_seed_diagnostics.jsonl` → `per_seed_diagnostics.jsonl`, visible in the `main.tex` diff) missed this one; `unzip -l` shows `diagnostics_summary.json`, not `episodic_diagnostics_summary.json`.
- **Why it matters:** a reviewer following the citation finds no such file; it misstates the bundle.
- **Fix:** change the `main.tex` citation to `diagnostics_summary.json` (or rename the file to match). **Test:** extend the bundle-lint to assert every `\texttt{...\.(json|jsonl|md|log)}` name cited in `main.tex` exists in the zip.

### B3 — Shipped result table bolds the in-sample 57.4% as a win, contradicting the corrected narrative (minor)
- **File:** `trm_bellman/results/paper_ready/hard4x4_trusted_baselines_20k/table_hard4x4_trusted_baselines.tex:6` (`UPI--TRM & 20k & 10 & \textbf{57.4 $\pm$ 12.2} & ...`) sits bolded above four baseline rows; same in `.../hard4x4_trusted_baselines/` and the sibling `per_seed_metrics.csv`/`summary.{csv,json}`. These are in the code artifact (`artifact/upi_trm_repository.zip`, 3024 files).
- **Affected claim:** directly contradicts `main.tex` / `README.md` / `AUDIT_REPORT.md`, which now label 57.4% in-sample and not comparable to held-out baselines, and contradicts the current stricter aggregator (`scripts/aggregate_hard4x4_trusted_baselines.py`), which would `RuntimeError` on these hash-less inputs.
- **Why it matters:** a reviewer opening the artifact sees the exact framing the repair set out to retract.
- **Fix:** regenerate/annotate these retained tables as `UPI--TRM (in-sample)` without emphasis, or move them under a clearly-labeled `historical/` path. **Test:** none needed beyond B1's inventory lint plus a note in `README.md` pointing at the file.

---

## 3. Non-blocking findings

All are real (CONFIRMED against source) but affect **no reported number**, the build, or reproducibility of any claimed result. Ordered by importance.

- **N1 (major, latent) — CleanRL TRM Sudoku baselines evaluate in-sample and can cycle a sub-size pool.** `rl/cleanrl/trm_adapter.py:140-143` `build_sudoku_bundle` calls `build_dataset_from_paths(...)` with **no split** (defaults `split="train"`, `rl/training_setup.py:97`) and builds no eval bundle; `_evaluate_sudoku` (`ppo_trm.py:283`), `_evaluate_sudoku_dqn` (`dqn_trm.py:200-201`), the A2C wrapper, and `dqn_inhouse_wrapper.py:135-137` all eval on `bundle.dataset`; the evaluator cycles with `env.reset(idx=episode_idx % dataset_size)` (`rl/evaluator.py:101-102`) with no refusal. None of the UPI/SB3 guards (disjoint split, overlap rejection, no-cycling, pool hash) apply here. This reproduces the historical 57.4% failure mode in a live code path with a dedicated benchmark script. **It also refutes the audit's blanket wording** ("Training and evaluation split names must differ", "Evaluation refuses to repeat a smaller pool") — those repairs are real for the UPI + SB3 paths but *not* repository-wide. Fix: route CleanRL Sudoku eval through a disjoint split + `ordered_pool_sha256`, or scope the audit/README claims to the UPI/SB3 entry points. Test: a CleanRL Sudoku eval test asserting eval indices are disjoint from train and that `num_episodes > pool` raises.

- **N2 (major, default-off) — KL trust-region computes `0 * inf = NaN` on masked actions.** `rl/upi_trm_trainer.py:1494` `kl_div = (old_probs * (old_log_probs - new_log_probs)).sum(-1).mean()`: at masked actions `old_probs=0` (from `EditPolicyHead` `masked_fill(~mask, -inf)`, `models/edit_policy.py:70,79`), `old_log_probs=log(clamp(0,1e-8))≈-18.42` finite (`:1441`), `new_log_probs=-inf` (`log_softmax`, `:1492`) → `0*inf=NaN`, propagating through `loss_policy` (`:1497`), `backward()`, `policy_opt.step()`. The NaN also defeats the early-stop guard (`kl_val > 1.5*target` is False for NaN, `:1501-1502`). Same pattern in the distillation branch (`:1581-1584`). Gated behind `enable_kl_trust_region` (default `False`, `rl/config.py:129`), enabled by nothing in configs/tests, and never on the theory-exact headline path — so no result is affected. Fix: `torch.where(mask, per-action-kl, 0)` before summing. Test: `policy_update` with an active mask and `enable_kl_trust_region=True` asserting finite `kl_div`.

- **N3 (minor) — CleanRL PPO truncation double-bootstraps + leaks across episodes.** `rl/cleanrl/ppo_trm.py:420-434` adds `gamma*V(final_obs)` to the reward on `truncated and not terminated`, but `next_done = terminated` only (`:437`), so GAE also bootstraps `V(reset_obs)` and never cuts the trace. Dormant in the Sudoku task (budget exhaustion is a *terminal*, so `truncated` is not set there), but wrong for any time-limit-truncated env. Fix: set the GAE continuation mask from `terminated | truncated` while keeping the reward correction. Test: a two-env rollout with a forced truncation asserting the advantage at the truncated step bootstraps exactly once.

- **N4 (minor) — CleanRL DQN epsilon-random ignores the action mask.** `rl/cleanrl/dqn_trm.py:356-357` `action = random.randrange(num_actions)` samples over all actions, while its own greedy branch and TD target mask, and the in-house `rl/algos/dqn.py:511-517` restricts random exploration to valid actions. Internal inconsistency + parity gap on a heavily-masked space. Fix: sample from `where(mask)` like the in-house DQN. Test: assert random-branch actions are always valid under a mask.

- **N5 (minor) — Checkpoints omit RNG state: `resume_from_checkpoint` is warm-start, not exact continuation.** `upi_trm_train.py:451-514` saves model/old/candidate/target, both optimizers, distill opt, schedulers, puzzle-emb opt, counters, `term_stats`, and full replay, but no Python/NumPy/torch/CUDA RNG; `:532-604` restores none. Replay sampling uses `torch.randint`/`torch.randperm` (`rl/replay.py:102,178,183,253`), so a resumed run diverges from an uninterrupted one. `README.md:22` calls these "resumable checkpoints" without the caveat (it does not claim RNG, but "resume" implies continuation). Per the review's own standard, either persist RNG or rename to warm-start. Fix: add `get_rng_state`/`set_rng_state` for all four generators, or relabel. Test: save→resume→one step reproduces an uninterrupted step's sampled minibatch.

- **N6 (minor) — Checkpoints omit dataset identity; resume validates nothing.** `upi_trm_train.py:451-514` stores `rl_config`/`model_config` but no `dataset_paths`/split/pool SHA-256 (only printed at `:1129-1140`); `:532-604` performs no dataset check, so relaunching with different `--dataset-paths`/`--eval-split` silently mixes restored replay with new-dataset rollouts. Fix: persist the pool hash + split names and assert on resume.

- **N7 (minor) — Sudoku/maze builders use the unseeded global NumPy RNG.** `dataset/build_sudoku_dataset.py:26,29,33,37,77` (`np.random.permutation/rand` in `shuffle_sudoku` + subsample) and `dataset/build_maze_dataset.py:53` are not seeded, so generated train data is **not** reproducible under the recorded seed — contradicting `AUDIT_REPORT.md` ("Generated ARC, maze, and Sudoku data are deterministic under the recorded seed"). Fix: thread a `np.random.default_rng(seed)` through the builders. Test: two builds at the same seed produce identical bytes.

- **N8 (minor) — Shipped scripts hardcode `/home/buiksat` defaults.** `scripts/aggregate_hard4x4_trusted_baselines.py:83,88,93` (`default="/home/buiksat/trm_bellman/results/..."`), `scripts/audit_exp1_paper_ready.py:34,37`, `scripts/generate_ablation_configs.py:6`, `scripts/run_shaped_reward_experiments.sh:4`. These `FileNotFound` out-of-the-box for a third party and also carry the username into the code artifact. Fix: make the paths required args or repo-relative. (Ties into B1's anonymization.)

- **N9 (minor) — Cleanup claim overstated: machine state remains.** `AUDIT_REPORT.md:108` says machine state / temporary logs were removed, but a ~4.4MB warnings-only `slurm_error_trm.txt` and other root-level `*.log`/`slurm_output_trm.txt` are still tracked and shipped in `artifact/upi_trm_repository.zip`. Fix: remove or ignore them; soften the audit wording.

- **N10 (nit) — `build_artifact_zip.sh` is not byte-reproducible.** `scripts/build_artifact_zip.sh:31` orders deterministically (`sort -u`) but `zip` embeds mtimes/extended-timestamp/UID, so re-running yields a different SHA-256 with identical contents. The `README_ARTIFACT.md` implies a stable checksum. Fix: `zip -X` and normalize mtimes (or `TZ=UTC` + `-X` + fixed `--` timestamps) if a reproducible checksum is intended.

- **N11 (nit) — Diagnostics default `--paper-root` points at the stale tree.** `scripts/episodic_z_hard_suite_diagnostics.py:38` (also 122, 743-746) defaults to `.../UPI_TRM/UPI_TRM_NIPS`, not the ICLR revision the README calls current. Fix: default to the ICLR path or require the arg.

- **N12 (nit) — `_QNetworkEvalAdapter.policy_dist` accepts `z` and drops it.** `rl/cleanrl/trm_adapter.py:465-481` declares `z` but never forwards it, so persistent-latent DQN eval would silently discard carried state. Dormant (DQN eval is episodic). Fix: forward `z` or raise if non-None.

- **N13 (nit) — Stray annotations in `_obs_to_buffer`.** `rl/cleanrl/dqn_trm.py:246-247` adds `q_network: Any` / `target_network: Any` inside a function that uses neither. Dead. Fix: delete.

- **N14 (nit) — Dead method `_project_to_ball`.** `models/recursive_reasoning/trm.py:297` is unused after every call site moved to `_project_carry_to_ball`. Fix: remove.

- **N15 (nit) — Stale docstring in `validate_theory_alignment`.** `rl/config.py:261-265` still lists Assumptions 4.1/4.2 as required, while the body demotes both to non-blocking `specialization_notes` and `is_theory_exact()` no longer requires them. Fix: update the docstring.

- **N16 (nit) — No-cycling invariant lives only in callers.** `rl/evaluator.py:101-102` has no guard against `num_episodes > dataset_size`; it is enforced by the UPI/SB3 wrappers but not centrally, so a future caller can silently repeat records. Fix: raise in `evaluate_plan_policy_with_scores` when `num_episodes > len(dataset)` unless an explicit `allow_cycle=True`.

**Cleared as not-a-defect (reported for completeness):** the exp1 dispersion tables use population std (`np.std`/`statistics.pstdev`, e.g. `scripts/make_paper_figures_exp1.py:158`). Verification **REJECTED** this as a defect: the shipped `.tex` tables are generated by `make_paper_figures_exp1_final.py` (which copies a pre-aggregated `std` column, not those scripts), and the cells are pooled over states×seeds with `n≈1000` (`results/tables/unroll_sensitivity_b0_mismatch.csv`), where the ddof correction is ~0.05% and the quantity is not an across-seed sample std. No paper number is affected.

---

## 4. Historical-risk disposition

All four independently CONFIRMED from retained code/artifacts, consistent with (and not merely copied from) the audit.

| # | Hypothesis | Status | Evidence |
|---|---|---|---|
| 1 | Persistent 57.4% is in-sample: 50 evals cycled over 32 `train` records also used in training | **confirmed** | Retained UPI reeval artifact cycles 50 episodes over a materialized 32-record `train/` pool with no ordered-pool hash; `main.tex` abstract + `app:headline_significance` now state exactly this; evaluator cycles via `idx % dataset_size`. |
| 2 | PPO row used test records with no common eval-pool hash shared with UPI-TRM | **confirmed** | External JSON files name a `test` split but contain no `pool_sha256`; the current aggregator (`aggregate_hard4x4_trusted_baselines.py:242-252,581-587`) would `RuntimeError` on them; paper labels the PPO row "per-seed artifact and common pool hash unavailable." |
| 3 | Historical persistent path deployed parameter interpolation, not an exact mixture | **confirmed** | Current default mode 3 is `_sync_policy_old_towards_candidate()` param-space interpolation (`rl/upi_trm_trainer.py:1592-1597`), explicitly labeled non-theory-exact; `main.tex` remark + claim-status now say deployment used parameter interpolation. |
| 4 | Historical episodic 0% endpoint evaluated the old policy, not the deployed mixture | **confirmed** | Repaired eval only deploys the mixture when `theory_exact_mixture=True` via `policy_dist_fn=_mixed_policy_dist` + `greedy=False` (`:1998-2026`, `rl/evaluator.py:155-176`); the retained endpoint scored `policy_model_old`; `main.tex:app:episodic_z_hard_suite_rerun` states the endpoint scored only `policy_model_old`. |

The current code fixes #3 and #4 (verified first-hand). #1/#2 are unrepairable for the *historical* numbers because the hard-suite data and checkpoints are absent; the paper correctly does not relabel them as held-out.

---

## 5. Paper and artifact consistency

Surviving mismatches (all in packaging/citation, none in the math or empirical numbers):

1. **De-anonymizing paths + prior venue in the bundled supplement** (B1).
2. **`episodic_diagnostics_summary.json` cited but shipped as `diagnostics_summary.json`** (B2).
3. **`table_hard4x4_trusted_baselines.tex` bolds in-sample 57.4% as a win** (B3), contradicting `main.tex`/`README.md`/`AUDIT_REPORT.md`.
4. `AUDIT_REPORT.md:108` "removed machine state" vs retained `slurm_error_trm.txt` and root logs (N9).
5. `AUDIT_REPORT.md`/`README.md` blanket provenance claims vs the CleanRL Sudoku path that enforces none of them (N1).
6. `AUDIT_REPORT.md` "deterministic under the recorded seed" vs unseeded builders (N7).

**Consistent (verified):** every empirical number in `main.tex` matches code/artifacts — 57.4±12.2 and 32.0±15.3 recomputed from the printed seed vectors (ddof=1: 12.186/15.319), Welch `t=4.103, df=17.13, p=7.31e-4, CI [12.35,38.45]` reproduces `t≈4.10/df≈17.1/p≈7.3e-4/[12.4,38.5]`; finite-MDP CSV has 101 rows, both flags true; `γ=0.99/K=1/n=2`, `R=10`, operator-norm target `0.9`, projection +13.0pp / clamp +2.2pp all present. Theory-scope language is honest: clamping is "contraction-oriented intervention" (not global contraction), centering allows any exact-expectation method (states explicit summation), the measurable-space extension is a remark, and the abstract/title claim no operational certificate. `UPI_TRM_ICLR_COMPLETE.zip` sha256 matches its sidecar (`af665f75...`); `artifact/upi_trm_repository.zip` sha256 matches (`e6813575...`) and contains no secrets, checkpoints, nested archives, or self-inclusion.

---

## 6. Validation performed

Environment: `python3` 3.9/3.12 present; **torch, numpy, scipy, pytest, yaml are not importable in any interpreter**; `buck2` is on PATH but `trm_bellman` is not wired as a Buck cell here (`Error: not in a Buck project`). So torch-dependent unit tests, the Buck suite, type-check targets, entry-point runtime execution, and LaTeX compilation could **not** be run in this sandbox. These are skipped for a *missing-dependency* reason, not a product failure; the audit's "249 tests / 35 type-checks / 5 entrypoint builds / 38-page PDF" were **not** independently re-executed here.

| Check | Command | Exit | Result |
|---|---|---|---|
| Compile all changed/new Python | `python3 -m py_compile` over `git diff --name-only 6d5a241 -- '*.py'` + untracked `*.py` | 0 | **72/72 existing files OK, 0 failures** (8 listed are deletions) |
| Whitespace/conflict markers | `git diff --check 6d5a241` | 0 | **clean** |
| Headline std (ddof=1) | pure-python recompute | 0 | UPI 57.400/**12.186**, PPO 32.000/**15.319** → matches 57.4/12.2, 32.0/15.3 |
| Welch t/df/p/CI | pure-python (betai t-dist) | 0 | **t=4.1034, df=17.13, p=7.31e-4, CI [12.35, 38.45]** → matches paper |
| Finite-MDP certificate | read `finite_mdp_summary.csv` | 0 | **101 rows; `certificate_holds_decomp`=1 and `certificate_holds_exact_A`=1 for all 101** |
| Code artifact inventory | `unzip -l` vs `git ls-files --cached --others --exclude-standard` | 0 | **3024 == 3024**; no `/home/`, `*.pt/.pth/.ckpt`, `.pem/id_rsa/.env`, nested `*.zip`, or self-inclusion |
| Code artifact checksum | `sha256sum -c upi_trm_repository.zip.sha256` | 0 | **OK** (`e6813575...`) |
| Paper bundle checksum | `sha256sum UPI_TRM_ICLR_COMPLETE.zip` | 0 | **matches** sidecar (`af665f75...`) |
| Bundle de-anon scan | `unzip -p` grep `/home/buiksat`\|`UPI_TRM_NIPS` | 0 | **9 leaking files inside the zip** (B1) |
| Dangling refs to deletions | basename grep of retained tree over `--diff-filter=D` | 0 | only stale `# per CLAUDE.md` comments in configs/scripts (nit); `zip.sh`/`README.md`/fig2/`diagnose_*` hits were substring false positives or relocations; phase4 export deletion safe (generator input survives at `results/paper_ready/phase4_2x2_norm_ablation/summary.json`) |
| Adversarial 10-lens review | Workflow (32 subagents, per-finding default-reject verify) | — | 21 findings CONFIRMED, 1 REJECTED, 0 agent errors; 107 cleared areas |

---

## 7. Cleared high-risk areas (actually traced)

- **Environment transitions / MDP semantics:** `PlanEditEnv.step` sets `done=True` on budget exhaustion (`rl/envs/plan_edit_env.py:889-892,920-922,957`) with `terminated_by_budget` in `info` — a terminal, not a truncation; terminal reward folds the discounted absorbing tail (`:94-98`, `compute_transition_reward`); `remaining_edits` is in state snapshots and replay (`:219-232`, `rl/batch_utils.py`). Invalid-action masking is identical in training (`collect_episode`) and eval (`rl/evaluator.py:155-186`).
- **K-step targets:** `compute_k_step_bootstrapped_target` (`rl/value_targets.py:15-73`) uses `γ^k` reward weights, `γ^steps_taken` (≡`γ^K` under the guard) bootstrap, zeroes bootstrap on `done_final`, and **raises on incomplete non-terminal segments** in exact mode; `_sample_k_step_batch` selects only K-complete/early-terminal segments; the exact-Q successor gets the decremented edit clock (`utils/lipschitz.py:825-830`).
- **Exact policy mixture:** `_mixed_policy_dist` (`rl/upi_trm_trainer.py:321-383`) forms `probs_mix=(1-α)·probs_old+α·probs_new` and returns `Categorical(probs=probs_mix)` — a true probability-space mixture, sampled at eval via `policy_dist_fn` (`:1998-2026`, `rl/evaluator.py:164,176`); default mode 3 (param interpolation) is clearly labeled non-theory-exact.
- **Exact centering:** `compute_exact_baseline_summation` sums `Σ_a π(a)Q̂(a)`; `_clip_and_recenter_advantages` (`:17-35`) clips within mask then subtracts the policy-weighted mean of clipped values, restoring `E_π[Â]=0` and re-zeroing invalid actions.
- **Projection:** `_project_carry_to_ball` uses the joint Euclidean norm over both carries with zero-radius no-op, correct broadcasting, and identity gradient inside the ball (`models/recursive_reasoning/trm.py`); production and diagnostics share it. The joint-ball change vs historical per-carry projection is acknowledged in the paper.
- **Provenance:** `ordered_pool_sha256` (`utils/dataset_provenance.py:41-57`) hashes the first `count` records in order, content-based, and **fails closed** below `count`. The hard-suite aggregator requires `train`/`test`, 50 samples, one pool hash across seeds (`:311`) and the same hash across methods (`:581-587`, `RuntimeError` on mismatch), and refuses to emit a between-method gap interval (`:549`). Fail-closed dataset loading with opt-in dummy fallback (`rl/training_setup.py:104-165`); disjoint multi-root identifier ranges.
- **Checkpointing:** full save/restore of model/old/candidate/target, both optimizers + distill opt, schedulers, puzzle-emb opt, counters, `term_stats`, and full replay; `weights_only=False` scoped to the trusted resume loader with `map_location="cpu"` (replay stays off CUDA); reeval reconstructs non-default architectures from persisted config and fails closed on ambiguous legacy per-puzzle embeddings. (Gap: RNG + dataset identity — N5/N6.)
- **Statistics:** headline mean/std/Welch and the 101-row finite-MDP certificate reproduce exactly; `+∞` CPI penalty for seeds 41/46 with finite-subset arithmetic over the other 8 is handled and serialized as strict JSON; the paper disclaims inferential interpretation of the Welch stat.
- **Cleanup:** deleted W&B/ICML aggregation and NeurIPS builder are not the sole generator of any retained table/plot/claim; deleted export dirs have retained canonical copies; `.gitignore` excludes caches/checkpoints/pids/locks without hiding required source; `build_artifact_zip.sh` cannot self-include the archive.
- **Paper claims:** theorem scope, CPI notation, clamping/centering language, absence of duplicate labels/stale refs, and no over-claim of interaction matching / out-of-sample / exact-mixture deployment / uniform residual / preregistration — all verified against code and the retained artifacts.

---

## 8. Prioritized next actions

1. **Scrub the submitted bundle (B1).** Rewrite `/home/buiksat/...` → repo-relative and `UPI_TRM_NIPS` → anonymized in every file cited by `main.tex` and shipped in `UPI_TRM_ICLR_COMPLETE.zip`; keep the `UPI_TRM_NIPS/` tree out of the zip.
2. **Fix the two paper/artifact consistency items (B2, B3):** correct the `main.tex:1243` supplement filename; de-emphasize/relabel the in-sample 57.4% in the retained `hard4x4_trusted_baselines*` tables and CSVs.
3. **Rebuild both archives and sidecars** after 1–2: regenerate `UPI_TRM_ICLR_COMPLETE.zip` + `.sha256` and `artifact/upi_trm_repository.zip` + `.sha256`, then re-verify checksums and re-run the bundle de-anon/inventory lint.
4. **Commit the code branch** (`feature/upi-trm-clean`) — the RL/provenance/checkpoint/aggregator repairs are correct and safe. Nothing in §2 blocks the code.
5. **Then close the evidence-preserving latents (N1, N2, N7):** add a disjoint split + no-cycling guard to the CleanRL Sudoku eval path (or scope the audit claims to UPI/SB3), mask the KL/distill term to kill the `0*inf` NaN, and seed the dataset builders — each with the regression test noted.
6. **Reproducibility caveats (N5, N6):** either persist RNG + dataset identity in checkpoints, or rename `resume_from_checkpoint`/README wording to "warm-start."
7. **Style/hygiene last (N3, N4, N8–N16):** truncation bootstrap mask, DQN random masking, hardcoded paths, root logs, reproducible zip, stale defaults/docstrings/dead code.

Before the artifact is treated as final, rebuild the two zips (action 3) — they are the only generated artifacts that must be regenerated immediately after the scrub, since their current bytes carry the de-anonymization.
