# Build and maintain a career evidence library

The library is a collection of small claims with sources and boundaries. It is not a master resume. Resumes select from it; they do not become its authority merely because they were submitted.

## Workspace and records

`library.json` has schema_version, sources and records. `sources/` holds immutable copies of original files or dated candidate notes. Use tools/jobsearch.py to register sources and add records. The complete field format is in templates/fact.json and examples/demo-fact.json.

Each record needs:

- A stable ID, such as employer.project.delivery, and an area identifying the actual employer or personal project.
- One narrow claim, a list of skill/topic tags and a status.
- Scope: career, preference, application or private. Only career records enter general evidence briefs.
- Limits: what the source does not establish, uncertain dates/metrics, team versus personal ownership, confidentiality restrictions.
- Provenance: source ID, a location such as page/paragraph/timestamp, and an exact source excerpt. The tool hashes the excerpt and original file.
- Candidate confirmation date/identity when status is confirmed. Do not backdate or invent confirmation.
- Supersedes IDs for corrections, while retaining the old record as superseded.

Statuses:

| Status | Use |
|---|---|
| confirmed | The candidate explicitly confirmed the fact within its stated scope |
| source_supported | An original record supports it; not independently verified and not necessarily candidate-confirmed |
| draft | Generated suggestion or extraction awaiting review; cannot support final career claims |
| unknown | Not established; ask if material, do not call it a gap |
| gap | Candidate explicitly lacks that experience; never use as positive evidence |
| superseded | Historical claim replaced by a correction; never use in new materials |

For a proposed approach (“I would…”), label it as a proposal in the answer and claim map. Do not convert it into a past achievement. Applications cannot establish new facts about the candidate by repetition.

## First import

1. Initialize an empty workspace with the README command.
2. Inventory the candidate's original files and interview notes. Read every career area.
3. Copy each source using `source-add`. A text extraction should be registered separately with a pointer to the original; OCR errors need review.
4. Draft atomic facts using templates/fact.json. Confirm title/date corrections, ownership, metrics and skill depth. Preserve supporting excerpts.
5. Add reviewed facts with `fact-add`, then run `validate`.
6. Run `context` to get a whole-career reading view and ask the candidate to review it. That command excludes private/application records.

```bash
python3 tools/jobsearch.py --workspace /ABS/PRIVATE source-add /ABS/notes.txt --id interview-01 --kind candidate_interview
python3 tools/jobsearch.py --workspace /ABS/PRIVATE fact-add /ABS/fact.json
python3 tools/jobsearch.py --workspace /ABS/PRIVATE validate
python3 tools/jobsearch.py --workspace /ABS/PRIVATE context
```

Do not import the fictional example into a real candidate library. Use the same structure with their own sources.

## Add facts during applications

When a screening question reveals new information, save the candidate's answer with the question and date in a source note. Ask follow-ups only when needed: “Did you implement it, maintain it, or observe it?”; “Was that measured?”; “Was it your responsibility through launch?”

Add a new fact. If it corrects an old fact, set supersedes to that ID. The helper marks the old record superseded without deleting it. A correction applies only to the stated scope: one MongoDB project does not establish broad NoSQL expertise. Never overwrite a source file to make an old claim appear supported.

Run validation. Any library change invalidates existing selection digests, even if unrelated; regenerate the brief and re-review the active package. Do not rewrite already submitted materials. Record a correction for future use.

## Requirements-first selection

Create a job file from templates/job.json using the actual official posting. Save excerpts and source URL/time. Then:

```bash
python3 tools/jobsearch.py --workspace /ABS/PRIVATE review-init --job /ABS/job.json --plan /ABS/selection.json
```

The resulting evidence-brief.json contains all active career records, including gaps and unknowns. Complete every area_review, every requirement assessment and the selected IDs. Compare relevant examples within each employer. Do not use timestamps, frequency of mentions or old tailored resumes as ranking signals.

Classify requirements as direct, transferable, gap or unknown. Explain each classification and cite evidence IDs. A positive match cannot use a draft or gap. Document truthful keyword use and omitted terms. For each resume bullet record exact text, correct area, requirement/evidence IDs, alternatives considered and why it earns space. Explain the page budget and secondary evidence added.

```bash
python3 tools/jobsearch.py --workspace /ABS/PRIVATE review-check --job /ABS/job.json --plan /ABS/selection.json
```

Before delivery, map factual claims to selected career records or explicitly typed external/preferences/application sources. Record exact artifact and plain-text-copy hashes and run audit. See examples/run_demo.py for an executable example of these steps.

## Limits and privacy

Hashes detect changed files, not lies. The validator cannot prove that a PDF excerpt is accurate, a reviewer read every source, or a selected claim is semantically supported. A named agent/human must perform that review. Structural checks are not an ATS score or an automated hiring decision.

General context must not include passwords, reference contact details, demographics, medical information or private application commitments. Keep confidential employer/customer names anonymized when requested. Store only the minimum information necessary, and back up the private workspace under the candidate's control. This utility assumes one writer; do not run simultaneous edits against the same library.
