# Troubleshooting

| Symptom | Check and next action |
|---|---|
| MCP server absent | Confirm executable path and arguments, fully restart the client, inspect its local server logs. Do not paste secrets from logs into chat. |
| Windows npx does not launch | Use the resolved npx.cmd path. If the client cannot spawn command files, use its documented cmd.exe /c launcher pattern and quote paths with spaces. Test in a terminal first. |
| “No clients connected” in extension | Trigger an actual Playwright tool action from the AI client. Merely opening extension status does not connect an MCP process. Confirm --extension and correct Chrome profile. |
| No approval dialog | Check the MCP process and extension permissions. A configured token can suppress the dialog; inspect client-owned tabs. Do not repeatedly rotate settings blindly. |
| Agent sees blank/wrong tab | Select the intended tab in the connection page or move it into the client's group. Ask the agent to list tabs again. |
| Connection lost after restart | Restart the relevant MCP server through the client, reconnect and inspect the page state. Do not assume entries persisted. |
| File upload fails | Confirm local file path, approved version and browser ownership. If a file:// route is used, check extension file-URL permission only as needed. Manual attachment is acceptable; verify the filename afterward. |
| Save/Next disabled | Inspect unfinished editors, required fields, dependent dropdowns, validation messages and upload completion. Ask the candidate to operate a stuck control. Never force-submit with page code. |
| JobSpy fewer/no results | Read error/warning fields and board logs; check parameters, reduce frequency and use cached results or another source. Empty preview is not proof of no jobs. |
| CAPTCHA fails after human solves | Stop repeated attempts, record uncertainty and reconcile receipt. Use a candidate-controlled manual form later if no submission occurred. No bypass tooling. |
| Claim audit becomes stale | A source, library, job, plan or artifact changed. Re-review and regenerate the relevant hashes; do not just replace digests to silence the check. |
| Earlier application may have submitted | Read the account/receipt/email evidence or ask the candidate. Mark unknown until resolved; never send another application automatically. |

Do not close the candidate's browser, clear cookies, reset their profile or kill unrelated processes as routine troubleshooting. Explain the narrow fix and preserve the prepared package. Escalate to manual work when further automation would repeat the same failure.
