# UPI-TRM paper artifact

The canonical paper is in `UPI_TRM_ICLR/` on branch `main`. Its semantic oracle is
`UPI_TRM_ICLR/main.tex`; theorem-facing terminology and implementation claims
must agree with that file.

The read-only implementation reference is
`https://github.com/gopeshh/trm_bellman`, branch `full-implementation`. The
paper describes one fixed-base candidate proposal at one frozen parameter
snapshot. It does not certify a recursively promoted CPI sequence.

The current implementation protocol distinguishes systems-only Stage 0 smoke
checks from later learned studies. Stage 0 is not paper evidence. Experiment 1B
run5 is the published learned-evaluator diagnostic: eight signed proxy-radius
differences on one fixed 128-state census, with mean `14.248703798855473` and
nominal seed-bootstrap interval
`[12.185185177643433, 16.739775084598428]`.

The later verification recovered the Stage A manifests, checked all 35 digest
links, replayed each census state from the sealed checkpoints, and ran an
independent checker against the additive audit bundle. Those checks reproduce
the finite-census measurement. They do not independently replicate training or
prove historical execution. The interval is conditional on one common base
initialization and the fixed census. Seeds, not census records, are the
resampling units; the interval establishes neither finite-sample coverage nor
independence across datasets or base-policy preparations. The paper makes no
learned-task performance, uniform-certificate, monotonic-depth, convergence,
or CPI claim from run5 and does not use deleted historical results.

Build the anonymous ICLR PDF from a clean auxiliary-file state:

```bash
cd UPI_TRM_ICLR
make clean
make pdf
```

Verify the exact finite-MDP calculation with only the Python standard library:

```bash
python3 UPI_TRM_ICLR/verify_finite_mdp.py
```

The script is a deterministic arithmetic check, not an experiment.
