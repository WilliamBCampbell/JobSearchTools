# JobSearchTools

A local workflow for an AI assistant and a job seeker to find suitable jobs, build truthful application materials, fill forms, track outcomes and prepare for interviews.

The assistant does the research and preparation. The job seeker supplies missing facts, reviews the materials and normally submits the application. Career evidence lives in files, so a new chat or a different AI can resume without relying on conversation memory.

This repository contains instructions, prompts, templates and a dependency-free Python utility. It is not an unattended application bot or a hosted service. It does not guarantee job-board access, CAPTCHA completion, interviews or an ATS score. Browser filling needs a local MCP-capable AI client; a plain web chat without local tools can only help with the writing.

## Start here

You need Git, Python 3.10+, a current Node.js LTS release with npm/npx, uv/uvx, Google Chrome, and an AI client with local file and MCP access. Install these from their official sites. See [installation](docs/INSTALLATION.md) for client-specific setup and verification.

```bash
git clone https://github.com/WilliamBCampbell/JobSearchTools.git
cd JobSearchTools
python3 tools/jobsearch.py --workspace "$HOME/job-search-private" init
python3 -m unittest discover -s tests -v
```

On Windows, use `py -3` in place of `python3` and a full workspace path such as `C:\Users\YourName\job-search-private`. The Python utility works across platforms. Shell examples marked Bash need translation in PowerShell.

Keep that workspace **outside this repository**. It will contain your resumes, contact information, evidence, receipts and private application answers. No personal library is shipped here.

Then:

1. [Connect JobSpy MCP and Playwright MCP](docs/INSTALLATION.md). Test each connection before searching or applying.
2. Give the AI [AGENTS.md](AGENTS.md), [the workflow](docs/WORKFLOW.md), and your workspace path. Clients do not all load AGENTS.md automatically.
3. Run the [onboarding conversation](docs/ONBOARDING.md), including an [AI-led career interview](docs/CAREER-INTERVIEW.md). Use voice with GPT/Dot or another AI if you prefer. The interviewer probes every resume position and produces reviewable notes for a fresh [career evidence library](docs/CAREER-LIBRARY.md).
4. Ask for a small [verified shortlist](docs/SEARCH-AND-MATCHING.md). Match skills and experience first; treat travel according to your preferences.
5. Select a role. Follow [application preparation](docs/APPLICATION-PACKAGES.md) and [browser filling](docs/BROWSER-WORKFLOW.md).
6. Save a receipt or unresolved outcome. Maintain [tracking and interview records](docs/TRACKING.md), then use [interview preparation](docs/INTERVIEWS.md).

Copy this into a new local AI chat, replacing the paths:

> Read `/absolute/path/JobSearchTools/AGENTS.md` and `/absolute/path/JobSearchTools/docs/WORKFLOW.md`. My private workspace is `/absolute/path/job-search-private`. Start with installation verification and onboarding. Read the full career library before matching jobs or drafting. Ask for facts you cannot establish. Do not submit applications or send messages without my authorization. Save progress so another chat can continue.

## What is included

| Component | Purpose |
|---|---|
| `tools/jobsearch.py` | Create a workspace, ingest sources and evidence, check selection/claim maps, keep application events, report counts |
| `tools/mcp_config.py` | Generate local Claude Desktop JSON and Codex TOML snippets with absolute executable paths |
| `tools/doctor.py` | Check local prerequisites without changing client settings |
| `templates/` | Candidate evidence, job requirements, application, receipt, claims and interview templates |
| `examples/` | Fictional worked example; never use it as a real candidate's experience |
| `prompts/` | Onboard, search, apply, reconcile, interview and handoff instructions |
| `docs/` | The full operating process, writing standards and troubleshooting |
| `tests/` | Offline checks for evidence freshness, corrections, duplicate records and interview counts |

The Python tool performs structural checks. An agent must still read the underlying evidence and decide whether a claim is supported. A passing audit cannot prove that prose is truthful or that every factual claim was included in its map.

## Privacy and authorization

Keep credentials in the client or operating-system credential store. Never put passwords, browser cookies, extension tokens, verification codes or government identifiers in this repository, source notes, screenshots or handoffs. Store sensitive optional application answers separately from general career evidence.

Preparation approval is not submission approval. A failed page after clicking Submit can still mean an application was received. Mark the outcome unknown and reconcile before retrying. Use normal employer workflows and human verification; do not add stealth plugins or CAPTCHA bypasses.

## Maintenance

The integration instructions were checked against upstream documentation on November 12, 2026. Verify current versions during installation, then record and pin the versions that pass your smoke tests. See [sources and compatibility](docs/SOURCES.md).

Run `python3 -m unittest discover -s tests -v` after changing the utility. Use one writer per private workspace. Back up the private workspace separately and retain submitted document versions. This toolkit does not migrate or modify any existing job-search application's database.
