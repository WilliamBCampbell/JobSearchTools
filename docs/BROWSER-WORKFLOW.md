# Fill applications in the candidate's Chrome browser

Use Playwright MCP with the Chrome extension described in INSTALLATION.md. This preserves the candidate's normal browser session. It is not an anti-detection promise. Sites can still reject a controlled session, even after a human completes verification.

## Connect and inspect

Ask the candidate to open the official application URL and allow/select the tab when required. List available tabs, confirm employer and requisition, then read the live page using the available snapshot tools. Do not assume a tab number or locator survived a reconnect. Multiple clients can own different tabs; stop duplicate controllers rather than repeatedly reconnecting them.

Use live labels/roles and current element references. Prefer filling text and choosing displayed options to executing arbitrary page scripts. Verify dependent fields after selecting country/state, and confirm dropdown choices actually persist. Avoid pressing Enter in a form because it can submit unexpectedly.

## Fill in sections

1. Contact and professional links from confirmed private facts.
2. Resume/cover letter from the approved package. Verify accepted filenames.
3. Work history and education. Correct parsing errors; include every required employer, accurate dates, formal titles and non-degree study labels. A certificate is not a diploma or bachelor's degree.
4. Screening questions. Match the full question, not a keyword. Explain adjacent experience without claiming direct expertise.
5. References and optional demographic questions only from confirmed answers and appropriate permission.
6. Final review: inspect all required fields, acknowledgments, text truncation and attachments.

Advance through clearly identified Next, Continue or Save controls. Inspect each new page. A final-action button visible from the beginning does not mean the form cannot be filled; it means the agent must avoid that action until authorized. Do not install network interceptors or disabled-button patches that leave the candidate unable to submit later.

The candidate enters passwords, verification codes, government identifiers and completes CAPTCHA. Do not save them in notes. Stop retries after repeated verification errors. Never rotate fingerprints, inject challenge tokens, bypass security controls or promise that a fresh tab will solve the problem.

## Review and submit

Default: leave the form ready for the candidate. Explicit approval to submit this application authorizes a single submission after unresolved material facts and acknowledgments are handled. Do not repeat approval questions for already approved documents. Do not generalize authorization from a different employer.

If the page contains a new certification, consent or contractual commitment, present it plainly and obtain the candidate's decision. Follow the active AI client's action rules as well. Do not falsely certify personal reading or acceptance.

After an authorized Submit action, inspect the actual result. Save a sanitized receipt or candidate report with the role and timestamp. An empty page, generic success URL or transport status alone is not proof. If the action might have reached the employer, mark unknown and reconcile before any retry.

## Manual fallback

If inputs do not respond, uploads fail, the session expires or verification repeatedly rejects the session, preserve the package and report exactly what is filled. The candidate can open a fresh ordinary tab, fill/review the copy-ready packet and submit. Disconnect or move the tab out of the controlled group if they prefer. This is normal manual use, not a security bypass.

Record per-employer behavior rather than treating every Lever, Ashby or ADP form as identical. Platform behavior changes. Never assume that an error means no receipt; an email may confirm a successful submission despite the page error.

## Evidence hygiene

Capture only the application result or relevant sanitized error. Avoid full network dumps, browser storage, cookies, headers and pages containing passwords, reference contacts or identity numbers. If a screenshot contains private details, crop/redact it or retain only a sanitized text note. Keep all evidence in the private workspace.
