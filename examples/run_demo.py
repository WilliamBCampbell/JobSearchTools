#!/usr/bin/env python3
"""Exercise the full evidence workflow in a disposable fictional workspace."""
import json,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import jobsearch as j

def build(root):
    j.init(root)
    here=Path(__file__).parent
    j.source_add(root,here/'demo-source.txt','demo-interview','fictional_fixture')
    j.fact_add(root,here/'demo-fact.json')
    package=root/'applications/example-123';package.mkdir()
    job={'company':'Example Employer','role':'Implementation Consultant','official_url':'https://example.invalid/jobs/123','requirements':[{'id':'r1','kind':'required','text':'Validate customer data imports'}]}
    jp=package/'job.json';pp=package/'selection.json';j.write(jp,job)
    j.review_init(root,jp,pp)
    plan=j.read(pp);plan.update(reviewed_by='Fictional fixture reviewer',complete=True,selected_ids=['example.imports'],area_review={'Example Systems':'Compared the fictional import example; direct evidence for validation, not project ownership.'},keyword_choices=[{'term':'validation','decision':'use','evidence_ids':['example.imports'],'reason':'Candidate described writing checks.'}],page_budget='One fictional bullet only; this is a test, not a finished resume.')
    plan['assessments']=[{'requirement_id':'r1','assessment':'direct','evidence_ids':['example.imports'],'reason':'Wrote validation checks for imports.'}]
    text='Wrote import validation checks for customer data imports.'
    plan['bullets']=[{'text':text,'area':'Example Systems','requirement_ids':['r1'],'evidence_ids':['example.imports'],'alternatives_considered':['Training mentioned in source but not yet a separate confirmed record.'],'reason':'Direct technical action matches the requirement.'}]
    j.write(pp,plan);j.check(root,jp,pp)
    artifact=package/'resume.txt';artifact.write_text(text+'\n')
    claims={'library_digest':j.digest(j.validate(root)),'plan_digest':j.digest(plan),'reviewed_by':'Fictional fixture reviewer','semantic_review_complete':True,'artifacts':[{'path':str(artifact.relative_to(root)),'sha256':j.sha(artifact),'text_path':str(artifact.relative_to(root)),'text_sha256':j.sha(artifact),'kind':'resume','all_factual_claims_mapped':True,'claims':[{'text':text,'kind':'career','evidence_ids':['example.imports'],'limits_reviewed':True}]}]}
    cp=package/'claim-map.json';j.write(cp,claims)
    result=j.audit(root,jp,pp,cp);j.write(package/'audit.json',result)
    return jp,pp,cp

if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='jobsearch-fictional-') as folder:
        root=Path(folder)/'workspace';build(root)
        print('Fictional source -> evidence -> requirement review -> resume text -> claim audit passed.')
        print('Temporary workspace removed on exit. No live search or application occurred.')
