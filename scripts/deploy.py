import json
import re
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
text = (ROOT.parents[3] / "accounts.env").read_text()
key = re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()
account = create_account(account_private_key=key)
client = create_client(chain=studionet, account=account)
tx = client.deploy_contract(code=(ROOT / "contracts" / "contract.py").read_text(), args=[])
print("deployment_tx=" + str(tx), flush=True)
try:
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
except TypeError:
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, status="FINALIZED", retries=180, interval=5000, full_transaction=True)
address = receipt.get("data", {}).get("contract_address") or receipt.get("to_address") or receipt.get("recipient")
print(json.dumps({"result": str(receipt.get("result_name")), "execution": str(receipt.get("tx_execution_result_name")), "data": receipt.get("data"), "to": str(receipt.get("to_address")), "recipient": str(receipt.get("recipient")), "consensus": receipt.get("consensus_data")}, default=str), flush=True)
assert "MAJORITY_AGREE" in str(receipt.get("result_name", "")).upper()
leader = ((receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]).get("execution_result")
assert str(leader).upper() == "SUCCESS"
print(json.dumps({"contractAddress": address, "deploymentTransaction": str(tx), "wallet": account.address}))
