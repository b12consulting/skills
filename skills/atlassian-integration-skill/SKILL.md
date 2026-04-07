---
name: atlassian-integration-skill
description: Use this skill to interact with Jira and Confluence through bundled Python scripts wrapping the Atlassian CLI and REST API, with JQL/CQL query patterns and ADF payload references.
---

# Atlassian Integration Skill

Use this skill when an agent needs reliable access to Atlassian Jira or Confluence.

For Jira, the bundled `jira_ops.py` script wraps the official [Atlassian CLI (acli)](https://developer.atlassian.com/cloud/acli/guides/introduction/) with auto-authentication, read-only enforcement, and consistent JSON output. For Confluence, `confluence_ops.py` wraps the REST API. Both share the same 1Password-backed credential resolution and are supported by JQL/CQL query patterns and ADF payload references.

## When to Use

Load this skill when you need to:

- search Jira with JQL
- fetch Jira issue context for downstream coding work
- create or update Jira work items
- transition a Jira work item or add comments
- search Confluence with CQL
- fetch Confluence page context for downstream coding work
- understand Atlassian Document Format (ADF) for rich text payloads

## Prerequisites

Install the Atlassian CLI for your platform:

- [macOS](https://developer.atlassian.com/cloud/acli/guides/install-macos/)
- [Linux](https://developer.atlassian.com/cloud/acli/guides/install-linux/)
- [Windows](https://developer.atlassian.com/cloud/acli/guides/install-windows/)

Verify installation:

```bash
acli --help
```

## Authentication

### Recommended: shared 1Password credentials (same as Confluence)

The bundled `acli_auth.py` script reuses the same credential resolution logic as the Confluence scripts (`auth_client.load_config`). It reads `JIRA_URL`, `JIRA_USERNAME`, and `JIRA_API_TOKEN` (with `ATLASSIAN_*` fallbacks), automatically resolves any `op://` 1Password secret references, and pipes the token into `acli jira auth login`.

Set your `.env` with `op://` references:

```bash
JIRA_URL=op://YOUR_VAULT/Atlassian Skill/jira_url
JIRA_USERNAME=op://YOUR_VAULT/Atlassian Skill/jira_username
JIRA_API_TOKEN=op://YOUR_VAULT/Atlassian Skill/jira_api_token
ATLASSIAN_DEPLOYMENT=cloud
```

Then authenticate:

```bash
eval "$(op signin)"
scripts/run_with_1password.sh python scripts/acli_auth.py
```

Or without the wrapper (when env vars are already resolved or contain plain values):

```bash
python scripts/acli_auth.py
```

Check current auth status:

```bash
python scripts/acli_auth.py --status
```

### API token (manual)

```bash
echo "$JIRA_API_TOKEN" | acli jira auth login \
  --site "your-domain.atlassian.net" \
  --email "agent@example.com" \
  --token
```

### OAuth (interactive)

```bash
acli jira auth login --web
```

## Defaults

- **Always use `jira_ops.py`** for Jira operations. It handles authentication, correct acli syntax, and JSON output automatically.
- Prefer raw outputs over summaries unless a human explicitly asks for a summary.
- Read `references/jql_cql_guide.md` before writing or debugging JQL or CQL queries.
- Read `references/atlassian_format.md` before creating rich-text Jira descriptions or Confluence page bodies.

## Common Commands

### View a work item

```bash
python scripts/jira_ops.py view --key DEMO-123
```

### Search work items

```bash
python scripts/jira_ops.py search --jql 'project = DEMO ORDER BY updated DESC' --limit 10
```

### Create a work item

```bash
python scripts/jira_ops.py create --project DEMO --type Task --summary "Agent-created task"
```

For complex payloads with ADF descriptions, use a JSON file:

```bash
python scripts/jira_ops.py create --from-json workitem.json
```

### Edit a work item

```bash
python scripts/jira_ops.py edit --key DEMO-123 --summary "Updated summary"
```

### Transition a work item

```bash
python scripts/jira_ops.py transition --key DEMO-123 --status "In Progress"
```

### Comment on a work item

```bash
python scripts/jira_ops.py comment --key DEMO-123 --body "Agent review complete."
```

### Assign a work item

```bash
python scripts/jira_ops.py assign --key DEMO-123 --assignee "user@example.com"
```

## Progressive Disclosure

Do not load every reference file by default.

- Read `references/jql_cql_guide.md` before writing or debugging JQL or CQL queries.
- Read `references/schemas.md` before creating or updating any Confluence page payload.
- Read `references/atlassian_format.md` before creating rich-text Jira descriptions, Confluence page bodies, or comment bodies with ADF.

## Workflow Checklists

### Safe read-only workflow (Jira)

1. Search or view the relevant work item:
   ```bash
   python scripts/jira_ops.py view --key DEMO-123
   ```
2. Use the retrieved content directly as coding context.
3. Only summarize if the human explicitly asks for a summary.

### Jira write workflow

1. If rich text is needed, read `references/atlassian_format.md`.
2. For updates, first view the issue to see its current state:
   ```bash
   python scripts/jira_ops.py view --key DEMO-123
   ```
3. Execute the write command (requires `ATLASSIAN_READ_ONLY=false` and `ATLASSIAN_ENABLE_WRITES=I_UNDERSTAND`):
   ```bash
   python scripts/jira_ops.py edit --key DEMO-123 --summary "Updated summary"
   ```

## Confluence

The Atlassian CLI does not yet support Confluence. Use the bundled Python scripts for Confluence operations.

### Confluence environment setup

Set environment variables before running the scripts. The scripts auto-load the nearest `.env` file from the current working directory up to this skill's root directory. Existing shell environment variables win over `.env` values.

#### Confluence Cloud

```bash
export CONFLUENCE_URL="https://your-domain.atlassian.net/wiki"
export CONFLUENCE_USERNAME="agent@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export ATLASSIAN_DEPLOYMENT="cloud"
```

#### Confluence Server or Data Center

```bash
export CONFLUENCE_URL="https://confluence.example.com"
export CONFLUENCE_API_TOKEN="your-personal-access-token"
export ATLASSIAN_DEPLOYMENT="server"
```

Shared fallbacks are also supported: `ATLASSIAN_URL`, `ATLASSIAN_USERNAME`, and `ATLASSIAN_API_TOKEN`.

#### 1Password integration

If your company uses 1Password, prefer `op://...` secret references instead of raw credentials in `.env`:

```bash
CONFLUENCE_URL=op://YOUR_VAULT/Atlassian Skill/confluence_url
CONFLUENCE_USERNAME=op://YOUR_VAULT/Atlassian Skill/confluence_username
CONFLUENCE_API_TOKEN=op://YOUR_VAULT/Atlassian Skill/confluence_api_token
ATLASSIAN_DEPLOYMENT=cloud
```

Day-to-day flow:

```bash
eval "$(op signin)"
scripts/run_with_1password.sh python scripts/confluence_ops.py get --page-id 123456
```

#### Write enable switch

Writes are disabled by default. To allow live write requests, set both variables:

```bash
ATLASSIAN_READ_ONLY=false
ATLASSIAN_ENABLE_WRITES=I_UNDERSTAND
```

Both are required. If either value is missing or different, the scripts remain read-only.

### Confluence commands

```bash
python scripts/confluence_ops.py search --cql 'type = page AND title ~ "Runbook"' --limit 10
python scripts/confluence_ops.py get --page-id 123456
python scripts/confluence_ops.py get --page-id 123456 --output json
python scripts/confluence_ops.py list-attachments --page-id 123456
```

### Safe read-only workflow (Confluence)

1. Search for the page:
   ```bash
   python scripts/confluence_ops.py search --cql 'type = page AND space = ENG' --limit 10
   ```
2. Fetch the page content:
   ```bash
   python scripts/confluence_ops.py get --page-id 123456 --output body
   ```
3. Use the retrieved page content directly as coding context.
4. Only summarize if the human explicitly asks for a summary.

### Confluence payload planning workflow

1. Read `references/schemas.md`.
2. Read `references/atlassian_format.md` before building a page body.
3. Draft the request body in `temp_payload.json`.
4. For updates, fetch the page first to capture the current version:
   ```bash
   python scripts/confluence_ops.py get --page-id 123456
   ```
5. Validate locally:
   ```bash
   python scripts/confluence_ops.py update-page --page-id 123456 --payload-file temp_payload.json --dry-run
   ```
6. Stop at dry-run. Live Confluence writes are intentionally blocked unless both write-enable variables are set.

### Confluence gotchas

- Confluence Cloud page bodies use Atlassian Document Format (`atlas_doc_format`). Raw markdown is not accepted directly by the page API.
- Confluence Cloud CQL search still relies on the v1 search endpoint even when page CRUD uses v2.
- Confluence page updates require the next version number. The script fetches the current version automatically when needed.
- Confluence attachment uploads require `X-Atlassian-Token: nocheck`.
- `confluence_ops.py get` defaults to `--output body` for coding-agent context retrieval.
- `confluence_ops.py get --output markdown` is a summary view; use `--output body` when you need the actual readable page content.
- Server/Data Center commonly uses bearer personal access tokens, while Cloud uses email plus API token basic auth.
- Space keys are usually uppercase short codes (e.g., `ENG`, `OPS`).

## Gotchas

- acli currently supports **Jira Cloud only**. For Jira Server/Data Center, use the REST API directly.
- Jira Cloud user identity uses `accountId`, not legacy usernames.
- Jira transitions require the exact target status name.
- Before changing a Jira issue, view it first to see available transitions and editable fields.
- Some fields visible in the UI are custom fields. Use exact field IDs like `customfield_12345` in payloads.
- When using `--from-json`, Jira descriptions use Atlassian Document Format (ADF), not raw markdown.

## Troubleshooting

- If `jira_ops.py` auto-authentication fails, run `python scripts/acli_auth.py --verbose` to diagnose.
- If acli authentication fails, verify your site URL and API token.
- Use `acli jira workitem <command> --help` to discover available flags for any raw acli command.
- If Confluence authentication fails, verify URL shape. Confluence Cloud usually needs the `/wiki` base URL.
- Confluence error messages intentionally avoid printing the configured host to reduce accidental infrastructure disclosure.
- If you see certificate verification failures for Confluence, install `certifi` (`pip install certifi`). The scripts auto-detect it and use its CA bundle (same strategy as the `requests` library). Alternatively, set `ATLASSIAN_CA_BUNDLE=/path/to/ca.pem`. Never disable verification in production.
- If Confluence update fails with version errors, fetch the latest page again and retry with a fresh payload.
- If a JQL or CQL query returns empty results, simplify the query and test incrementally.
- See the [acli command reference](https://developer.atlassian.com/cloud/acli/reference/commands/jira/) for full Jira CLI documentation.

## Files in This Skill

| File | Purpose |
|------|---------|
| `scripts/auth_client.py` | Shared auth, retries, HTTP helpers for Confluence scripts |
| `scripts/acli_auth.py` | Authenticate acli using the same 1Password-backed credentials as Confluence |
| `scripts/jira_ops.py` | Jira CLI wrapper with auto-auth, read-only enforcement, and JSON output |
| `scripts/confluence_ops.py` | Confluence CLI wrapper |
| `scripts/run_with_1password.sh` | 1Password process-scoped secret injection wrapper |
| `references/jql_cql_guide.md` | JQL and CQL query patterns |
| `references/atlassian_format.md` | ADF guidance for rich text payloads |
| `references/schemas.md` | Minimal payload shapes for Confluence operations |
