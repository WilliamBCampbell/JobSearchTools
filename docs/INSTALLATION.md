# Installation and connection checks

## Prerequisites

Install [Python](https://www.python.org/downloads/) 3.10 or later, [Git](https://git-scm.com/downloads), a current [Node.js LTS](https://nodejs.org/en/download), [uv](https://docs.astral.sh/uv/getting-started/installation/) and Google Chrome. Use an AI client that supports local MCP servers. A subscription or model account is separate from this repository.

Run from the repository:

```bash
python3 tools/doctor.py
python3 -m unittest discover -s tests -v
```

The doctor checks executable availability and versions. It does not prove an MCP connection works. No package installation or change to your AI-client settings happens automatically.

For document generation, install your preferred PDF/DOCX tools separately. One option is a private Python environment with ReportLab and pypdf, plus Poppler for page previews. LibreOffice can convert DOCX/ODT to PDF. See APPLICATION-PACKAGES.md for rendering checks. The tracker and library utility have no third-party Python dependencies.

## JobSpy MCP

Use the upstream server distributed by [speedyapply/JobSpy](https://github.com/speedyapply/JobSpy/tree/main/mcp), not an unrelated similarly named repository. The upstream launcher is:

```bash
uvx mcp-jobspy@latest
```

This starts a stdio server, not an interactive search screen. Usually the AI client launches it. Its discovered tools include `search_jobs` and `get_job_details`. The latter reads full records from a prior search; saving a search also retains results beyond the preview. Inspect the current tool schema instead of guessing argument names.

Use `latest` for initial discovery only. After a successful smoke test, find the installed release and replace `latest` with that version in your local configuration. Keep a private install record. We do not claim the versions of unrelated local applications are a reproducible lockfile for this toolkit.

## Playwright MCP and Chrome

Install Microsoft's [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm) in the Chrome profile you intend to use. Configure [Playwright MCP](https://github.com/microsoft/playwright-mcp) with `--extension`. This connects to an existing browser rather than requiring an isolated automation profile.

```bash
npx -y @playwright/mcp@latest --extension
```

The AI client normally starts this command. On its first browser action, approve the extension connection and select the intended tab. Current extension versions use client-owned tabs/groups. If the agent sees a blank tab, move the intended application tab into its group and ask it to inspect again. A browser restart can require reconnecting. Pin a tested MCP version afterward; extension releases update separately.

The optional `PLAYWRIGHT_MCP_EXTENSION_TOKEN` comes from your own extension status page. It permits reconnecting without the approval dialog; keep it in a private client environment, never in this repository or chat. The default examples omit it. A token does not mean the desired tab has been selected. Rotate exposed tokens through the extension and restart the client.

The extension grants meaningful browser access. Use a dedicated job-search Chrome profile if you want separation from other browsing. See Microsoft's current [extension guide](https://github.com/microsoft/playwright/blob/main/packages/extension/README.md) for permissions and connection behavior.

## Generate client snippets

After creating the private workspace:

```bash
python3 tools/mcp_config.py --workspace "$HOME/job-search-private" --output "$HOME/job-search-private/private/client-config"
```

This writes sample Claude Desktop JSON and Codex TOML with resolved executable paths. It does not replace an existing client configuration. Inspect the files and merge the named server entries into your settings. JSON paths are escaped automatically, including Windows paths. If a GUI client cannot find a command, use the full path printed by the doctor. Windows command launch behavior varies by client; see TROUBLESHOOTING.md.

### Claude Desktop

Open Settings > Developer > Edit Config (wording can vary by release), then merge the `mcpServers` entries from the generated JSON. Restart the application fully. Verify the servers appear in the client. The sample includes a filesystem MCP restricted to the private workspace and toolkit directory; omit it if the client already has suitable native file access. File access alone does not provide shell execution. The user can run the documented Python commands when the client cannot.

Do not overwrite unrelated servers. Follow the [local MCP setup guide](https://modelcontextprotocol.io/docs/develop/connect-local-servers) if the menu or config location differs.

### Codex CLI

Codex reads MCP entries from its TOML configuration. Merge the generated entries into your user config, or use the CLI:

```bash
codex mcp add jobspy -- uvx mcp-jobspy@latest
codex mcp add job-application-browser -- npx -y @playwright/mcp@latest --extension
codex mcp list
```

Use an installed release in place of `latest` after verification. Give the agent access to the private workspace under your normal permission settings. See [official MCP documentation](https://developers.openai.com/codex/mcp/). No API key is needed by this toolkit itself; your AI client manages its own authentication.

### Other clients

Configure two stdio servers with the same command/argument pairs. Supply a local file tool and a command runner, or run helper commands yourself. Paste AGENTS.md and the current task prompt if the client does not discover repository instructions. Tool names may be namespaced differently; identify capabilities by their descriptions and live schemas.

## Smoke tests before onboarding

1. Ask the agent to list files in the empty private workspace. Confirm it can read profile.json and write then remove a harmless test note.
2. Ask it to discover JobSpy tools and make one small search (one board, five results). Retrieve full details for one result. Save errors as errors, not an empty successful search.
3. Serve the local practice form from the repository: `python3 -m http.server 8765 --bind 127.0.0.1 --directory examples`. Open `http://127.0.0.1:8765/practice-form.html` in Chrome yourself.
4. Approve the Playwright connection to that tab. Ask the agent to fill the fictional name, choose a country and pause before Finish. Confirm values yourself. The form sends no data.
5. Close the test server with Ctrl+C. Record the successful client, OS, executable paths and installed MCP versions privately. Verify file uploads on the first real form and ask for manual attachment if needed.

A successful local test does not guarantee employer sites will accept an automated session. The manual workflow remains available.
