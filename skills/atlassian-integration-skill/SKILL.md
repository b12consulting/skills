---
name: atlassian-integration-skill
description: Use this skill to search, read, create, update, transition, and comment on Jira issues and Confluence pages through Atlassian REST APIs with reusable local scripts.
---

# Atlassian Integration Skill

Use this skill when an agent needs reliable, scriptable access to Atlassian Jira or Confluence.

This skill is primarily for retrieving exact Jira and Confluence context for downstream coding work. Do not summarize by default. Retrieve the raw issue/page content first, then let the coding agent use that content directly.

The bundled scripts provide a local wrapper around Atlassian REST APIs for:

- Jira search, read, create, update, transition, and comments
- Confluence search, read, create, update, comments, and attachments
- Cloud and Server/Data Center authentication

## When to Use

Load this skill when you need to:

- search Jira with JQL
- fetch Jira issue context for downstream coding work
- create or update Jira issues safely
- transition a Jira issue and add comments
- search Confluence with CQL
- fetch Confluence page context for downstream coding work
- create or update Confluence pages with structured bodies
- add Confluence comments or manage attachments

## Defaults

- Prefer Jira Cloud REST API v3.
- Prefer Confluence Cloud REST API v2 for page operations.
- Use Confluence REST API v1 only where v2 does not provide the needed capability yet, especially CQL search.
- For Server/Data Center, use the compatible v1/v2-style endpoints automatically selected by the scripts.
- Read-only mode is the default. Live create, update, transition, comment, and attachment upload requests stay blocked unless you explicitly opt in.
- Use `--dry-run` for any write-style command if you need to inspect payloads without sending them.
- Prefer context/body outputs over summary outputs unless a human explicitly asks for a summary.

## Environment Setup

Set environment variables before running the scripts.

The scripts auto-load the nearest `.env` file from the current working directory up to this skill's root directory. They do not keep walking above the skill root. Existing shell environment variables win over `.env` values.

### Recommended: 1Password-backed configuration

If your company uses 1Password, prefer `op://...` secret references instead of storing raw credentials in `.env`.

Create a single 1Password item, for example:

- Vault: `Project Name`
- Item title: `Atlassian Skill`
- Fields: `jira_url`, `jira_username`, `jira_api_token`, `confluence_url`, `confluence_username`, `confluence_api_token`

Then point the skill at those exact fields:

```bash
JIRA_URL=op://YOUR_VAULT/Atlassian Skill/jira_url
JIRA_USERNAME=op://YOUR_VAULT/Atlassian Skill/jira_username
JIRA_API_TOKEN=op://YOUR_VAULT/Atlassian Skill/jira_api_token
CONFLUENCE_URL=op://YOUR_VAULT/Atlassian Skill/confluence_url
CONFLUENCE_USERNAME=op://YOUR_VAULT/Atlassian Skill/confluence_username
CONFLUENCE_API_TOKEN=op://YOUR_VAULT/Atlassian Skill/confluence_api_token
ATLASSIAN_DEPLOYMENT=cloud
ATLASSIAN_READ_ONLY=true
```

The skill does not scan vaults. It only resolves the exact `op://vault/item/field` references you provide. To keep access scoped, use a 1Password account or service account that only has access to the vault you want this skill to read.

Before using the skill, confirm the CLI can resolve one field:

```bash
eval "$(op signin)"
op read 'op://YOUR_VAULT/Atlassian Skill/jira_api_token'
```

The Python loader resolves `op://...` values with `op read` automatically. For process-scoped injection, you can also run commands through:

```bash
scripts/run_with_1password.sh python scripts/jira_ops.py get --issue DEMO-123
```

Recommended day-to-day flow:

```bash
eval "$(op signin)"
scripts/run_with_1password.sh python scripts/jira_ops.py get --issue DEMO-123
```

