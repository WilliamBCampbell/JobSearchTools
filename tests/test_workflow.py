import copy,importlib.util,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'examples'))
import jobsearch as j
from run_demo import build

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'private'
        self.job,self.plan,self.claims=build(self.root)
    def tearDown(self):self.tmp.cleanup()
    def test_demo(self):self.assertTrue(j.audit(self.root,self.job,self.plan,self.claims)['passed'])
    def test_source_tampering(self):
        (self.root/'sources/demo-interview.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError,'Source changed'):j.validate(self.root)
    def test_stale_plan(self):
        lib=j.read(self.root/'library.json');lib['records'][0]['limits']+=' Extra boundary.';j.write(self.root/'library.json',lib)
        with self.assertRaisesRegex(ValueError,'Library changed'):j.check(self.root,self.job,self.plan)
    def test_draft_cannot_be_selected(self):
        lib=j.read(self.root/'library.json');lib['records'][0]['status']='draft';j.write(self.root/'library.json',lib)
        plan=j.read(self.plan);plan['library_digest']=j.digest(lib);j.write(self.plan,plan)
        with self.assertRaisesRegex(ValueError,'usable career'):j.check(self.root,self.job,self.plan)
    def test_all_areas_required(self):
        plan=j.read(self.plan);plan['area_review']={};j.write(self.plan,plan)
        with self.assertRaisesRegex(ValueError,'every career area'):j.check(self.root,self.job,self.plan)
    def test_changed_artifact(self):
        (self.job.parent/'resume.txt').write_text('Unsupported claim')
        with self.assertRaisesRegex(ValueError,'changed'):j.audit(self.root,self.job,self.plan,self.claims)
    def test_correction_preserves_history(self):
        fact=j.read(ROOT/'examples/demo-fact.json');fact['id']='example.imports-correction';fact['supersedes']=['example.imports'];fact['claim']='Corrected fictional fact';p=self.root/'fact.json';j.write(p,fact)
        j.fact_add(self.root,p);lib=j.validate(self.root)
        self.assertEqual(lib['records'][0]['status'],'superseded');self.assertEqual(len(lib['records']),2)
    def test_invalid_fact_rolls_back(self):
        before=j.read(self.root/'library.json');fact=j.read(ROOT/'examples/demo-fact.json');fact['id']='bad';fact['status']='confirmed';fact['confirmed_by']=None;p=self.root/'bad.json';j.write(p,fact)
        with self.assertRaises(ValueError):j.fact_add(self.root,p)
        self.assertEqual(before,j.read(self.root/'library.json'))
    def test_paths_cannot_escape(self):
        with self.assertRaises(ValueError):j.within(self.root,'../outside')
    def test_initialization_never_overwrites(self):
        with self.assertRaises(ValueError):j.init(self.root)
    def add_app(self,ident='example-123',req='123'):
        p=self.root/(ident+'.json');j.write(p,{'id':ident,'company_key':'example','company':'Example','role':'Role','requisition':req,'official_url':'https://example.invalid/'+req});j.tracker_add(self.root,p);return p
    def event(self,ident,kind='status',status='submitted',app='example-123',interview='round1'):
        p=self.root/(ident+'.json');j.write(p,{'id':ident,'application_id':app,'kind':kind,'status':status,'interview_id':interview,'occurred_at':j.now(),'evidence_type':'candidate_report','evidence':'Fictional candidate report'});j.event_add(self.root,p)
    def test_duplicate_application(self):
        p=self.add_app()
        with self.assertRaisesRegex(ValueError,'Duplicate'):j.tracker_add(self.root,p)
    def test_interview_rounds_count_once_after_rejection(self):
        self.add_app();self.event('sent');self.event('first','interview_scheduled');self.event('done','interview_completed');self.event('second','interview_scheduled',interview='round2');self.event('reject',status='rejected')
        r=j.report(self.root);self.assertEqual(r['submitted_applications'],1);self.assertEqual(r['companies_with_scheduled_or_completed_interview'],1);self.assertEqual(r['current_status_counts'],{'rejected':1})
    def test_cancelled_only_not_counted(self):
        self.add_app();self.event('sent');self.event('first','interview_scheduled');self.event('cancel','interview_cancelled')
        self.assertEqual(j.report(self.root)['companies_with_scheduled_or_completed_interview'],0)
    def test_private_facts_not_in_context(self):
        lib=j.read(self.root/'library.json');r=copy.deepcopy(lib['records'][0]);r.update(id='private.fact',scope='private',claim='PRIVATE SENTINEL');lib['records'].append(r);j.write(self.root/'library.json',lib)
        self.assertNotIn('PRIVATE SENTINEL',json.dumps(j.context(self.root)))
    def test_unknown_is_not_submitted(self):
        self.add_app();self.event('uncertain',status='unknown');self.assertEqual(j.report(self.root)['submitted_applications'],0)


class ConfigTests(unittest.TestCase):
    def test_snippets_escape_paths_and_parse(self):
        import os,subprocess
        with tempfile.TemporaryDirectory(prefix='paths with spaces ') as directory:
            root=Path(directory);workspace=root/'private';j.init(workspace)
            fakebin=root/'bin';fakebin.mkdir()
            # Config generation locates commands but does not execute them.
            for name in ('uvx','npx'):
                f=fakebin/(name+'.exe' if os.name=='nt' else name);f.write_text('fixture');f.chmod(0o755)
            env=dict(os.environ);env['PATH']=str(fakebin)+os.pathsep+env.get('PATH','')
            out=root/'config'
            subprocess.run([sys.executable,str(ROOT/'tools/mcp_config.py'),'--workspace',str(workspace),'--output',str(out)],env=env,check=True,capture_output=True)
            config=j.read(out/'claude-desktop.json')
            self.assertEqual(config['mcpServers']['job-application-browser']['args'][-1],'--extension')
            self.assertNotIn('TOKEN',json.dumps(config))
            if sys.version_info >= (3,11):
                import tomllib
                data=tomllib.loads((out/'codex.toml').read_text())
                self.assertEqual(data['mcp_servers']['jobspy']['args'],['mcp-jobspy@latest'])
    def test_local_markdown_links_exist(self):
        import re
        for file in ROOT.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
                if '://' in target or target.startswith('#'):continue
                self.assertTrue((file.parent/target.split('#')[0]).exists(),str(file)+': '+target)

if __name__=='__main__':unittest.main()
