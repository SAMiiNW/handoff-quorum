import json
import re
import time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text()
ADDRESS = json.loads((ROOT / "deployment.json").read_text())["contractAddress"]


def account(slot):
    key = re.search(rf'^ACCOUNT_{slot}_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
    return create_account(account_private_key=key)


def finalized(client, method, args):
    tx = client.write_contract(address=ADDRESS, function_name=method, args=args, value=0)
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
    assert "MAJORITY_AGREE" in str(receipt.get("result_name", "")).upper()
    leader = ((receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]).get("execution_result")
    assert str(leader).upper() == "SUCCESS"
    return str(tx)


incumbent, successor, observer = account(1), account(2), account(3)
clients = [create_client(chain=studionet, account=x) for x in (incumbent, successor, observer)]
record = "LIVE-" + str(int(time.time()))
dossier = "https://raw.githubusercontent.com/SAMiiNW/handoff-quorum/222e2c9/evidence/live-dossier.txt"
policy = "https://raw.githubusercontent.com/SAMiiNW/handoff-quorum/222e2c9/evidence/live-policy.txt"
gap = "https://raw.githubusercontent.com/SAMiiNW/handoff-quorum/222e2c9/evidence/live-observer-gap.txt"
transactions = {}
transactions["open"] = finalized(clients[0], "open_handoff", [record, "Technical succession evidence review", successor.address, observer.address, ["Document deployment rollback procedure", "Inventory unresolved incidents", "Identify production change approvals"], dossier, policy, 600, 600])
transactions["accept"] = finalized(clients[1], "accept", [record])
transactions["verify"] = finalized(clients[0], "verify", [record])
transactions["block"] = finalized(clients[2], "block", [record, gap])
state = clients[0].read_contract(address=ADDRESS, function_name="get_handoff", args=[record])
assert state["state"] == "BLOCKED"
print(json.dumps({"recordId": record, "transactions": transactions, "state": state["state"], "decision": state["decision"]}))
