# Experiment Triage

## Scope

This inventory covers every result-bearing experiment subsection, empirical
table, and empirical figure currently rendered by `main.tex`. It also records
the two evidence/implementation tables that organize the experiments and the
one unused empirical table source in `tables/`. No source, result, or raw data
has been deleted or moved as part of this triage.

Path aliases in this report are:

- `PAPER_REPO/`: the current ICLR paper repository.
- `CODE_REPO/`: the implementation repository.

The authoritative provenance inputs are
`reports/HISTORICAL_PROVENANCE_AUDIT.md` and
`reports/CLAIM_EVIDENCE_LEDGER.md`. A retained aggregate is not confirmatory
evidence merely because its arithmetic can be recomputed.

## Decision rule

The paper should reserve its experimental space for these questions, in this
order:

1. Do finite-batch augmented-state diagnostics connect successful persistent
   checkpoints to at least one theorem condition?
2. Which single factor, or predeclared interaction, explains the
   persistent-versus-episodic gap?
3. How does corrected UPI--TRM compare with PPO at equal environment
   interactions on one immutable held-out pool?
4. What is the frozen forward-pass effect of projection, separated from its
   training effect?
5. Does the result transfer to one preselected verifier-guided domain?

None of those five confirmatory results currently exists. The present learned
model records are historical, exploratory, incomplete, or missing the
checkpoints and byte-identified data needed for reruns. The finite-MDP result
is a theorem-pipeline unit test, not empirical validation.

## Subsection inventory

There are 25 labeled experiment subsections in the current manuscript: five in
the main text and 20 in the appendix. The appendix also has one unlabeled
finite-difference diagnostic paragraph. `Keep` below means retain in compact
form. It does not promote the evidence status.

