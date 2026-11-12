# Search and match jobs

## Build searches from evidence

Read the full library and preferences first. Build several search families: core occupation, adjacent customer-facing work, industry experience and tool/skill combinations. For example, a fictional developer with implementation experience might search implementation consultant, integration engineer, technical consultant and customer engineer alongside software roles. Do not reuse these titles for every candidate.

Search broadly enough to find transferable work. Give travel a bonus when wanted, but do not require it unless the candidate does. Confirm frequency, location, territory and nights away separately. Remote does not automatically mean every state or country is eligible.

## Run JobSpy deliberately

Discover the installed MCP schema. Start with one board and a modest result count. Request full descriptions only for candidates worth reviewing. Save full results to the private research folder if the server supports it; previews can omit records. Retrieve details from the same search rather than repeating it.

A typical request, subject to the installed schema, is:

```json
{
  "site_name": ["indeed"],
  "search_term": "implementation consultant",
  "location": "United States",
  "is_remote": true,
  "results_wanted": 20,
  "hours_old": 168
}
```

Do not mistake this example for a universal query. Save requested parameters, timestamp, result count and board errors. When a board is rate-limited or returns unexpectedly sparse results, reduce frequency and stop repeated retries. Reuse cached results, try another permitted source or browse official careers pages. Do not claim the market has no jobs because one board failed.

## Verify each serious lead

Open the employer's official requisition. Confirm title, ID, full requirements, apply action, geography and current availability. Record verified_at and any redirect. A search snippet or aggregator salary estimate is not employer confirmation. If the official page is inaccessible, mark verification pending rather than inventing availability.

Normalize employer/brand aliases and strip tracking parameters for duplicate comparison, while retaining job-identifying parameters. Check company plus requisition, canonical URL, similar titles and existing unknown attempts. A different requisition can be a new role; a repost is not automatically new.

## Evaluate before shortlisting

Use a requirement matrix with direct, transferable, gap or unknown. Distinguish must-have from preferred criteria; retain the employer's wording and evidence. A missing degree may be acceptable where equivalent experience is explicitly offered. Do not turn unrelated work into healthcare, financial audit, platform-specific or management experience.

Prioritize legal/location eligibility and required qualifications, then actual work, ownership, results and candidate preferences. Compensation must distinguish base, OTE, bonus and equity, currency and period. Ask before pursuing a materially different package. An unusually low applicant count is not a reliable measure of competition or interview odds.

A shortlist entry includes company, role, requisition, official URL, verified time, compensation/source, location, travel/source, two or three concrete fit reasons with evidence IDs, material gaps, questions and recommendation. Record why rejected leads were rejected so the next search does not repeat them.

Do not fill a requested list size with poor matches. Explain which searches produced the best evidence-backed matches and what remains uncertain. Let the candidate select roles before uploading personal information.
