# Prepare an application package

Create a private folder named for company and requisition. Preserve original posting snapshots and submitted versions. Each package should contain:

```text
job.json                    requirements, official URL, verification time
posting.txt                 retained job description and source
selection.json              reviewed whole-career comparison
evidence-brief.json          all active career records
resume-plan notes           represented by selection.json bullets/page_budget
resume.txt / resume.pdf     matching reading and submission copies
cover-letter.txt / .pdf      when useful/requested
answers.json                labels, answers, status, provenance, approval
claim-map.json              claims and artifact hashes
audit.json                  validation output
review.json                 unresolved fields and candidate review
attempts/                   one record per attempt
receipt.json                confirmed result or unknown outcome
```

Use templates/job.json and run review-init. Complete the plan before drafting. A selection is not candidate approval; it is an evidence review. Save employer-specific salary, start date, terms, reference-contact choices and survey answers in the package. Unanswered optional fields can remain blank. Required unknowns need a question, not a guess.

Create answer records with key, exact label, required, options, answer, status, source and approval_scope. Status should distinguish confirmed, prepared_draft, needs_review and unanswered. A draft suggestion must never silently become a personal fact. Save newly confirmed reusable career facts through the library workflow.

## Render and verify

Use whatever document tooling the local environment supports: ReportLab, LibreOffice, a document skill or another installed renderer. Do not claim a PDF exists when only Markdown was written. Use a standard 10-12 point body font, ordinary margins and selectable text.

For example, with Poppler installed:

```bash
pdftotext resume.pdf resume-extracted.txt
pdftoppm -png -r 110 resume.pdf preview
```

Inspect every preview page for clipping, broken glyphs, awkward whitespace and hierarchy. Compare extracted text against the source. Verify names, dates, links and actual filenames. Do this again after revisions. Keep the chosen renderer/version in package notes so the next agent can reproduce the output.

Map every factual statement to evidence, including header/timeline facts. Non-career claims need a typed source: employer, preference, application or proposal. Use templates/claim-map.json. Compute digests with the utility's digest function; examples/run_demo.py demonstrates it. Hash the actual PDF and its reading copy. Do not set all_factual_claims_mapped until that review happened.

```bash
python3 tools/jobsearch.py --workspace /ABS/PRIVATE audit --job /ABS/job.json --plan /ABS/selection.json --claims /ABS/claim-map.json
```

Store the printed result as audit.json. The tool checks provenance structure and freshness, not the truth of the text or visual quality. Those checks remain the agent's responsibility.

## Review and handoff

Show the candidate the documents and a short explanation of the strongest matches and material gaps. Ask only unresolved questions. After approval, retain that exact version and upload it. If edited, replace the old browser attachment and verify the new filename. Record SHA-256 hashes for the files actually used, not every file in the folder.

For manual forms, provide official URL, copy-ready answers, full document paths, unresolved fields and prior-attempt status. A new tab does not authorize a duplicate application. Reconcile an earlier uncertain attempt first.