| Source and label | Subject | Classification | Provenance constraint | Disposition |
| --- | --- | --- | --- | --- |
| `main.tex`, `sec:harder_puzzles` | Persistent hard-suite implementation and limitations | useful secondary diagnostic; historical record | Successful checkpoints, hard data, ordered pool, and augmented diagnostics are absent; theorem instantiation is not verifiable from supplied evidence | Keep as a short limitation with no performance headline |
| `main.tex`, `sec:projection_contraction_ablation` | Historical projection x clamping summary | exploratory; not reproducible | Cell arithmetic is retained, but the dataset, checkpoints, ordered outcomes, and test script are absent; mechanism claims are not verifiable from supplied evidence | Move the numerical result to the external legacy report; retain one limitation sentence |
| `main.tex`, `sec:episodic_negative_main` | Episodic old-policy endpoint | useful secondary diagnostic; negative result; historical record | Ten-seed aggregate exists, but checkpoints, hard data, producer commit, and exact-mixture endpoint do not | Keep one compact negative-result paragraph, explicitly old-policy and in-sample |
| `main.tex`, `sec:interaction_audit_main` | Budget audit | useful secondary diagnostic; missing experiment | The common-budget sweep is incomplete and contains no UPI--TRM arm | Keep one sentence stating that the comparison is missing |
| `main.tex`, `sec:finite_mdp_main` | Exact finite-MDP calculation | theorem unit test | Numeric pipeline is reproducible; exact historical plotting environment is not verifiable from supplied evidence | Keep, but call it a unit test and avoid empirical framing |
| `main.tex`, `app:finite_mdp_certificate` | Detailed finite-MDP construction and results | theorem unit test | Generator and 101-row CSV are retained | Keep a compact appendix description and reproducibility pointer |
| `main.tex`, `app:sn_instability` | Spectral-normalization failure modes | exploratory; not reproducible | Checkpoint and raw batch identities are absent | Move to external legacy report |
| `main.tex`, `app:latent_collapse_diagnostic` | Latent-collapse isolation | exploratory; single-seed; underpowered; not reproducible | One seed and short follow-ups; checkpoints and raw batches are absent | Move to external legacy report |
| `main.tex`, `app:toy_feasibility` | Easy-suite sanity check | exploratory; underpowered; not relevant to hard-suite claim | Three seeds; masked random succeeds 52%; historical corpus identity is not verifiable from supplied evidence | Move to external legacy report |
| `main.tex`, `app:exp1_tables` | B0 depth/radius tables | useful secondary diagnostic; exploratory; not reproducible | Aggregate tables remain, but checkpoints and B0 batches are absent | Move to external legacy report; remove duplicate label declaration |
| `main.tex`, `app:finite_r_b0` | Fine-grained fixed-pair radius sweep | exploratory; redundant; not reproducible | Derived figures remain, but checkpoints and raw evaluation batches are absent | Move to external legacy report |
| `main.tex`, `app:exp1_b1` | B1 successor-state radius sweep | exploratory; redundant; not reproducible | Same provenance gap as B0; B1 is noisier and duplicates the qualitative pattern | Move to external legacy report |
| `main.tex`, `app:exp2_sweep` | Projection dominance and failed clamping dial | useful negative diagnostic; exploratory; not reproducible | Aggregate tables exist; checkpoint and raw batch identities are absent | Move both tables and the null dial result to external legacy report |
| `main.tex`, `app:exp4_projection_free_dial` | Inference-time scale range | exploratory; single-checkpoint; underpowered; not reproducible | One checkpoint and 100 samples; checkpoint is absent | Move to external legacy report |
| `main.tex`, `app:exp3_projection_ablation` | Easy-suite training stability | exploratory; underpowered; not relevant to hard-suite claim | Easy-suite historical records only; no broad stability inference is justified | Move to external legacy report |
| `main.tex`, `app:exp4_projection_free_dial_v2` | Projection-free clamping sweep | exploratory; redundant; underpowered; not reproducible | Four scale points support neither a robust monotone mechanism nor a confirmatory correlation claim | Move to external legacy report; do not retain the significance claim in the paper |
| `main.tex`, `app:exp5_tradeoff_curve` | Stability--expressivity tradeoff | exploratory; underpowered; negative result; not reproducible | Success stays near 6.7%; checkpoints and raw batches are absent | Move to external legacy report and preserve the null result |
| `main.tex`, `app:harder_sudoku_detailed` | Hard-suite definition and random baseline | not reproducible | Dataset and random-policy artifact are absent; 0% random success is not verifiable from supplied evidence | Replace with a provenance limitation or remove from PDF |
| `main.tex`, `sec:controlled_2x2_main` | Historical hard-suite factorial | historical record; exploratory; not reproducible | Per-seed logs reproduce arithmetic; causal and statistical claims are not verifiable from supplied evidence | Move the full table to external legacy report |
| `main.tex`, `sec:isolation_study` / `app:depth_mismatch_main` | Depth-mismatch summary | useful secondary diagnostic; exploratory; not reproducible | Finite-batch easy-suite aggregate only; no global modulus and no persistent checkpoint | Move to external legacy report |
| `main.tex`, `app:controlled_2x2` | Repeated factorial interpretation | redundant; historical record | Repeats `sec:controlled_2x2_main` without new evidence | Remove from PDF after preserving the text externally |
| `main.tex`, `app:discussion_details` | Synthesis of legacy stability studies | redundant; exploratory | Repeats findings from five moved subsections | Remove from PDF after preserving the text externally |
| `main.tex`, `app:equalized_baselines` | Incomplete equal-interaction audit | useful secondary diagnostic; missing experiment | Partial baseline-only logs and no UPI--TRM arm | Replace the table with one sentence; retain details externally |
| `main.tex`, `app:headline_significance` | Historical seed arithmetic | historical record; not reproducible as a comparison | Aggregates are auditable; common pool, equal budget, checkpoints, data, and producer revision are absent | Move full seed lists and table to external legacy report |
| `main.tex`, `app:episodic_z_hard_suite_rerun` | Episodic endpoint and penalty diagnostics | negative result; finite-batch diagnostic only; historical record; not reproducible | Aggregate arithmetic exists; checkpoints, data, source logs, producer commit, and exact-mixture endpoint are absent | Keep one compact negative endpoint in the paper; move diagnostics and penalty table externally |
| `main.tex` paragraph before `tab:exp1_value_head_lipschitz` | Local value-head Lipschitz proxy | exploratory; useful secondary diagnostic; not reproducible | Retained summary only; checkpoint and B0 batch identities are absent | Move to external legacy report |

## Table inventory

The manuscript renders 17 result-bearing empirical tables, plus three
evidence/implementation-status tables. The notation table is theoretical and
is outside this inventory. One additional empirical table source is present
but not included by `main.tex`.

