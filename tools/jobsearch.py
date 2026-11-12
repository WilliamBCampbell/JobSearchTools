#!/usr/bin/env python3
"""Portable, local evidence and application records. Python 3.10+, no dependencies."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from datetime import date, datetime, timezone, timedelta

STATES = {'confirmed', 'source_supported', 'draft', 'unknown', 'gap', 'superseded'}
USABLE = {'confirmed', 'source_supported'}
SCOPES = {'career', 'preference', 'application', 'private'}
STATUSES = {'shortlisted', 'prepared', 'ready', 'manual_required', 'unknown', 'submitted', 'rejected', 'withdrawn', 'closed', 'not_pursuing', 'offer'}
KINDS = {'status', 'interview_scheduled', 'interview_completed', 'interview_cancelled'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, data):
    """Replace atomically; workspace is single-writer, not a concurrent database."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.write-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def safe_id(value):
    require(bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', value)), 'Use a simple ID: letters, digits, dots, underscores, hyphens')
    return value


def within(root, relative):
    p = (Path(root) / relative).resolve()
    require(p.is_relative_to(Path(root).resolve()), 'Path escapes private workspace')
    return p


def init(root):
    root = Path(root).resolve()
    require(not root.exists() or not any(root.iterdir()), 'Choose a new or empty workspace; refusing to overwrite')
    root.mkdir(parents=True, exist_ok=True)
    for d in ('sources', 'applications', 'research', 'interviews', 'receipts', 'private'):
        (root / d).mkdir()
    write(root/'library.json', {'schema_version': 1, 'sources': [], 'records': []})
    write(root/'profile.json', {'name': None, 'location': None, 'target_roles': [], 'skills_to_emphasize': [], 'travel': {'preference': None, 'maximum': None}, 'compensation': {'currency': None, 'base_minimum': None, 'transition_flexibility': None}, 'constraints': [], 'onboarding_complete': False})
    write(root/'private/form-facts.json', {'answers': [], 'note': 'Only confirmed facts; no passwords, tokens, codes or government identifiers.'})
    write(root/'tracker.json', {'applications': [], 'events': []})
    write(root/'session.json', {'updated_at': now(), 'active_application': None, 'next_action': 'Complete onboarding', 'pending_questions': []})
    (root/'.gitignore').write_text('*\n!.gitignore\n', encoding='utf-8')
    print(root)


def validate(root):
    lib = read(root/'library.json')
    require(lib.get('schema_version') == 1, 'Unsupported library version')
    sources = {s['id']: s for s in lib['sources']}
    require(len(sources) == len(lib['sources']), 'Duplicate source ID')
    for s in sources.values():
        safe_id(s['id'])
        require(within(root, s['path']).is_file(), 'Missing source '+s['id'])
        require(sha(within(root, s['path'])) == s['sha256'], 'Source changed: '+s['id'])
    records = {r['id']: r for r in lib['records']}
    require(len(records) == len(lib['records']), 'Duplicate evidence ID')
    for r in records.values():
        safe_id(r['id'])
        require(r['status'] in STATES and r['scope'] in SCOPES, 'Invalid evidence status/scope')
        require(all(isinstance(r.get(k), str) and r[k].strip() for k in ('claim','area','limits')), 'Record needs claim, area and limits')
        require(isinstance(r.get('tags'), list), 'Record needs tags')
        require(bool(r.get('provenance')), 'Record needs provenance')
        for p in r['provenance']:
            require(p['source_id'] in sources and p.get('locator') and p.get('excerpt'), 'Incomplete source reference')
            require(p['excerpt_sha256'] == hashlib.sha256(p['excerpt'].encode()).hexdigest(), 'Excerpt hash mismatch')
        if r['status'] == 'confirmed':
            require(r.get('confirmed_at') and r.get('confirmed_by') == 'candidate', 'Confirmed means candidate confirmation, with date')
            date.fromisoformat(r['confirmed_at'])
        for old in r.get('supersedes', []):
            require(old in records and records[old]['status'] == 'superseded', 'Correction must retain superseded record')
    return lib


def source_add(root, path, ident, kind):
    lib = validate(root);safe_id(ident)
    require(not any(s['id'] == ident for s in lib['sources']), 'Source ID already exists')
    path = Path(path)
    target = root/'sources'/(ident+path.suffix.lower())
    require(not target.exists(), 'Source destination exists')
    shutil.copyfile(path, target)
    lib['sources'].append({'id': ident, 'path': str(target.relative_to(root)), 'sha256': sha(target), 'kind': kind, 'captured_at': now()})
    write(root/'library.json', lib)


def fact_add(root, path):
    lib = validate(root);record = read(path)
    require(not any(r['id'] == record['id'] for r in lib['records']), 'Evidence ID exists; create a new correction ID')
    for p in record.get('provenance', []):
        p['excerpt_sha256'] = hashlib.sha256(p['excerpt'].encode()).hexdigest()
    for old in record.get('supersedes', []):
        match = next((r for r in lib['records'] if r['id'] == old), None)
        require(match is not None, 'Unknown superseded ID')
        match['status'] = 'superseded'
    lib['records'].append(record)
    # Validate in a temporary sibling view before committing the real library.
    prior = read(root/'library.json')
    write(root/'library.json', lib)
    try:
        validate(root)
    except Exception:
        write(root/'library.json', prior)
        raise


def active(lib):
    return [r for r in lib['records'] if r['scope'] == 'career' and r['status'] != 'superseded']


def review_init(root, jobpath, output):
    lib = validate(root);job = read(jobpath)
    reqs = job['requirements']
    require(reqs and len({r['id'] for r in reqs}) == len(reqs), 'Need unique requirements')
    require(not Path(output).exists(), 'Review already exists')
    eligible = active(lib)
    review = {'library_digest': digest(lib), 'job_digest': digest(job), 'reviewed_by': '', 'complete': False,
              'area_review': {a: '' for a in sorted({r['area'] for r in eligible})},
              'considered_ids': [r['id'] for r in eligible],
              'assessments': [{'requirement_id': r['id'], 'assessment': 'unknown', 'evidence_ids': [], 'reason': ''} for r in reqs],
              'selected_ids': [], 'keyword_choices': [], 'bullets': [], 'page_budget': ''}
    write(output, review)
    # All records, including explicit gaps, are presented; no recency weighting.
    write(Path(output).with_name('evidence-brief.json'), {'requirements': reqs, 'career_records': eligible})


def check(root, jobpath, planpath):
    lib = validate(root);job = read(jobpath);plan = read(planpath)
    require(plan['library_digest'] == digest(lib), 'Library changed: regenerate and review selection')
    require(plan['job_digest'] == digest(job), 'Job changed: review selection again')
    require(plan.get('complete') and plan.get('reviewed_by'), 'Selection is not reviewed')
    all_records = {r['id']: r for r in active(lib)}
    require(set(plan['considered_ids']) == set(all_records), 'Must consider the whole career library')
    areas = {r['area'] for r in all_records.values()}
    require(set(plan['area_review']) == areas and all(plan['area_review'].values()), 'Explain every career area')
    selected = set(plan['selected_ids'])
    require(selected and all(i in all_records and all_records[i]['status'] in USABLE for i in selected), 'Select only usable career evidence')
    reqs = {r['id'] for r in job['requirements']}
    require(len(plan['assessments']) == len(reqs) and {a['requirement_id'] for a in plan['assessments']} == reqs, 'Assess every requirement once')
    for a in plan['assessments']:
        require(a['assessment'] in {'direct','transferable','gap','unknown'} and a['reason'], 'Assessment needs classification and reason')
        require(set(a['evidence_ids']) <= set(all_records), 'Assessment references unknown career record')
        if a['assessment'] in {'direct','transferable'}:
            require(a['evidence_ids'] and all(all_records[i]['status'] in USABLE for i in a['evidence_ids']), 'Positive assessment needs usable evidence')
    for k in plan['keyword_choices']:
        require(k['term'] and k['reason'] and k['decision'] in {'use','omit'}, 'Explain keyword decisions')
        if k['decision'] == 'use': require(k['evidence_ids'] and set(k['evidence_ids']) <= selected, 'Keyword has no selected support')
    for b in plan['bullets']:
        require(b['text'] and b['reason'] and b['alternatives_considered'] and b['requirement_ids'] and b['evidence_ids'], 'Bullet comparison incomplete')
        require(set(b['requirement_ids']) <= reqs and set(b['evidence_ids']) <= selected, 'Bullet references invalid selection')
        require(all(all_records[i]['area'] == b['area'] for i in b['evidence_ids']), 'Keep work under its actual employer/project area')
    return lib, job, plan


def audit(root, jobpath, planpath, claimpath):
    lib, job, plan = check(root, jobpath, planpath);claims = read(claimpath)
    require(claims['library_digest'] == digest(lib) and claims['plan_digest'] == digest(plan), 'Claim map stale')
    require(claims.get('semantic_review_complete') and claims.get('reviewed_by'), 'Human/agent semantic review required')
    require(claims.get('artifacts'), 'No artifacts')
    for a in claims['artifacts']:
        p = within(root, a['path']);textpath = within(root, a['text_path'])
        require(sha(p) == a['sha256'] and sha(textpath) == a['text_sha256'], 'Artifact or reading-copy changed')
        text = textpath.read_text(encoding='utf-8')
        require(a.get('claims') and a.get('all_factual_claims_mapped'), 'Missing claim coverage attestation')
        for c in a['claims']:
            require(c['text'] in text and c.get('limits_reviewed'), 'Claim not found or not reviewed')
            if c['kind'] == 'career':
                require(c['evidence_ids'] and set(c['evidence_ids']) <= set(plan['selected_ids']), 'Claim lacks selected career evidence')
            else:
                require(c['kind'] in {'employer','preference','application','proposal'} and c.get('source'), 'Other claim needs explicit source/type')
        if a['kind'] == 'resume':
            require(plan['bullets'] and plan['page_budget'], 'Resume requires compared bullets and page-budget review')
            require(all(b['text'] in text for b in plan['bullets']), 'Planned resume bullets missing from text')
    return {'passed': True, 'checked_at': now(), 'limit': 'Structural freshness/provenance checks, not proof of truth or exhaustive claim coverage.'}


def tracker_add(root, path):
    tracker = read(root/'tracker.json');app = read(path)
    for k in ('id','company_key','company','role','official_url','requisition'):
        require(isinstance(app.get(k), str) and app[k], 'Application needs '+k)
    safe_id(app['id'])
    require(not any(a['id'] == app['id'] or (a['company_key'] == app['company_key'] and a['requisition'] == app['requisition']) for a in tracker['applications']), 'Duplicate application/requisition')
    require(not any(a['official_url'] == app['official_url'] for a in tracker['applications']), 'Duplicate URL; reconcile instead')
    tracker['applications'].append(app);write(root/'tracker.json',tracker)


def event_add(root, path):
    tracker = read(root/'tracker.json');event = read(path)
    require(event['application_id'] in {a['id'] for a in tracker['applications']}, 'Unknown application')
    safe_id(event['id']);require(not any(e['id'] == event['id'] for e in tracker['events']), 'Duplicate event ID')
    require(event['kind'] in KINDS and event.get('evidence') and event.get('evidence_type') in {'candidate_report','browser_receipt','email','calendar','agent_observation'}, 'Event needs typed evidence')
    dt = datetime.fromisoformat(event['occurred_at']);require(dt.tzinfo is not None, 'Event needs timestamp with timezone')
    if event['kind'] == 'status':
        require(event['status'] in STATUSES, 'Unknown status')
        if event['status'] == 'submitted': require(event['evidence_type'] != 'agent_observation', 'Submission needs explicit receipt or candidate report')
    else:
        require(event.get('interview_id'), 'Interview event needs stable interview_id')
    tracker['events'].append(event);write(root/'tracker.json',tracker)


def report(root, days=None):
    require(days is None or days > 0, 'Day window must be positive')
    t = read(root/'tracker.json');events=sorted(t['events'],key=lambda e:datetime.fromisoformat(e['occurred_at']))
    submitted={};status={};interviews={}
    for event in events:
        aid=event['application_id']
        if event['kind']=='status':
            status[aid]=event['status']
            if event['status']=='submitted':submitted.setdefault(aid,event['occurred_at'])
        else:interviews[(aid,event['interview_id'])]=event['kind']
    if days is not None:
        start=datetime.now(timezone.utc)-timedelta(days=days)
        submitted={k:v for k,v in submitted.items() if datetime.fromisoformat(v)>=start}
    companies={a['id']:a['company_key'] for a in t['applications']}
    interviewed={companies[a] for (a,i),kind in interviews.items() if kind!='interview_cancelled' and (days is None or a in submitted)}
    result={'tracked_applications':len(t['applications']), 'submitted_applications':len(submitted), 'companies_with_scheduled_or_completed_interview':len(interviewed), 'interview_company_keys':sorted(interviewed), 'applications_per_interview_company':round(len(submitted)/len(interviewed),2) if interviewed else None, 'current_status_counts':{s:list(status.values()).count(s) for s in sorted(set(status.values()))}, 'cohort':f'applications submitted in trailing {days} days' if days else 'all recorded history', 'note':'Rounds at one company count once. Interview ratio is descriptive, not a forecast; recent applications have less response time. Status counts cover all history.'}
    return result


def context(root):
    lib=validate(root)
    return {'profile':read(root/'profile.json'), 'career_library_digest':digest(lib), 'career_records':active(lib), 'session':read(root/'session.json'), 'tracker_summary':report(root), 'instruction':'Review all career areas; profile preferences are not career claims. No private form facts included.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',type=Path,required=True)
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('init');sub.add_parser('validate');sub.add_parser('context')
    q=sub.add_parser('source-add');q.add_argument('file',type=Path);q.add_argument('--id',required=True);q.add_argument('--kind',default='candidate_note')
    q=sub.add_parser('fact-add');q.add_argument('file',type=Path)
    for name in ('review-init','review-check','audit'):
        q=sub.add_parser(name);q.add_argument('--job',required=True,type=Path);q.add_argument('--plan',required=True,type=Path)
        if name=='audit':q.add_argument('--claims',required=True,type=Path)
    for name in ('application-add','event-add'):
        q=sub.add_parser(name);q.add_argument('file',type=Path)
    q=sub.add_parser('report');q.add_argument('--days',type=int)
    q=sub.add_parser('export-csv');q.add_argument('file',type=Path)
    a=p.parse_args();root=a.workspace.resolve()
    if a.cmd=='init':init(root)
    elif a.cmd=='validate':validate(root);print('Evidence sources and records valid')
    elif a.cmd=='source-add':source_add(root,a.file,a.id,a.kind)
    elif a.cmd=='fact-add':fact_add(root,a.file)
    elif a.cmd=='review-init':review_init(root,a.job,a.plan)
    elif a.cmd=='review-check':check(root,a.job,a.plan);print('Selection valid')
    elif a.cmd=='audit':print(json.dumps(audit(root,a.job,a.plan,a.claims),indent=2))
    elif a.cmd=='application-add':tracker_add(root,a.file)
    elif a.cmd=='event-add':event_add(root,a.file)
    elif a.cmd=='report':print(json.dumps(report(root,a.days),indent=2))
    elif a.cmd=='context':print(json.dumps(context(root),indent=2))
    elif a.cmd=='export-csv':
        t=read(root/'tracker.json');latest={}
        for ev in sorted(t['events'],key=lambda e:datetime.fromisoformat(e['occurred_at'])):
            if ev['kind']=='status':latest[ev['application_id']]=ev['status']
        require(not a.file.exists(),'Export exists; choose a new path')
        with a.file.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=['id','company','role','requisition','official_url','status']);w.writeheader()
            for app in t['applications']:
                row={k:app[k] for k in w.fieldnames if k!='status'};row['status']=latest.get(app['id'],'unrecorded')
                # Prevent spreadsheet formula execution in exported untrusted text.
                w.writerow({k:("'"+v if v.startswith(('=','+','-','@')) else v) for k,v in row.items()})

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as exc:
        print('Error:',exc,file=sys.stderr);sys.exit(1)