### Jira Cloud

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_USERNAME="agent@example.com"
export JIRA_API_TOKEN="your-api-token"
export ATLASSIAN_DEPLOYMENT="cloud"
```

### Jira Server or Data Center

```bash
export JIRA_URL="https://jira.example.com"
export JIRA_API_TOKEN="your-personal-access-token"
export ATLASSIAN_DEPLOYMENT="server"
```

### Confluence Cloud

```bash
export CONFLUENCE_URL="https://your-domain.atlassian.net/wiki"
export CONFLUENCE_USERNAME="agent@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export ATLASSIAN_DEPLOYMENT="cloud"
```

### Confluence Server or Data Center

```bash
export CONFLUENCE_URL="https://confluence.example.com"
export CONFLUENCE_API_TOKEN="your-personal-access-token"
export ATLASSIAN_DEPLOYMENT="server"
```

Shared fallbacks are also supported: `ATLASSIAN_URL`, `ATLASSIAN_USERNAME`, and `ATLASSIAN_API_TOKEN`.

### Optional write enable switch

Writes are disabled by default. To allow live write requests, set both variables:

```bash
ATLASSIAN_READ_ONLY=false
ATLASSIAN_ENABLE_WRITES=I_UNDERSTAND
```

Both are required. If either value is missing or different, the skill remains read-only.

### Optional `.env` file

```bash
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=agent@example.com
JIRA_API_TOKEN=your-api-token
CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_USERNAME=agent@example.com
CONFLUENCE_API_TOKEN=your-api-token
ATLASSIAN_DEPLOYMENT=cloud
```

Notes:

- `.env` loading is automatic; no `source .env` step is required for these scripts.
- Explicit environment variables already exported in the shell take precedence.
- Do not commit `.env` files with real credentials.
- Prefer storing `op://...` references in `.env` instead of plaintext secrets whenever 1Password is available.
- Keep `.env` files local to this skill directory and rotate any credential that was ever written to disk on a shared machine.
- Keep `ATLASSIAN_READ_ONLY=true` unless you intentionally need write access.

### TLS options

If your Jira or Confluence server uses a private or enterprise CA, prefer a custom CA bundle:

```bash
ATLASSIAN_CA_BUNDLE=/absolute/path/to/company-ca.pem
```

For temporary testing only, you can bypass verification:

```bash
ATLASSIAN_INSECURE_SKIP_VERIFY=true
```

Use the insecure option only as a last resort, never in shared or production environments, and remove it immediately after the diagnostic session.

## Progressive Disclosure

Do not load every reference file by default.

- Read `references/jql_cql_guide.md` before writing or debugging JQL/CQL queries.
- Read `references/schemas.md` before creating or updating any Jira issue or Confluence page payload.
- Read `references/atlassian_format.md` before creating rich-text Jira descriptions, comments, or Confluence page bodies.

## Script Entry Points

Run commands from the skill directory.

### Jira

```bash
python scripts/jira_ops.py search --jql 'project = DEMO ORDER BY updated DESC' --limit 10
python scripts/jira_ops.py get --issue DEMO-123
python scripts/jira_ops.py get --issue DEMO-123 --output json
python scripts/jira_ops.py get --issue DEMO-123 --expand editmeta,transitions
```

### Confluence

```bash
python scripts/confluence_ops.py search --cql 'type = page AND title ~ "Runbook"' --limit 10
python scripts/confluence_ops.py get --page-id 123456
python scripts/confluence_ops.py get --page-id 123456 --output json
python scripts/confluence_ops.py list-attachments --page-id 123456
```

## Workflow Checklists

### Safe read-only workflow

1. Run the relevant `search` or `get` command.
2. Prefer direct retrieval outputs, not summaries:
   ```bash
   python scripts/jira_ops.py get --issue DEMO-123
   python scripts/confluence_ops.py get --page-id 123456 --output body
   ```
3. Use the retrieved issue/page content directly as coding context.
4. Only summarize if the human explicitly asks for a summary.

### Jira payload planning workflow

1. Read `references/schemas.md`.
2. If rich text is needed, read `references/atlassian_format.md`.
3. Draft the request body in `temp_payload.json`.
4. For updates, first fetch the issue:
   ```bash
   python scripts/jira_ops.py get --issue DEMO-123 --expand editmeta,transitions
   ```
5. Validate locally:
   ```bash
   python scripts/jira_ops.py update --issue DEMO-123 --payload-file temp_payload.json --dry-run
   ```
