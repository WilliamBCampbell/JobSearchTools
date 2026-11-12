# Application and interview tracking

The default tracker is private tracker.json. It stores application identities and append-only events. CSV exports are views for a spreadsheet, not a second competing authority. If integrating an existing tracker/database, choose one authoritative store and document the mapping before changing it.

## Identity and statuses

Use a stable application ID, normalized company_key, company display name, role, official URL and requisition. For a job without a requisition, use a stable canonical identifier and note its basis. Manually reconcile aliases, reposts and redirects; exact matching alone will not catch them all.

Statuses: shortlisted, prepared, ready, manual_required, unknown, submitted, rejected, withdrawn, closed, not_pursuing, offer. An interview is a separate event so rejection does not erase interview history. The current status is the latest timestamped status event.

```bash
python3 tools/jobsearch.py --workspace /ABS/PRIVATE application-add /ABS/application.json
python3 tools/jobsearch.py --workspace /ABS/PRIVATE event-add /ABS/event.json
python3 tools/jobsearch.py --workspace /ABS/PRIVATE report
python3 tools/jobsearch.py --workspace /ABS/PRIVATE report --days 7
python3 tools/jobsearch.py --workspace /ABS/PRIVATE export-csv /ABS/new-export.csv
```

Every event needs an ID, application_id, occurred_at with timezone, kind, evidence and evidence_type. Use templates/event.json. Evidence types distinguish candidate_report, browser_receipt, email, calendar and agent_observation. A submitted event cannot use agent_observation: use an actual receipt or explicit candidate report. Record the real event date when known, not the date an agent finally noticed it. Unknown dates should stay in notes until resolved, rather than being invented for the tool.

Interview events need a stable interview_id. Use the same ID to cancel or complete that appointment. Use another ID for a later round. A scheduled future appointment counts as a company inviting the candidate to interview; cancelled-only appointments do not count in the current summary. Multiple applications/rounds at the same normalized company count once.

The report's application/interview ratio is submitted applications divided by distinct companies with a scheduled or completed interview. The seven-day report uses the submission cohort, not interviews merely occurring that week. Always state the window and denominator. Recent cohorts have had less time to respond; this is not a prediction of how many more applications are needed.

## Receipts and reconciliation

A receipt records employer/requisition, outcome, source type, observation time, actual document hashes and evidence location. Preserve candidate reports as candidate reports. If a page failed after Submit, set unknown. Before retrying, inspect the candidate's account and authorized email sources or ask whether they received confirmation.

An interview invitation can arrive without a stored submission receipt. Record the interview event, then reconcile the missing submission history; do not fabricate a submission date. A rejection also does not establish when the application was sent.

## Email and calendar updates

Only use connected accounts with user authorization. Search by employer, recruiter domains, requisitions and date range. Read enough context to separate receipts, rejections, interviews, marketing and unrelated jobs. Match to existing application IDs. Save a message/event identifier and a minimal factual summary, not full mailboxes or credentials. Do not send replies or accept calendar invitations unless requested.

Use calendar evidence to identify scheduled interviews and email to confirm roles and changes. Preserve cancelled/rescheduled events. If the company or requisition is ambiguous, mark it for candidate review. Never infer rejection from silence or an expired job posting.

## Handoff and backups

Use one writer per workspace. Back up tracker.json and the library before bulk reconciliation. Save session.json after each application with current step, pending questions and the next action. Keep earlier receipts and submitted document hashes. Corrections should be new events with reasons, not quiet deletion of history. The utility does not implement multi-user locking or automated email synchronization.
