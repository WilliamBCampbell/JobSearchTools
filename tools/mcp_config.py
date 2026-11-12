#!/usr/bin/env python3
"""Generate snippets only. Never overwrite a client's settings or embed tokens."""
import argparse,json,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--workspace',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
p.add_argument('--jobspy-version',default='latest');p.add_argument('--playwright-version',default='latest')
a=p.parse_args();repo=Path(__file__).resolve().parents[1]
commands={k:shutil.which(k) for k in ('uvx','npx')}
if not all(commands.values()):p.error('Install uv/uvx and Node/npm/npx first')
if not (a.workspace/'library.json').is_file():p.error('Initialize the workspace first')
servers={'jobspy':{'command':commands['uvx'],'args':['mcp-jobspy@'+a.jobspy_version]},'job-application-browser':{'command':commands['npx'],'args':['-y','@playwright/mcp@'+a.playwright_version,'--extension']}}
files=dict(servers);files['filesystem']={'command':commands['npx'],'args':['-y','@modelcontextprotocol/server-filesystem',str(a.workspace.resolve()),str(repo)]}
a.output.mkdir(parents=True,exist_ok=True)
for name in ('claude-desktop.json','codex.toml'):
    if (a.output/name).exists():p.error('Output exists; choose a new directory')
(a.output/'claude-desktop.json').write_text(json.dumps({'mcpServers':files},indent=2)+'\n')
# JSON strings/arrays are also valid TOML basic strings/arrays for these values.
(a.output/'codex.toml').write_text('\n'.join('[mcp_servers.'+name+']\ncommand = '+json.dumps(s['command'])+'\nargs = '+json.dumps(s['args'])+'\n' for name,s in servers.items()))
print('Created snippets in',a.output,'; merge them manually. No client settings changed.')
