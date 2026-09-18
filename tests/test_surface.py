from pathlib import Path
TEXT=Path('contracts/contract.py').read_text();PAGE=Path('docs/index.html').read_text()
def test_contract_surface():
 for name in ('open_handoff','accept','verify','activate','block','lapse','get_handoff'):assert 'def '+name in TEXT
def test_interface_surface():
 for name in ('open_handoff','accept','verify','activate','block','lapse','get_handoff'):assert name in PAGE
 assert "status:'FINALIZED'" in PAGE
