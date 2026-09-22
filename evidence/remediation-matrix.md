# Steward remediation matrix

| Requirement | Code and proof | Status |
|---|---|---|
| Close activate/block race | Separate `review_deadline`; finalization only after it, block allowed through boundary; direct boundary test | PASS — local test |
| Pin dossier and policy | Both sources fetched and SHA-256 committed during open; verify rejects changed bytes | PASS — deployed and exercised |
| Recover INCOMPLETE, BLOCKED, LAPSED | `revise` requires incumbent and changed origin pair, resets acceptance and increments revision | PASS — deployed contract and direct tests |
| Correct product framing | Contract decision renamed `EVIDENCE_COMPLETE`; site and README disclaim operational authority | PASS — repository and public UI |
| Full live flow | Fresh deployment plus finalized open, accept, verify and observer block using three independent wallets | PASS — record `LIVE-1790111455`, final state `BLOCKED` |
| Reproducible tests | Pinned dependency manifest, tox entry point, expanded direct suite and interface assertions | PASS — 10 tests |
