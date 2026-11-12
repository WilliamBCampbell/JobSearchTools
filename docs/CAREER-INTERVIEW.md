# AI-led career interview

The goal is a detailed, accurate account of the candidate's entire professional career that future agents can use without remembering this conversation. The AI leads the interview. It asks, listens, follows up and checks what it understood. It does not read a questionnaire aloud without responding to the answers.

## Set up a voice session

The candidate can use GPT/Dot, another AI voice interface, or a text chat. Give the interviewer the resume and prompts/CAREER-INTERVIEW.md. Remove private contact details if they are unnecessary. Tell it how much time is available and which roles have already been covered.

Suggested opening: “I want you to interview me about my whole career. Use my resume as a starting point, not as a complete record. Ask one question at a time and probe my answers as a hiring manager would. At the end, give me detailed notes I can review and save in my career library.”

Voice clients differ in access, recording and export. If there is no transcript export, ask for structured notes at the end of each role and copy them to a dated text file. Preserve the distinction between verbatim transcript, candidate-reviewed notes and an unreviewed AI summary. Do not invent exact quotations from a summary.

## Interview pacing

Begin with a five-minute career map. Confirm every employer, role, promotion, contract, significant project and education period on the resume. Ask what is missing. Agree on the order and create a coverage checklist. Start with the role the candidate remembers best if useful, but return to every role before declaring the interview complete.

Work in 30-60 minute sessions, or shorter when preferred. A long career may need several sessions. These are suggestions, not quotas. Ask one substantive question at a time, allow the person to finish, and use follow-ups based on the answer. Do not repeatedly ask questions already answered. At a pause, recap the role and save unanswered questions so the next session can continue.

## Questions for every position

### Establish the role

- What did this company do, who used its products or services, and what business problems did your team address?
- What was your formal title? Did your responsibilities or title change? What were the dates, and which dates are approximate?
- Where did you sit in the organization? Who did you work with, and who made final decisions?
- What were you accountable for personally? What was owned by teammates, vendors or managers?
- What did an ordinary week look like? What work was important but never appeared on your resume?

### Examine actual work

Ask for a project or responsibility, then follow the example through rather than accepting a list of technologies:

- What was happening before you got involved? Who was affected?
- What did success need to look like? Who agreed on that?
- Walk me through what you personally did, from the first conversation to the result.
- What was the hardest decision? Which alternative did you reject, and why?
- What constraints mattered: budget, time, regulation, staffing, data quality or existing systems?
- How did you test, validate or check the result? Who accepted it?
- What happened after delivery? Did you remain responsible for support or improvements?

If the candidate says “we,” ask “Which part was yours?” If they say “improved,” ask “What changed, and how did you know?” If they name a technology, ask what they built, configured, maintained or troubleshot with it. Do not turn familiarity into expertise.

### Ask interview-grade follow-ups

Choose the questions that fit the role and answers; do not force software terminology onto other careers.

- Tell me about a difficult problem where your first approach did not work. What evidence changed your mind?
- Describe a disagreement about a requirement or priority. How was it resolved, and who made the decision?
- Tell me about a customer or colleague who was unhappy with the outcome. What did you do, and what actually happened afterward?
- What mistake did you make? How did you identify it, communicate it and prevent a repeat?
- What did you deliver with incomplete information? Which assumptions did you test?
- How did you balance competing deadlines? Give a particular example rather than a general philosophy.
- What did you teach someone else? How did you know they could do the work afterward?
- What process did you improve? What remained manual or difficult?
- Describe a time you had to learn a new business domain. How did that knowledge change your decisions?
- What are you proud of that your resume currently fails to explain?

For customer-facing work, probe discovery, demos, scoping, promised deliverables, configuration, onboarding, training, go-live and ongoing ownership. Distinguish formal contract authority from participation in estimates or acceptance criteria.

For technical work, probe architecture, data flow, dependencies, production troubleshooting, testing, release decisions, security boundaries and operational responsibility. Ask for concrete code/configuration actions without requesting proprietary code or secrets.

For leadership, distinguish mentoring, project coordination, technical leadership and direct people management. Ask about team size, decisions, planning, feedback and accountability. A team lead is not automatically a hiring manager or budget owner.

For sales or commercial work, separate prospecting, technical support, demos, closing authority, quota and attributed revenue. For operations, explore volumes, reliability, quality, customer impact and handoffs. Adapt to the candidate's occupation.

### Establish outcomes without inventing metrics

Ask for before/after measurements, approximate scale, timeframe and how the candidate knows the result. “I remember roughly half as many calls” must not become an audited 50% performance claim. Label self-reported estimates and retain the original language.

When no number exists, capture the concrete result: a repeated meeting became unnecessary, staff completed the task independently, a customer launched, an error stopped recurring, or a manual step was removed. Do not pressure the candidate to supply a percentage. Ask what did not improve as well.

### Close each role

Read back a short summary of responsibilities, two or more useful examples when available, tools/depth, outcomes and boundaries. Ask:

- What did I misunderstand or leave out?
- Which statements are estimates or uncertain memories?
- Is anything confidential that should be anonymized in applications?
- Why did you leave, and how would you state that accurately?
- Does the resume describe this role correctly?

Do not call an answer confirmed unless the candidate actually confirms it. Preserve unresolved contradictions for follow-up.

## Beyond the resume

After covering every role, ask about education and unfinished study, certificates versus degrees, volunteer work, hobbies with transferable skills, independent projects, contract work, writing, talks and professional development. Let the candidate decide whether side work should appear as a project or employment; complete-history forms may still require disclosure.

Ask what they want next and why. Probe the work they enjoy, the environment where they do well, travel preferences, location and compensation tradeoffs. Keep preferences distinct from evidence of skill.

## Output for the local agent

Produce these sections after each session:

1. Coverage checklist: covered roles, partial roles, untouched roles and next questions.
2. Timeline: employer, formal title, responsibilities, dates and uncertainty.
3. Detailed story cards: context/problem, personal action, collaborators/authority, alternatives/tradeoffs, result, measurement basis, tools/depth, lesson and confidentiality limits.
4. Candidate confirmations and corrections, with transcript timestamps or message references when available.
5. Unresolved questions and contradictions. Do not choose the more impressive version.
6. Potential skill tags and suitable role families, clearly labeled as analysis rather than candidate facts.
7. Preferences and sensitive form answers in separate sections.

Save the raw transcript or notes as a source. The local agent splits them into atomic records following CAREER-LIBRARY.md, with source excerpts, status, scope and limits. The candidate reviews the overview before the library is used in an application.

## Completion check

Every resume role has been visited, each important claim has a source, personal versus team ownership is clear, approximate numbers remain approximate, and gaps are explicit. The interviewer has not substituted a polished fictional story for an incomplete memory. A second agent should be able to tell what is known, how it is known and what still needs asking.
