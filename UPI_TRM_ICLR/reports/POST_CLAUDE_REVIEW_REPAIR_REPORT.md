# Post-review repair report

Date: 2026-08-04, America/Los_Angeles

Claude's corrected final panel tally was 25 findings emitted, 11 rejected by
the adversarial gate, and 14 surviving findings: one high, three medium, and
ten low. This report records the repairs after that review. It does not record
or imply a confirmatory experiment result.

## Implementation state

- Repository: `CODE_REPO/`
- Branch: `iclr-confirmatory-repair`
- Pushed commit: `1880b41c196109add997f1663190ca36d6b70be5`
- Producer-source manifest SHA-256:
  `ff7eb54793cd7a0cf26cc5b9df14a5caf6c57b3f0aefdd901194ae532b515747`
- Registry status: `registered_not_authorized`

The repair makes the anonymous archive scanner fail closed, scrubs the
reported affiliation and build-system tokens including `/data/repos/...`, and
adds scanner-error tests. Standalone ZIP/PAR runtimes now hash their behavior
source members against the embedded manifest. Confirmatory restarts use an
explicit attempt index and fresh checkpoint, evaluation, log, lock, and
execution-index paths. Existing evidence is never overwritten.

The lower-severity fixes reject an all-false edit mask, renormalize tolerated
probability rows before TV/KL diagnostics, preserve the latest actual optimizer
metrics at cap-only milestones, enforce PPO interval divisibility in the
registered configuration test, correct PPO and DQN documentation, and add a
numeric terminal-boundary GAE test. The current production GAE implementation
was already correct.

## Verification

One optimized local Buck invocation ran all 33 declared runtime targets:

```text
Tests finished: Pass 409. Fail 0. Timeout 0. Fatal 0. Skip 0. Omit 0.
Infra Failure 0. Build failure 0.
```

The retained log is
`CODE_REPO/reports/POST_CLAUDE_REVIEW_FULL_UNITTESTS.log`, SHA-256
`516c5952c3e61752a0fc700a51aa07d8f28dd1e1309ae6fa303fa1b36c060b98`.

The full 68 MiB code archive rebuilt byte-identically twice at SHA-256
`c60c67772ad65aa97265e0bc596b57e73f883920f66611dac6b322f03bdf11b0`.
ZIP integrity passed. A case-insensitive content and path scan over 3,719
extracted paths found none of the forbidden identity, affiliation, internal
host, build-root, user, or prior-venue tokens. The archive remains a local
code artifact and is not part of the paper-only review ZIP.

The deterministic corpus verifier now reports the completion-reuse caveat
from committed labels: 283 of 288 valid 4 by 4 completions occur in the corpus,
and 494 of 512 test records share a completion with a training record. The
paper states that the held-out split measures constraint satisfaction on
unseen givens, not generalization to unseen solution grids.

## Execution status

No confirmatory training, bridge result, matched PPO comparison, successful-
checkpoint diagnostic, projection cross-design, or second-domain experiment
was run. Those outcomes remain `missing experiment` or
`not verifiable from supplied evidence`, as applicable. The retained
seed-9001 debug bundle was produced by pre-amendment commit `e4c924c` and is
excluded from confirmatory analysis. New execution requires regenerated
schema-3 locks bound to the pushed producer commit above.
