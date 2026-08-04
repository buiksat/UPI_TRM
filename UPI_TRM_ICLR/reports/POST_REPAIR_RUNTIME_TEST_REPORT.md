# Post-repair runtime test report

Date: 2026-08-03, America/Los_Angeles

## Source identity

- Code repository branch: `iclr-confirmatory-repair`
- Code commit: `e4c924cc721e9f4f356789eba03a09f6c8ca1913`
- Producer worktree before and after the run: clean
- Buck cell: `fbcode//buiksat_trm`
- Mode: `@fbcode//mode/opt`, `--local-only`

## Command

The invocation selected all 33 `python_unittest` targets declared in the
package `BUCK` file. It used no target or test-case filter. Target names were
derived from the declarations and passed explicitly to:

```text
buck2 test --local-only @fbcode//mode/opt \
  fbcode//buiksat_trm:test_run_identity \
  ... all 33 declared python_unittest targets ... \
  fbcode//buiksat_trm:test_constraint_aware_masking \
  -- --timeout=600
```

## Result

```text
Tests finished: Pass 397. Fail 0. Timeout 0. Fatal 0. Skip 0. Omit 0.
Infra Failure 0. Build failure 0.
```

- Start: 2026-08-03 20:07:38 PDT
- Finish: 2026-08-03 20:14:14 PDT
- Duration: 6 minutes 35 seconds
- Buck trace: `ce53bee3-4ede-412f-a196-0e96d77d3b91`
- Test session: `32369622344952422`

The local Buck event log is intentionally not staged into the paper artifact
tree because it contains workstation and internal-monorepo metadata. The trace
identifier and exact result are retained here.

## Static-check boundary

This was the complete declared runtime suite, not a package-wide static-type
run. The last package-wide audit retained 21 failing generated type targets
from pre-existing debt, including nine pre-existing errors in the `rl` target.
The model and utility type targets passed in the focused audit. These static
failures remain open and are not hidden by the 397 passing runtime cases.
