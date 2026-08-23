# UPI-TRM paper artifact

The canonical paper is in `UPI_TRM_ICLR/` on branch
`iclr-evidence-aligned-revision`. Its semantic oracle is
`UPI_TRM_ICLR/main.tex`; theorem-facing terminology and implementation claims
must agree with that file.

The read-only implementation reference is
`https://github.com/gopeshh/trm_bellman`, branch `full-implementation`. The
paper describes one fixed-base candidate proposal at one frozen parameter
snapshot. It does not certify a recursively promoted CPI sequence.

The current implementation protocol distinguishes systems-only Stage 0 smoke
checks from later learned studies. Stage 0 is not paper evidence. This paper
contains no learned-task performance claim and does not use deleted historical
results.

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