6. Stop at dry-run. Live Jira writes are intentionally blocked by the skill.

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
6. Stop at dry-run. Live Confluence writes are intentionally blocked by the skill.

## Gotchas

- Jira Cloud user identity uses `accountId`, not legacy usernames.
- Jira transitions require a transition ID or exact transition name available for the current issue state.
- Before changing a Jira issue, fetch it first with `--expand editmeta,transitions` so you can see editable fields and valid transitions.
- Jira Cloud search is moving toward `/rest/api/3/search/jql`; the script uses the modern endpoint on Cloud by default.
- The skill is read-only by default. Any live POST, PUT, PATCH, or DELETE request is rejected unless both write-enable variables are set exactly as documented.
- Confluence Cloud page bodies use Atlassian Document Format for `atlas_doc_format`. Raw markdown is not accepted directly by the page API.
- Confluence Cloud CQL search still relies on the v1 search endpoint even when page CRUD uses v2.
- Confluence page updates require the next version number. The script fetches the current version automatically when needed.
- Confluence attachment uploads require `X-Atlassian-Token: nocheck`.
- `jira_ops.py get` defaults to `--output context` for coding-agent context retrieval.
- `confluence_ops.py get` defaults to `--output body` for coding-agent context retrieval.
- `confluence_ops.py get --output markdown` is a summary view; use `--output body` or `--include-body` when you need the actual readable page content.
- Server/Data Center commonly uses bearer personal access tokens, while Cloud uses email plus API token basic auth.
- Some fields visible in the UI are custom fields. Use exact field IDs like `customfield_12345` in Jira payloads.

## Output Templates

### Jira issue summary

```markdown
## Jira Issue Summary

- Key: ISSUE-123
- Summary: <summary>
- Type: <issue type>
- Status: <status>
- Assignee: <display name or Unassigned>
- Priority: <priority or None>
- Updated: <timestamp>

### Details
<short plain-language summary of description, acceptance criteria, blockers, or next action>
```

### Confluence page summary

```markdown
## Confluence Page Summary

- Title: <title>
- Page ID: <id>
- Space: <space key or id>
- Version: <version>
- Updated: <timestamp>

### Contents
<short summary of the important sections, decisions, or action items>
```

## Output Rules

- Prefer `jira_ops.py get` default `--output context` for coding-agent context retrieval.
- Prefer `confluence_ops.py get` default `--output body` for coding-agent context retrieval.
- Prefer `--output json` when you need exact raw fields or want to chain additional inspection.
- Prefer `--output markdown` only when a human explicitly wants a summary view.
- For destructive commands, keep a copy of the exact payload used in `temp_payload.json` until the task is complete.

## Troubleshooting

- If authentication fails, verify URL shape first. Confluence Cloud usually needs the `/wiki` base URL.
- Error messages intentionally avoid printing the configured Atlassian host to reduce accidental infrastructure disclosure.
- If you see certificate verification failures, prefer `ATLASSIAN_CA_BUNDLE=/path/to/ca.pem` over disabling verification.
- If you enable writes temporarily, prefer one-command scoped environment variables instead of persisting them in `.env`, and unset the write flags immediately after the task is complete.
- If you use 1Password, keep the `.env` file limited to `op://...` references and run the helper wrapper or `op run` manually so real secrets stay process-scoped.
- If Jira update fails with field errors, fetch the issue with `--expand editmeta`.
- If Confluence update fails with version errors, fetch the latest page again and retry with a fresh payload.
- If a query returns empty results, simplify the JQL or CQL and test incrementally.

## Files in This Skill

| File | Purpose |
|------|---------|
| `scripts/auth_client.py` | Shared auth, retries, HTTP helpers, JSON and multipart support |
| `scripts/jira_ops.py` | Jira CLI wrapper |
| `scripts/confluence_ops.py` | Confluence CLI wrapper |
| `references/jql_cql_guide.md` | JQL and CQL query patterns |
| `references/atlassian_format.md` | ADF guidance for rich text payloads |
| `references/schemas.md` | Minimal payload shapes for common operations |
