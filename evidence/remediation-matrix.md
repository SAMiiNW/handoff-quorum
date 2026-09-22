# Steward remediation matrix

| Requirement | Code and proof | Status |
|---|---|---|
| Close activate/block race | Separate `review_deadline`; finalization only after it, block allowed through boundary; direct boundary test | PASS — local test |
| Pin dossier and policy | Both sources fetched and SHA-256 committed during open; verify rejects changed bytes | PASS locally pending deployment |
| Recover INCOMPLETE, BLOCKED, LAPSED | `revise` requires incumbent and changed origin pair, resets acceptance and increments revision | PASS locally pending deployment |
| Correct product framing | Contract decision renamed `EVIDENCE_COMPLETE`; site and README disclaim operational authority | PASS locally pending browser deployment |
| Full live flow | Requires a fresh deployment and finalized open, accept, verify, observer-window, record sequence | UNVERIFIED — deployment pending |
| Reproducible tests | Dependency manifest, CI workflow, expanded direct suite and interface assertions | PASS locally pending CI |