| Label and source path | Classification | Disposition |
| --- | --- | --- |
| `tab:claim_status`, `main.tex` | useful claim/evidence map | Keep and update from the final ledger |
| `tab:diagnostics`, `main.tex` | implementation definition | Keep in a compact implementation appendix |
| `tab:equalized_baselines`, `main.tex` | useful secondary diagnostic; missing experiment | Replace with one sentence; archive the table |
| `tab:exp1_value_head_lipschitz`, `tables/table_exp1_value_head_lipschitz.tex` | exploratory; not reproducible | Move |
| `tab:sn_instability`, `main.tex` | exploratory; not reproducible | Move |
| `tab:latent_collapse`, `main.tex` | single-seed; underpowered; exploratory | Move |
| `tab:upi_success_only`, `main.tex` | three-seed easy-suite sanity check; underpowered | Move |
| `tab:unroll_sensitivity`, `tables/table_exp1_unroll_sensitivity.tex` | exploratory depth diagnostic; not reproducible | Move |
| `tab:radius_sweep`, `tables/table_exp1_radius_sweep_main.tex` | exploratory B0 radius diagnostic; not reproducible | Move |
| `tab:radius_sweep_b1`, `tables/table_exp1_radius_sweep_appendix.tex` | redundant B1 diagnostic; not reproducible | Move |
| `tab:exp2_dial_failure`, `tables/table_exp2_dial_does_not_control_Lz.tex` | useful null diagnostic; exploratory | Move and preserve the null result |
| `tab:exp2_projection_stabilizer`, `tables/table_exp2_projection_effect.tex` | exploratory composite projection contrast | Move |
| `tab:exp4_projection_free_dial`, `tables/table_exp4_projection_free_dial_range_test.tex` | single-checkpoint; underpowered | Move |
| `tab:exp3_projection_ablation`, `tables/table_exp3_projection_ablation.tex` | easy-suite exploratory result | Move |
| `tab:exp4_projection_free_dial_v2`, `tables/table_exp4_projection_free_dial_v2.tex` | redundant; four-point correlation; underpowered | Move; drop the confirmatory-sounding significance language |
| `tab:exp5-tradeoff`, `tables/table_exp5_tradeoff_curve.tex` | exploratory null result | Move and preserve the null result |
| `tab:controlled_2x2_main`, `main.tex` | exploratory historical factorial; not reproducible | Move |
| `tab:hard_suite_anchor`, `main.tex` | confounded historical records; not reproducible as a comparison | Move |
| `tab:episodic_z_branch_d`, `main.tex` | negative historical endpoint plus finite-batch diagnostics | Move full table; retain only a compact endpoint sentence in the paper |
| `tab:episodic_z_penalty`, `main.tex` | derived finite-batch penalty; nonfinite in 2/10 seeds | Move and preserve the nonfinite outcome |
| `tab:contraction_sweep`, `tables/table_exp2_contraction_sweep.tex` | unused stale empirical source; exploratory | Do not add to the paper; archive as legacy source |

## Figure inventory

| Label and source path | Classification | Disposition |
| --- | --- | --- |
| `fig:trm_architecture`, `main.tex` TikZ | implementation definition, not an empirical result | Keep after ensuring the clock-complete state is shown |
| `fig:finite_mdp_certificate_main`, `results/finite_mdp_certificate/fig_value_decomposition.png` and `fig_cpi_certificate.png` | theorem unit test | Keep one compact figure or replace with a concise test table |
| `fig:exp1_finite_r_b0`, `figures/fig_exp1_finite_r_primary_b0.png`, `fig_exp1_finite_r_mechanism_b0.png`, and `fig_exp1_finite_r_theory_b0.png` | exploratory; redundant; not reproducible | Move all three panels to the external legacy report |

## Compact target paper

Before new experiments complete, the empirical paper should contain only:

1. the updated claim/condition/evidence/status table;
2. the finite-MDP theorem-pipeline unit test;
3. one compact negative episodic endpoint with its old-policy, in-sample, and
   provenance limitations;
4. one sentence stating that the persistent diagnostic runner exists but has
   no learned-checkpoint output, and that the bridge, matched PPO comparison,
   projection cross-design, and second-domain result are missing.

After registered runs complete, replace the missing-result sentence with the
five decision-relevant analyses. Do not restore the historical 57.4% record,
the factorial, or legacy depth sweeps to the main evidence narrative merely
because new experiments are delayed.

## Counts and actions

- Labeled experiment subsections: 25 total.
- Unlabeled empirical diagnostic blocks: 1.
- Result-bearing rendered tables: 17.
- Evidence/implementation-status tables: 3.
- Unused empirical table sources: 1.
- Empirical result figures: 2, one with three panels.
- Implementation-definition figures: 1.
- Current confirmatory learned-model results: 0.
- Current theorem-pipeline unit tests: 1.
- Subsections retained substantially: 2 (`sec:finite_mdp_main` and
  `app:finite_mdp_certificate`).
- Subsections retained only as compact limitations or negative records: 3
  (`sec:harder_puzzles`, `sec:episodic_negative_main`, and
  `sec:interaction_audit_main`).
- Subsections moved, replaced by a sentence, or removed from the PDF: 20.

The highest-impact cuts are the repeated projection/clamping narrative,
three B0/B1/radius presentations of the same qualitative pattern, the
four-point correlation table, the single-seed latent-collapse study, the
easy-suite feasibility tables, and the full historical UPI--TRM/PPO table.
Those cuts remove unsupported mechanism and performance impressions while
preserving every null and negative result in `reports/ARCHIVED_EXPERIMENTS.md`.
