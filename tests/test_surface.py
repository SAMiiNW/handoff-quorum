from pathlib import Path
TEXT=Path('contracts/contract.py').read_text(encoding='utf-8');PAGE=Path('docs/index.html').read_text(encoding='utf-8')
def test_contract_surface():
 for name in ('open_handoff','accept','verify','activate','block','lapse','revise','get_handoff'):assert 'def '+name in TEXT
def test_interface_surface():
 for name in ('open_handoff','accept','verify','activate','block','lapse','revise','get_handoff'):assert name in PAGE
 assert "status:'FINALIZED'" in PAGE
 assert 'data-step="1"' in PAGE and 'data-step="4"' in PAGE
 assert 'id="evidenceDock"' in PAGE and 'id="demoEvidence"' in PAGE
 assert 'class="compose"' not in PAGE
 assert 'Deployment pending' not in PAGE
 assert '0x9e3A9305fE74d40DA07728bFc22A89c61B221aFD' in PAGE
 assert 'does not transfer keys, credentials, access, or legal authority' in PAGE
 assert 'reviewWindow' in PAGE and 'revisedDossier' in PAGE and 'revisedPolicy' in PAGE
