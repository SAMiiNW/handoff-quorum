from conftest import CONTRACT
import json

def llm(vm,pattern,response):
 vm.mock_llm(pattern,json.dumps(response))

DEPS=['Transfer production signing authority','Document open incidents','Confirm rollback access']
DOSSIER='https://handoff.example/dossier';POLICY='https://policy.example/succession'

def sources(vm,dossier='All three dependencies are documented for the successor.',policy='Technical evidence scope covers production operations.'):
 vm.mock_web(r'handoff\.example',{'status':200,'body':dossier});vm.mock_web(r'policy\.example',{'status':200,'body':policy})

def setup(vm,deploy,alice,bob,charlie):
 vm.warp('2035-01-01T00:00:00+00:00');vm.sender=alice;sources(vm);c=deploy(CONTRACT);c.open_handoff('ops-7','Production operations succession','0x'+bob.hex(),'0x'+charlie.hex(),DEPS,DOSSIER,POLICY,600,600);return c

def evidence(vm,decision='EVIDENCE_COMPLETE',missing='[]'):
 sources(vm);llm(vm,r'.*technical evidence coverage review.*','{"decision":"'+decision+'","missing_indexes":'+missing+'}')

def accept_and_verify(vm,c,bob,decision='EVIDENCE_COMPLETE',missing='[]'):
 vm.sender=bob;c.accept('ops-7');evidence(vm,decision,missing);c.verify('ops-7')

def fresh_sources(vm):
 vm.mock_web(r'revised\.example',{'status':200,'body':'Revised dossier covers every dependency.'});vm.mock_web(r'charter\.example',{'status':200,'body':'Revised technical evidence policy.'})

def test_successful_succession(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);accept_and_verify(direct_vm,c,direct_bob);p=c.get_handoff('ops-7');assert p['state']=='VERIFIED' and p['decision']=='EVIDENCE_COMPLETE' and len(p['digests'])==2
 direct_vm.sender=direct_bob
 with direct_vm.expect_revert('after observer review'):c.activate('ops-7')
 direct_vm.warp('2035-01-01T00:10:01+00:00');c.activate('ops-7');assert c.get_handoff('ops-7')['state']=='RECORDED'

def test_roles_and_timeout(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie)
 with direct_vm.expect_revert('nominated successor acceptance required'):c.accept('ops-7')
 accept_and_verify(direct_vm,c,direct_bob);direct_vm.warp('2035-01-01T00:20:01+00:00');direct_vm.sender=direct_alice;c.lapse('ops-7');assert c.get_handoff('ops-7')['state']=='LAPSED'

def test_validator_rejects_forged_missing_indexes(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;c.accept('ops-7');evidence(direct_vm);result=c._assess(c.handoffs['OPS-7']);assert direct_vm.run_validator(leader_result=result) is True;forged=dict(result);forged['missing']=[1];assert direct_vm.run_validator(leader_result=forged) is False

def test_observer_wins_until_review_deadline(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);accept_and_verify(direct_vm,c,direct_bob);direct_vm.warp('2035-01-01T00:10:00+00:00');direct_vm.clear_mocks();direct_vm.sender=direct_charlie;direct_vm.mock_web(r'observer\.example',{'status':200,'body':'Rollback access is absent.'});llm(direct_vm,r'.*emergency observer check.*','{"material":true}');c.block('ops-7','https://observer.example/gap');assert c.get_handoff('ops-7')['state']=='BLOCKED'

def test_evidence_change_between_open_and_verify_fails(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);direct_vm.sender=direct_bob;c.accept('ops-7');direct_vm.clear_mocks();sources(direct_vm,dossier='Changed after acceptance.');llm(direct_vm,r'.*technical evidence coverage review.*','{"decision":"EVIDENCE_COMPLETE","missing_indexes":[]}')
 with direct_vm.expect_revert('pinned handoff evidence changed'):c.verify('ops-7')

def test_incomplete_can_be_revised_with_new_origins(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);accept_and_verify(direct_vm,c,direct_bob,'INCOMPLETE','[2]');assert c.get_handoff('ops-7')['state']=='INCOMPLETE';direct_vm.clear_mocks();direct_vm.sender=direct_alice;fresh_sources(direct_vm);c.revise('ops-7','https://revised.example/dossier','https://charter.example/policy');r=c.get_handoff('ops-7');assert r['state']=='OFFERED' and r['revision']==2 and r['dossier_digest']

def test_blocked_revision_reopens_offer(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);accept_and_verify(direct_vm,c,direct_bob);direct_vm.clear_mocks();direct_vm.sender=direct_charlie;direct_vm.mock_web(r'observer\.example',{'status':200,'body':'A critical dependency is absent.'});llm(direct_vm,r'.*emergency observer check.*','{"material":true}');c.block('ops-7','https://observer.example/gap');direct_vm.clear_mocks();direct_vm.sender=direct_alice;fresh_sources(direct_vm);c.revise('ops-7','https://revised.example/dossier','https://charter.example/policy');assert c.get_handoff('ops-7')['state']=='OFFERED'

def test_lapsed_revision_reopens_offer(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 c=setup(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie);accept_and_verify(direct_vm,c,direct_bob);direct_vm.warp('2035-01-01T00:20:01+00:00');direct_vm.sender=direct_charlie;c.lapse('ops-7');direct_vm.clear_mocks();direct_vm.sender=direct_alice;fresh_sources(direct_vm);c.revise('ops-7','https://revised.example/dossier','https://charter.example/policy');assert c.get_handoff('ops-7')['state']=='OFFERED'
