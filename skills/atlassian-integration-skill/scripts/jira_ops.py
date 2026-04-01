#!/usr/bin/env python3
"""CLI wrappers for Jira REST API operations."""

from __future__ import annotations

import argparse
from typing import Any

from auth_client import (
    AtlassianClient,
    AtlassianClientError,
    dump_output,
    load_json_file,
)


def _join_extracted_text(items: list[Any]) -> str:
    return "\n".join(
        part for part in (extract_jira_text(item) for item in items) if part
    )


def jira_api_path(client: AtlassianClient, path: str) -> str:
    """Return a Jira REST endpoint for the configured deployment."""

    version = "3" if client.config.is_cloud else "2"
    return f"rest/api/{version}/{path.lstrip('/')}"


def extract_jira_text(value: Any) -> str:
    """Extract readable text from Jira plain-text or ADF-like payloads."""

    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return _join_extracted_text(value)
    if not isinstance(value, dict):
        return ""

    if value.get("type") == "text":
        return value.get("text", "")

    content = value.get("content", [])
    return _join_extracted_text(content)


def build_jira_context(issue: dict[str, Any]) -> str:
    """Render issue context optimized for downstream coding tasks."""

    fields = issue.get("fields", {})
    description = extract_jira_text(fields.get("description"))
    comments = fields.get("comment", {}).get("comments", [])
    comment_blocks: list[str] = []
    for comment in comments:
        comment_text = extract_jira_text(comment.get("body"))
        if comment_text:
            comment_blocks.append(comment_text)

    parts = [
        f"Key: {issue.get('key', 'Unknown')}",
        f"Summary: {fields.get('summary') or '(no summary)'}",
        f"Status: {((fields.get('status') or {}).get('name')) or 'Unknown'}",
        "",
        "Description:",
        description or "(no description)",
    ]
    if comment_blocks:
        parts.extend(["", "Comments:", "\n\n".join(comment_blocks)])
    return "\n".join(parts)


def build_jira_markdown(issue: dict[str, Any]) -> str:
    """Render a compact markdown summary for a Jira issue."""

    fields = issue.get("fields", {})
    issue_type = (fields.get("issuetype") or {}).get("name", "Unknown")
    status = ((fields.get("status") or {}).get("name")) or "Unknown"
    assignee = ((fields.get("assignee") or {}).get("displayName")) or "Unassigned"
    priority = ((fields.get("priority") or {}).get("name")) or "None"
    summary = fields.get("summary") or "(no summary)"
    description = fields.get("description")
    description_hint = "ADF document" if isinstance(description, dict) else "None"
    updated = fields.get("updated") or issue.get("updated") or "Unknown"

    return "\n".join(
        [
            "## Jira Issue Summary",
            "",
            f"- Key: {issue.get('key', 'Unknown')}",
            f"- Summary: {summary}",
            f"- Type: {issue_type}",
            f"- Status: {status}",
            f"- Assignee: {assignee}",
            f"- Priority: {priority}",
            f"- Updated: {updated}",
            "",
            "### Details",
            f"Description format: {description_hint}",
        ]
    )


def validate_payload_file(path: str) -> dict[str, Any]:
    """Load and validate a Jira request payload file."""

    return load_json_file(path)


def command_search(client: AtlassianClient, args: argparse.Namespace) -> str:
    """Execute a Jira search command."""

    endpoint = (
        jira_api_path(client, "search/jql")
        if client.config.is_cloud
        else jira_api_path(client, "search")
    )
    query: dict[str, Any] = {
        "maxResults": args.limit,
        "fields": args.fields,
        "expand": args.expand,
        "jql": args.jql,
    }
    data = client.request_json("GET", endpoint, query=query)
    return dump_output(data, fmt=args.output)


def command_get(client: AtlassianClient, args: argparse.Namespace) -> str:
    endpoint = jira_api_path(client, f"issue/{args.issue}")
    data = client.request_json(
        "GET",
        endpoint,
        query={
            "fields": args.fields,
            "expand": args.expand,
        },
    )
    if args.output == "context":
        return build_jira_context(data)
    if args.output == "markdown":
        return build_jira_markdown(data)
    return dump_output(data, fmt=args.output)


def command_create(client: AtlassianClient, args: argparse.Namespace) -> str:
    payload = validate_payload_file(args.payload_file)
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "jira_create_issue",
                "endpoint": jira_api_path(client, "issue"),
                "payload": payload,
            },
            fmt=args.output,
        )
    data = client.request_json("POST", jira_api_path(client, "issue"), payload=payload)
    return dump_output(data, fmt=args.output)


def command_update(client: AtlassianClient, args: argparse.Namespace) -> str:
    payload = validate_payload_file(args.payload_file)
    if args.dry_run:
        current = client.request_json(
            "GET",
            jira_api_path(client, f"issue/{args.issue}"),
            query={"expand": "editmeta"},
        )
        return dump_output(
            {
                "dry_run": True,
                "operation": "jira_update_issue",
                "endpoint": jira_api_path(client, f"issue/{args.issue}"),
                "editable_fields": sorted(
                    current.get("editmeta", {}).get("fields", {}).keys()
                ),
                "payload": payload,
            },
            fmt=args.output,
        )
    client.request_json(
        "PUT",
        jira_api_path(client, f"issue/{args.issue}"),
        payload=payload,
    )
    result = {"updated": True, "issue": args.issue}
    return dump_output(result, fmt=args.output)


