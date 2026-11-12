# Onboarding a new candidate

Start with the person, not a job advertisement. A career library built only while answering application questions will overrepresent the most recent conversations.

## Collect the starting materials

Ask the candidate to place original resumes, employment timelines, project notes, portfolio links, recommendations, writing samples and past application records in the private workspace. Accept incomplete records. Do not request confidential customer data, employer source code or documents they cannot share.

Inventory files before extracting them. Record which are originals, candidate-authored notes, AI drafts, or unknown. Extract PDF/DOCX text with available local tools; inspect the original when formatting or tables affect meaning. For scanned PDFs, use OCR and mark the extraction uncertain until checked. A directory full of duplicate resumes is one set of claims, not independent corroboration.

Ask about:

- Preferred/full name, professional contact links and location.
- Roles they want, work they enjoy, work they want less of, and acceptable adjacent roles.
- Remote/hybrid/onsite requirements, relocation, work authorization, coverage hours and on-call expectations.
- Travel interest, typical nights away they would accept and hard limits. Travel is a preference, not always a requirement.
- Base compensation versus bonus, commission, equity and OTE. Identify flexibility for a career transition without assuming a universal salary floor.
- Submission preference, recruiting contact preferences and any companies/roles to exclude.

Keep sensitive disclosures in private/form-facts.json only when needed and confirmed. Do not infer demographics, disability, veteran status, legal history or family relationships.

## Conduct the career interview

Recommend a voice conversation with GPT/Dot or another voice-capable AI if that is easier than typing. A voice session does not need local MCP access. The candidate can provide a redacted resume, use prompts/CAREER-INTERVIEW.md, and save the resulting transcript or structured notes locally afterward. Do not imply every voice client can read this workspace or export a transcript automatically.

Follow [CAREER-INTERVIEW.md](CAREER-INTERVIEW.md). It is an AI-led interview covering every position, with follow-up questions at the depth of a hiring interview. Offer several shorter sessions if the candidate prefers. Never silently record audio or upload documents to an additional service. Use the voice tool's ordinary controls and the candidate's chosen sharing settings.

The interview ends with a reviewable record, not an automatically confirmed biography. The local agent imports the transcript as a source, checks transcription ambiguities, proposes atomic facts and asks the candidate to confirm corrections. An interviewer-generated summary is still a draft unless the person confirms it.

## Complete the first library

Read CAREER-LIBRARY.md. Enter all employers and projects before selecting favorite stories. Include education, certifications, technical depth, leadership, customer delivery, failures, lessons, side projects and explicit gaps. Mark dates approximate when necessary. The toolkit's fictional examples are for learning the format only.

Show the candidate:

1. Employment and education timeline, including formal titles and promotions.
2. An employer-by-employer overview with strongest evidence and unresolved details.
3. A skill matrix separating implemented, maintained, observed, studied and not used.
4. A story bank with problem, personal action, result and source IDs.
5. Preferences and constraints, separately from qualifications.

Correct the record before setting profile.json's onboarding_complete to true. Run validate. Save unresolved questions in session.json. Onboarding can be complete with clearly recorded unknowns; it does not require manufacturing certainty.

## Keep interviewing during the search

New application questions often reveal useful experience. Ask the question, capture the answer, clarify scope, update the library and regenerate affected selection plans. After every few applications, review whether an employer or career period has been neglected. Do not reward a story merely because it was discussed yesterday.
