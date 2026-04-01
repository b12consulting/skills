# Atlassian Document Format and Body Payloads

Use this file before creating rich text for Jira or Confluence.

## What to know first

- Jira Cloud descriptions and some comment bodies commonly use Atlassian Document Format (ADF).
- Confluence Cloud v2 page bodies can use `atlas_doc_format`.
- Confluence comments are still commonly sent as storage-format HTML payloads.
- Plain markdown is not accepted directly by Atlassian APIs. Convert it first.

## Minimal ADF document

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello from the agent."
        }
      ]
    }
  ]
}
```

## Common ADF building blocks

### Heading

```json
{
  "type": "heading",
  "attrs": { "level": 2 },
  "content": [{ "type": "text", "text": "Release notes" }]
}
```

### Bullet list

```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "First item" }]
        }
      ]
    }
  ]
}
```

### Code block

```json
{
  "type": "codeBlock",
  "attrs": { "language": "bash" },
  "content": [{ "type": "text", "text": "echo hello" }]
}
```

## Jira usage

Typical Jira create or update payload snippets:

```json
{
  "fields": {
    "summary": "Agent-created issue",
    "description": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Investigate the deployment failure." }
          ]
        }
      ]
    }
  }
}
```

## Confluence Cloud v2 page body

```json
{
  "spaceId": "123456",
  "status": "current",
  "title": "Agent Notes",
  "body": {
    "representation": "atlas_doc_format",
    "value": "{\"version\":1,\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Hello\"}]}]}"
  }
}
```

Important: for Confluence Cloud v2, `body.value` is often sent as a JSON string containing the ADF document.

## Confluence storage format comments

Comments are often simpler with storage-format HTML:

```json
{
  "body": {
    "representation": "storage",
    "value": "<p>Reviewed by the agent.</p>"
  }
}
```

## Safe authoring workflow

1. Draft the intended text in plain language.
2. Convert it to minimal ADF or storage HTML.
3. Save it inside `temp_payload.json`.
4. Run the relevant script with `--dry-run`.
5. Execute only after checking the serialized body carefully.

## Practical advice

- Keep ADF simple unless the page genuinely needs rich structure.
- Prefer paragraphs, headings, bullet lists, and code blocks.
- Escape embedded JSON correctly when Confluence expects `body.value` as a string.
- If you are unsure whether the target field expects ADF or storage format, fetch an existing example first.
