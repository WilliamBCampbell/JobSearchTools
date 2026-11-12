# Sources and compatibility

Integration guidance checked November 12, 2026 against primary sources:

- [JobSpy repository](https://github.com/speedyapply/JobSpy) and [upstream MCP setup/tools](https://github.com/speedyapply/JobSpy/tree/main/mcp).
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp), [extension documentation](https://github.com/microsoft/playwright/blob/main/packages/extension/README.md) and [Chrome extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm).
- [OpenAI Codex MCP configuration](https://developers.openai.com/codex/mcp/).
- [MCP local-server setup for Claude Desktop](https://modelcontextprotocol.io/docs/develop/connect-local-servers) and [Anthropic local MCP guidance](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).
- [uv installation](https://docs.astral.sh/uv/getting-started/installation/).

The toolkit's evidence, writing, application and tracking procedures are distilled from a human-reviewed job-search workflow. Private career records, credentials, applicant details and employer-specific commitments are not included. Generic examples are fictional.

Local automated tests cover the Python utilities and fictional end-to-end evidence flow. Live job-board availability, all client/OS combinations, employer submissions and Chrome extension interactions are not guaranteed by those tests. Installations should record tested versions and perform their own smoke checks. The repository does not vendor upstream server code or lock their dependency trees.

Use the client's current documentation when menus, tool schemas or extension behavior change. Any agent with suitable local file/command and MCP capabilities can follow the process; clients without those capabilities need the user to run the missing steps. Voice interviews can happen separately and be imported afterward.
