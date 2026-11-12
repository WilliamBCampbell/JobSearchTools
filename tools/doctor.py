#!/usr/bin/env python3
"""Read-only prerequisite check. Does not inspect secrets or personal configuration."""
import shutil, subprocess, sys
print('Python:',sys.version.split()[0],sys.executable)
missing=[]
for name in ('git','node','npm','npx','uv','uvx'):
    path=shutil.which(name)
    if not path:missing.append(name);print(name+': missing');continue
    try:
        result=subprocess.run([path,'--version'],capture_output=True,text=True,timeout=15,check=True)
        print(name+':',path,result.stdout.strip())
    except (OSError,subprocess.SubprocessError):print(name+': found, version check failed; inspect in your terminal')
print('Manual checks: Chrome + extension installed; AI client sees both MCP servers; workspace access works.')
sys.exit(1 if missing or sys.version_info<(3,10) else 0)
