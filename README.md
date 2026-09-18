# HANDOFF QUORUM / TRANSFER MANIFEST

```text
OBJECT        operational authority
OUTGOING      incumbent wallet
INCOMING      nominated successor
WATCH         independent emergency observer
LOAD          frozen dependency checklist
ROUTE         OFFERED > ACCEPTED > VERIFIED > ACTIVE
SIDINGS       INCOMPLETE / BLOCKED / LAPSED
```

## Why this manifest exists

A changed admin name is not a transfer of operational readiness. Handoff Quorum turns succession into a three-role custody movement. The incumbent freezes the dependency load, dossier, governing policy, and activation window. The successor must explicitly accept the load. Validators fetch the two public records and return the exact missing dependency indexes. Only a `READY` record can move toward activation.

The observer does not cast a vague veto. A block requires separately hosted evidence, validator agreement that it identifies a material unresolved dependency, and a stored digest. If the successor disappears after verification, anyone can move the expired transfer to `LAPSED`.

## Station checks

- `OFFERED`: roles, sources, checklist, and 5-minute-to-7-day window are sealed.
- `ACCEPTED`: the nominated successor, and nobody else, accepted custody.
- `VERIFIED`: every dependency is covered; two source digests remain attributable.
- `ACTIVE`: the successor activated inside the window.
- `BLOCKED`: the designated observer proved a material gap.
- `LAPSED`: permissionless recovery closed an abandoned verified transfer.

## Workshop inspection

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```

The direct suite runs successful custody, unauthorized acceptance, timeout recovery, observer intervention, and a forged missing-index result. Deployment coordinates are intentionally absent until reviewed source, wallet, network run, and public build agree.
