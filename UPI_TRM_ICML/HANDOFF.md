# HANDOFF: Short Paper Consistency Check (2026-01-21)

## Summary

Verified and updated `main.tex` to ensure the SHORT version is internally consistent with the latest HARD 4×4 Sudoku (6–8 empties, 20k steps) results.

## Verified Claims (already correct)

| Variant | Actual | Paper Claims | Status |
|---------|--------|--------------|--------|
| persistent_nc | 56.7% ± 4.2% | ~57% | ✓ |
| episodic_nc | 48.0% ± 6.0% | ~48% | ✓ |
| episodic_c_clean | 36.7% ± 3.1% | ~37% | ✓ |
| PPO/A2C/DQN | 0.0% | 0% | ✓ |

## Changes Made

### Line 2330-2335: Updated hard-suite figure caption

**Before:**
```latex
\caption{Harder 4$\times$4 Sudoku (6--8 empties): success rate (feasible within $T{=}16$) vs.\ training steps (20k steps, 3 seeds).
No-contraction variants learn (persistent-$z$ reaches ${\sim}57\%$; episodic-$z$ reaches ${\sim}48\%$), while enforcing inner $z\!\to\!z$ contraction yields ${\sim}37\%$ success.
Standard baselines (PPO, A2C, DQN) fail (0\%); Random (uniform over valid actions) also achieves 0\%---the search space is now too large for chance completion.
This suggests $L_z{<}1$ can be overly restrictive on harder discrete tasks. Results are descriptive.}
```

**After:**
```latex
\caption{Harder 4$\times$4 Sudoku (6--8 empties): success rate (feasible within $T{=}16$) vs.\ training steps (20k steps, 3 seeds, greedy argmax + action masking, eval every 100 steps, 50 episodes).
No-contraction variants learn (persistent-$z$ reaches ${\sim}57\%$; episodic-$z$ reaches ${\sim}48\%$), while enforcing inner $z\!\to\!z$ contraction yields ${\sim}37\%$ success.
Standard baselines (PPO, A2C, DQN) fail (0\%); Random (uniform over valid actions) also achieves 0\%---the search space is now too large for chance completion.
\textbf{Protocol note:} No-contraction variants use projection $R{=}10$; contraction uses $R{=}0$; this asymmetry is inherited from the trivial-suite ablation design (Appendix~\ref{app:exp3_projection_ablation}).
Results are descriptive (3 seeds).}
```

**Why:**
1. Added explicit eval details: greedy argmax + action masking, eval every 100 steps, 50 episodes
2. Added projection asymmetry disclaimer (no-contraction uses R=10, contraction uses R=0)
3. Added pointer to controlled projection ablation appendix

## Sanity Checks Passed

- [x] No "T=20" anywhere (horizon is T=16)
- [x] No "near-zero success" claims for contraction on 6–8 empties (correctly says ~37%)
- [x] No "extended compute (n=4, R=10)" confusion
- [x] Figure 2 caption says "same runs as Table" (line 1636)
- [x] Figure file `feasibility_6to8empties_success_vs_steps.pdf` exists and matches expected content
- [x] Main text (line 1691) correctly states: "enforcing $L_z < 1$ yields ~37% success while unconstrained variants reach ~50–57%"

## File Linkage Verified

- `feasibility_6to8empties_success_vs_steps.pdf` exists in `figures/`
- Identical MD5 hash with `hard_4x4_baselines_success_vs_steps.pdf` (same file, different names)

## Compilation

```
pdflatex main.tex
Output written on main.pdf (27 pages, 671166 bytes)
```

No errors or warnings related to the changes.

