# HANDOFF QUORUM / TRANSFER MANIFEST

```text
OBJECT        technical succession evidence
OUTGOING      incumbent wallet
INCOMING      nominated successor
WATCH         independent emergency observer
LOAD          frozen dependency checklist
ROUTE         OFFERED > ACCEPTED > VERIFIED > REVIEW WINDOW > RECORDED
SIDINGS       INCOMPLETE / BLOCKED / LAPSED
```

## Why this manifest exists

A changed admin name is not a transfer of operational readiness. Handoff Quorum records whether a succession dossier covers a frozen dependency checklist. It does not transfer keys, credentials, system access, organizational approval, or legal authority. The incumbent freezes the dependency load, byte digests of the dossier and policy, an observer review window, and a later activation window. The successor must explicitly accept the load. Validators refetch the pinned records and return exact missing dependency indexes. Only `EVIDENCE_COMPLETE` may enter observer review.

The observer does not cast a vague veto. A block requires separately hosted evidence, validator agreement that it identifies a material unresolved dependency, and a stored digest. Activation is impossible until the observer window closes, including at its exact boundary. If the successor disappears, anyone can move the expired transfer to `LAPSED`. `INCOMPLETE`, `BLOCKED`, and `LAPSED` records can be revised by the incumbent using a changed pair of origins; the successor must accept the new revision again.

## Station checks

- `OFFERED`: roles, sources, checklist, and 5-minute-to-7-day window are sealed.
- `ACCEPTED`: the nominated successor, and nobody else, accepted custody.
- `VERIFIED`: the pinned dossier technically covers every dependency; this is not proof of operational authority.
- `RECORDED`: the review window closed and the successor finalized the technical evidence record inside the later window. This state does not transfer keys, access, credentials, legal authority, or operational control.
- `BLOCKED`: the designated observer proved a material gap.
- `LAPSED`: permissionless recovery closed an abandoned verified transfer.

## Workshop inspection

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```

The direct suite covers the finalize-versus-block boundary, changing source bytes between open and verify, validator disagreement, unauthorized acceptance, timeout recovery, and revisions from every failure state. `requirements-dev.txt` pins the test tools and `tox.ini` reproduces lint, direct tests, and interface checks.

## Observer-blocked route

`StudioNet / 0x94781DA4710C6fbf08FB4A3A641CA6DD1f968077`

The technical manifest `LIVE-1790111455` travelled through offer, successor acceptance, validator verification, and the observer response window. The designated observer then submitted material gap evidence, producing the final `BLOCKED` state. All four writes finalized with majority agreement and successful execution. This demonstrates the repaired race boundary without claiming that the demo wallets are independent authorities. Inspect the [contract](https://explorer-studio.genlayer.com/address/0x94781DA4710C6fbf08FB4A3A641CA6DD1f968077), review the transaction hashes in `evidence/network-run.json`, or open the [public conveyor](https://samiinw.github.io/handoff-quorum/).
