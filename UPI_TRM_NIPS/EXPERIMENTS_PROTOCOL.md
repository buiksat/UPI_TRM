# Experiment protocol: theorem-aligned hard-suite rerun

## Goal
Test whether episodic-z UPI-TRM on the no-mask hard 4x4 6-8-empty suite has measurable finite-batch contact with the CPI error bound. This is not a proof of the global theorem; all theorem-tracking quantities are empirical proxies on a frozen held-out closure batch.

## Non-claims
This protocol does not produce, and the resulting paper text shall not state:
- a verified version of Theorem 6.5 or Corollary 6.7 on the hard suite;
- an estimator-quality guarantee for any of the nine logged quantities;
- a sample-complexity bound;
- a predictor of out-of-distribution policy improvement.

Diagnostics 1-9 are reported as finite-batch proxies for the global suprema appearing in Sections 5-6, evaluated on a frozen held-out closure batch. Any paper-text claim phrased as "we verify" or "we prove" about these diagnostics is a protocol violation.

## Locked protocol
- Suite: no-mask hard 4x4 Sudoku, 6-8 empties
- Budget: 20k environment steps
- Horizon: T=16
- Seeds: 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
- Latent mode: episodic-z
- Baseline: exact action-space summation
- Policy update: exact mixture where feasible; if distillation is used, log distillation KL
- Evaluation interface: same interface used for architecture-matched baselines
- Reported task metrics: success, return, invalid-action rate

## Required theorem-tracking diagnostics
A run is not reported as theorem-aligned evidence unless all nine are logged:

1. Held-out finite-depth Bellman residual: eps_res,n
2. Centering defect: eps_cent
3. Candidate advantage bias: eps_A,cand
4. Surrogate-true gap across alpha grid
5. Predicted CPI penalty across alpha grid
6. Local value-head Lipschitz proxy: L_V
7. Projection saturation margin: rho_R
8. Post-projection Lipschitz proxy: L_z_post
9. Projection-active rate

## Alpha grid
alpha in {0.05, 0.1, 0.2, 0.4}

## Reproducibility lock
- Closure batch: 256 held-out instances from the 6-8-empty no-mask distribution, sampled with seed 1729
- Closure batch frozen before training begins
- The closure batch and the L_V perturbation directions are fixed at protocol commit time
- Diagnostics are computed against this frozen batch at checkpoints {5k, 10k, 15k, 20k}; 20k is the primary reported value
- The closure batch is never resampled, refiltered, or augmented
- If a diagnostic value at 20k looks wrong or larger than expected, it is still reported as the measurement
- Re-running diagnostics against a different batch or different perturbation directions is a protocol violation
- L_V finite-difference perturbation scale: epsilon = 1e-4
- No architecture or hyperparameter retuning relative to the persistent-z hard-suite configuration except latent mode and exact-centering requirements
- Stopping rule: all seeds run to 20k unless NaN, OOM, or hardware failure

## Decision rule
Let S_E be episodic-z success rate.
Let S_P = 57.4 be persistent-z success rate.
Let gap_alpha be the measured surrogate-true gap at alpha.
Let pen_alpha be the predicted CPI penalty at alpha using measured proxy constants.

### Branch A: strong theorem contact
Condition: S_E >= 0.85 * S_P and gap_alpha <= pen_alpha for every alpha in {0.05, 0.1, 0.2, 0.4}.

Action: Section 7 leads with finite-batch theorem-contact diagnostics at the empirical anchor. State that the measured proxy penalty dominates the measured gap on the tested batch/grid.

### Branch B: qualitative theorem contact
Condition: S_E >= 0.85 * S_P and gap_alpha <= pen_alpha for alpha in {0.05, 0.1}, with pen_alpha / gap_alpha <= 5 at the operating alpha.

Action: Report measured-vs-predicted ratio. Keep structural framing, but say the proxy bound is calibrated within the stated factor on the tested batch/grid.

### Branch C: vacuous bound
Condition: S_E >= 0.85 * S_P but pen_alpha > 1.0 at all alpha in {0.1, 0.2, 0.4}.

Action: Keep structural framing. Report constants and say the measured proxy bound is conservative/vacuous for improvement-step selection on this benchmark.

### Branch D: episodic-z underperforms
Condition: S_E < 0.85 * S_P.

Action: Persistent-z remains the empirical algorithm; episodic-z becomes the theory companion. Demote theorem from headline contribution.

### Branch E: run failure
Condition: training fails to complete on more than 50% of seeds.

Action: Report failure mode in appendix if relevant; do not use the run as positive evidence.