def command_transition(client: AtlassianClient, args: argparse.Namespace) -> str:
    transitions = client.request_json(
        "GET",
        jira_api_path(client, f"issue/{args.issue}/transitions"),
    ).get("transitions", [])
    chosen = resolve_transition(args.transition, transitions)
    payload: dict[str, Any] = {"transition": {"id": chosen["id"]}}
    if args.comment:
        payload["update"] = {"comment": [{"add": {"body": args.comment}}]}
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "jira_transition_issue",
                "issue": args.issue,
                "transition": chosen,
                "payload": payload,
            },
            fmt=args.output,
        )
    client.request_json(
        "POST",
        jira_api_path(client, f"issue/{args.issue}/transitions"),
        payload=payload,
    )
    return dump_output(
        {"transitioned": True, "issue": args.issue, "transition": chosen},
        fmt=args.output,
    )


def command_comment(client: AtlassianClient, args: argparse.Namespace) -> str:
    payload: dict[str, Any] = {"body": args.text}
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "jira_add_comment",
                "issue": args.issue,
                "payload": payload,
            },
            fmt=args.output,
        )
    data = client.request_json(
        "POST",
        jira_api_path(client, f"issue/{args.issue}/comment"),
        payload=payload,
    )
    return dump_output(data, fmt=args.output)


def resolve_transition(
    requested: str,
    transitions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Resolve a Jira transition by id or case-insensitive name."""

    for transition in transitions:
        if transition.get("id") == requested:
            return transition
        if transition.get("name", "").casefold() == requested.casefold():
            return transition
    available = ", ".join(
        f"{item.get('name')} ({item.get('id')})" for item in transitions
    )
    raise AtlassianClientError(
        f"Transition '{requested}' not found. Available transitions: {available}"
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the Jira CLI argument parser."""

    parser = argparse.ArgumentParser(description="Jira REST API helper CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search Jira issues with JQL")
    search.add_argument("--jql", required=True, help="JQL query string")
    search.add_argument("--limit", type=int, default=10, help="Max issues to return")
    search.add_argument(
        "--fields",
        default="summary,status,assignee,priority,issuetype,updated",
        help="Comma-separated field list",
    )
    search.add_argument("--expand", default=None, help="Comma-separated expand list")
    search.add_argument("--output", choices=("json", "markdown"), default="json")
    search.set_defaults(func=command_search)

    get_issue = subparsers.add_parser("get", help="Get a Jira issue")
    get_issue.add_argument("--issue", required=True, help="Issue key or id")
    get_issue.add_argument(
        "--fields", default="*all", help="Comma-separated field list"
    )
    get_issue.add_argument("--expand", default=None, help="Comma-separated expand list")
    get_issue.add_argument(
        "--output", choices=("json", "markdown", "context"), default="context"
    )
    get_issue.set_defaults(func=command_get)

    create = subparsers.add_parser("create", help="Create a Jira issue")
    create.add_argument("--payload-file", required=True, help="JSON payload file")
    create.add_argument("--dry-run", action="store_true", help="Validate only")
    create.add_argument("--output", choices=("json", "markdown"), default="json")
    create.set_defaults(func=command_create)

    update = subparsers.add_parser("update", help="Update a Jira issue")
    update.add_argument("--issue", required=True, help="Issue key or id")
    update.add_argument("--payload-file", required=True, help="JSON payload file")
    update.add_argument("--dry-run", action="store_true", help="Validate only")
    update.add_argument("--output", choices=("json", "markdown"), default="json")
    update.set_defaults(func=command_update)

    transition = subparsers.add_parser("transition", help="Transition a Jira issue")
    transition.add_argument("--issue", required=True, help="Issue key or id")
    transition.add_argument(
        "--transition",
        required=True,
        help="Transition name or id",
    )
    transition.add_argument(
        "--comment",
        default=None,
        help="Optional comment to add in the same transition payload",
    )
    transition.add_argument("--dry-run", action="store_true", help="Validate only")
    transition.add_argument("--output", choices=("json", "markdown"), default="json")
    transition.set_defaults(func=command_transition)

    comment = subparsers.add_parser("comment", help="Add a Jira comment")
    comment.add_argument("--issue", required=True, help="Issue key or id")
    comment.add_argument("--text", required=True, help="Comment text")
    comment.add_argument("--dry-run", action="store_true", help="Validate only")
    comment.add_argument("--output", choices=("json", "markdown"), default="json")
    comment.set_defaults(func=command_comment)

    return parser


def main() -> int:
    """Run the Jira CLI."""

    parser = build_parser()
    args = parser.parse_args()
    try:
        client = AtlassianClient.from_product("jira")
        print(args.func(client, args))
    except AtlassianClientError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
