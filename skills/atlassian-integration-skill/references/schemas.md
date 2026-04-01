# Payload Schemas for Common Atlassian Operations

Use these examples as starting points. Keep them minimal and instance-specific.

## Jira create issue

```json
{
  "fields": {
    "project": {
      "key": "DEMO"
    },
    "issuetype": {
      "name": "Task"
    },
    "summary": "Agent-created task",
    "description": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Describe the work clearly."
            }
          ]
        }
      ]
    }
  }
}
```

## Jira update issue

```json
{
  "fields": {
    "summary": "Updated summary"
  },
  "update": {
    "labels": [
      {
        "add": "agent-reviewed"
      }
    ]
  }
}
```

## Jira comment

```json
{
  "body": "Plain text comment"
}
```

If the Jira instance requires ADF comments, replace `body` with an ADF document object.

## Jira transition

```json
{
  "transition": {
    "id": "31"
  }
}
```

## Confluence create page (Cloud v2)

```json
{
  "spaceId": "123456",
  "status": "current",
  "title": "Agent Runbook",
  "parentId": "78910",
  "body": {
    "representation": "atlas_doc_format",
    "value": "{\"version\":1,\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Hello from the agent.\"}]}]}"
  }
}
```

## Confluence update page (Cloud v2)

```json
{
  "title": "Agent Runbook",
  "body": {
    "representation": "atlas_doc_format",
    "value": "{\"version\":1,\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Updated content.\"}]}]}"
  }
}
```

The script fills `id`, `status`, and the incremented `version.number`.

## Confluence create or update page (Server/Data Center)

```json
{
  "type": "page",
  "title": "Agent Runbook",
  "space": {
    "key": "ENG"
  },
  "body": {
    "storage": {
      "value": "<p>Hello from the agent.</p>",
      "representation": "storage"
    }
  }
}
```

## Confluence comment

### Cloud v2

```json
{
  "body": {
    "representation": "storage",
    "value": "<p>Reviewed by the agent.</p>"
  }
}
```

### Server/Data Center

```json
{
  "type": "comment",
  "body": {
    "storage": {
      "value": "<p>Reviewed by the agent.</p>",
      "representation": "storage"
    }
  }
}
```

## Validation checklist

- Confirm project key, issue type, and custom field IDs for Jira.
- Confirm space ID or space key, parent page, and body representation for Confluence.
- Fetch the existing issue or page before any update.
- Use `--dry-run` before live execution.
