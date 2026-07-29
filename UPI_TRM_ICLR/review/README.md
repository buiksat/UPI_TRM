# UPI--TRM ICLR consolidated archive

`UPI_TRM_ICLR_COMPLETE.zip` is the single paper handoff archive.

It contains:

- the final rendered PDF;
- a self-contained LaTeX source tree and current build logs;
- finite-MDP generator, outputs, and validation log;
- episodic and persistent per-seed evidence;
- retained experiment protocols and provenance;
- revision, experiment, and final-validation reports;
- the external review prompt;
- a SHA-256 manifest for every archived file.

The source tree can be rebuilt with:

```bash
cd source
make pdf
```

Known evidence gaps remain explicit in the manuscript: no PPO per-seed run artifact, no projection--clamping factorial per-seed artifact or test script, and no interaction-matched UPI--TRM/PPO result.

Absolute local paths are sanitized only in the archive copy. Raw checkpoints, LaTeX intermediates, historical template builds, withdrawn studies, and obsolete venue handoff notes are excluded.
