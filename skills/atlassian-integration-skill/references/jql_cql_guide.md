# JQL and CQL Quick Guide

Use this reference when you need to write or debug Jira Query Language or Confluence Query Language.

## Jira Query Language (JQL)

### Common fields

- `project`
- `issuetype`
- `status`
- `assignee`
- `reporter`
- `priority`
- `labels`
- `updated`
- `created`
- `resolution`

### Core patterns

```jql
project = DEMO
project = DEMO AND status = "In Progress"
project = DEMO AND assignee = currentUser()
project = DEMO AND labels = backend
project = DEMO AND updated >= -7d
project = DEMO ORDER BY updated DESC
```

### Useful operators

- `=`, `!=`
- `IN`, `NOT IN`
- `~` for contains-style text search
- `IS EMPTY`, `IS NOT EMPTY`
- `>=`, `<=`, `>`, `<`
- `AND`, `OR`, `NOT`
- `ORDER BY`

### Time helpers

- `startOfDay()`
- `startOfWeek()`
- `startOfMonth()`
- `currentUser()`

### Examples

```jql
project = PLATFORM AND issuetype in (Bug, Task)
project = OPS AND resolution IS EMPTY AND priority in (High, Highest)
text ~ "\"single sign-on\"" ORDER BY created DESC
assignee = currentUser() AND status NOT IN (Done, Closed)
```

### JQL tips

- Quote values containing spaces.
- Prefer exact project keys and status names from the target instance.
- Custom fields often require IDs like `cf[12345]` or API field names like `customfield_12345`.
- Build complex queries incrementally if search returns no results.

## Confluence Query Language (CQL)

### Common fields

- `type`
- `title`
- `space`
- `label`
- `creator`
- `contributor`
- `lastModified`
- `created`
- `ancestor`

### Core patterns

```cql
type = page
type = page AND space = ENG
type = page AND title ~ "Runbook"
label = documentation
creator = currentUser()
lastModified > startOfMonth("-1M")
```

### Examples

```cql
type = page AND space = PLATFORM AND title ~ "Architecture"
space = ENG AND text ~ "\"incident response\""
label = runbook AND lastModified > startOfWeek()
ancestor = 123456 AND type = page
```

### CQL tips

- Cloud search still uses the Confluence v1 search endpoint.
- Space keys are usually uppercase short codes.
- Quote values with spaces or special characters.
- Search can be broad; narrow by `space`, `type`, `label`, or `ancestor`.

## Query Debugging Workflow

1. Start with the smallest working filter.
2. Add one clause at a time.
3. Run the script with `--limit 5` first.
4. Only add sorting after the filters work.

## Example commands

```bash
acli jira workitem search --jql 'project = DEMO ORDER BY updated DESC' --limit 5
python scripts/confluence_ops.py search --cql 'type = page AND space = ENG' --limit 5
```
