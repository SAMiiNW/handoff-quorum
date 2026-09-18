from conftest import CONTRACT

DEPS=['Transfer production signing authority','Document open incidents','Confirm rollback access']
DOSSIER='https://handoff.example/dossier';POLICY='https://policy.example/succession'

def setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 direct_vm.warp('2035-01-01T00:00:00+00:00');direct_vm.sender=direct_alice;c=direct_deploy(CONTRACT);c.open_handoff('ops-7','Production operations succession','0x'+direct_bob.hex(),'0x'+direct_charlie.hex(),DEPS,DOSSIER,POLICY,600);return c

def evidence(vm,decision='READY',missing='[]'):
 vm.mock_web(r'handoff\.example',{'status':200,'body':'All three dependencies are assigned to the successor.'});vm.mock_web(r'policy\.example',{'status':200,'body':'Successor scope includes production operations.'});vm.mock_llm(r'.*HandoffQuorum\..*','{"decision":"'+decision+'","missing_indexes":'+missing+'}')

def test_successful_succession(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;c.accept('ops-7');evidence(direct_vm);c.verify('ops-7');p=c.get_handoff('ops-7');assert p['state']=='VERIFIED' and len(p['digests'])==2;direct_vm.sender=direct_bob;c.activate('ops-7');assert c.get_handoff('ops-7')['state']=='ACTIVE'

def test_roles_and_timeout(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie)
 with direct_vm.expect_revert('nominated successor acceptance required'):c.accept('ops-7')
 direct_vm.sender=direct_bob;c.accept('ops-7');evidence(direct_vm);c.verify('ops-7');direct_vm.warp('2035-01-01T00:11:00+00:00');direct_vm.sender=direct_alice;c.lapse('ops-7');assert c.get_handoff('ops-7')['state']=='LAPSED'

def test_validator_rejects_forged_missing_indexes(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;c.accept('ops-7');evidence(direct_vm);result=c._assess(c.handoffs['OPS-7']);assert direct_vm.run_validator(leader_result=result) is True;forged=dict(result);forged['missing']=[1];assert direct_vm.run_validator(leader_result=forged) is False

def test_observer_can_block_material_gap(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;c.accept('ops-7');evidence(direct_vm);c.verify('ops-7');direct_vm.clear_mocks();direct_vm.sender=direct_charlie;direct_vm.mock_web(r'observer\.example',{'status':200,'body':'Rollback access is absent.'});direct_vm.mock_llm(r'.*emergency observer check.*','{"material":true}');c.block('ops-7','https://observer.example/gap');assert c.get_handoff('ops-7')['state']=='BLOCKED'
