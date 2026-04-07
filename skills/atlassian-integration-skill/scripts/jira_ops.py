#!/usr/bin/env python3
"""CLI wrapper for Jira operations via the Atlassian CLI (acli).

Provides a consistent interface matching the ``confluence_ops.py`` pattern.
Handles authentication checks (with auto-login from 1Password credentials),
correct acli command syntax, read-only enforcement, and JSON output.

Usage
-----
::

    python scripts/jira_ops.py view --key DEMO-123
    python scripts/jira_ops.py search --jql 'project = DEMO' --limit 10
    python scripts/jira_ops.py create --project DEMO --type Task --summary "New task"
    python scripts/jira_ops.py edit --key DEMO-123 --summary "Updated summary"
    python scripts/jira_ops.py transition --key DEMO-123 --status "In Progress"
    python scripts/jira_ops.py comment --key DEMO-123 --body "Agent review complete."
    python scripts/jira_ops.py assign --key DEMO-123 --assignee "user@example.com"
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

# ---------------------------------------------------------------------------
# Read-only enforcement (mirrors auth_client._enforce_read_only)
# ---------------------------------------------------------------------------

WRITE_ENABLE_TOKEN = "I_UNDERSTAND"
WRITE_COMMANDS = {"create", "edit", "transition", "comment", "assign"}


def _enforce_read_only(command: str) -> None:
    if command not in WRITE_COMMANDS:
        return
    read_only_value = os.getenv("ATLASSIAN_READ_ONLY", "true").strip().lower()
    writes_enabled = os.getenv("ATLASSIAN_ENABLE_WRITES", "").strip()
    read_only_disabled = read_only_value in {"false", "0", "no", "off"}
    if read_only_disabled and writes_enabled == WRITE_ENABLE_TOKEN:
        return
    raise SystemExit(
        f"Error: Read-only mode is enforced. Blocked write command '{command}'.\n"
        "To enable writes, set ATLASSIAN_READ_ONLY=false "
        f"and ATLASSIAN_ENABLE_WRITES={WRITE_ENABLE_TOKEN}."
    )


# ---------------------------------------------------------------------------
# acli helpers
# ---------------------------------------------------------------------------


class AcliError(RuntimeError):
    """Raised when an acli command fails."""


def _run_acli(*args: str, input_text: str | None = None) -> str:
    """Run an acli command and return stdout."""
    cmd = ["acli", *args]
    try:
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise AcliError(
            "The Atlassian CLI 'acli' is required but was not found on PATH. "
            "Install it from https://developer.atlassian.com/cloud/acli/guides/introduction/"
        ) from exc

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else ""
        stdout = result.stdout.strip() if result.stdout else ""
        detail = stderr or stdout or f"acli exited with code {result.returncode}"
        raise AcliError(detail)

    return result.stdout


def _is_authenticated() -> bool:
    """Return True if acli already has a valid Jira session."""
    try:
        result = subprocess.run(
            ["acli", "jira", "auth", "status"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _ensure_authenticated() -> None:
    """Check acli auth status; auto-authenticate using 1Password credentials."""
    if _is_authenticated():
        return

    # Auto-login using the same credential resolution as Confluence
    try:
        from acli_auth import authenticate

        print("acli not authenticated — auto-logging in…", file=sys.stderr)
        authenticate()
    except Exception as exc:
        raise AcliError(
            f"acli is not authenticated and auto-login failed: {exc}\n"
            "Run manually: python scripts/acli_auth.py"
        ) from exc


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def command_view(args: argparse.Namespace) -> str:
    cmd = ["jira", "workitem", "view", args.key]
    if args.fields:
        cmd += ["--fields", args.fields]
    if args.json:
        cmd.append("--json")
    return _run_acli(*cmd)


def command_search(args: argparse.Namespace) -> str:
    cmd = ["jira", "workitem", "search", "--jql", args.jql]
    if args.limit:
        cmd += ["--limit", str(args.limit)]
    if args.fields:
        cmd += ["--fields", args.fields]
    if args.json:
        cmd.append("--json")
    return _run_acli(*cmd)


def command_create(args: argparse.Namespace) -> str:
    if args.from_json:
        return _run_acli("jira", "workitem", "create", "--from-json", args.from_json)
    cmd = [
        "jira", "workitem", "create",
        "--project", args.project,
        "--type", args.type,
        "--summary", args.summary,
    ]
    if args.description:
        cmd += ["--description", args.description]
    if args.assignee:
        cmd += ["--assignee", args.assignee]
    if args.label:
        cmd += ["--label", args.label]
    if args.parent:
        cmd += ["--parent", args.parent]
    if args.json:
        cmd.append("--json")
    return _run_acli(*cmd)


def command_edit(args: argparse.Namespace) -> str:
    if args.from_json:
        return _run_acli("jira", "workitem", "edit", "--from-json", args.from_json)
    cmd = ["jira", "workitem", "edit", "--key", args.key]
    if args.summary:
        cmd += ["--summary", args.summary]
    if args.description:
        cmd += ["--description", args.description]
    if args.assignee:
        cmd += ["--assignee", args.assignee]
    if args.labels:
        cmd += ["--labels", args.labels]
    if args.type:
        cmd += ["--type", args.type]
    if args.json:
        cmd.append("--json")
    cmd.append("--yes")
    return _run_acli(*cmd)


def command_transition(args: argparse.Namespace) -> str:
    cmd = [
        "jira", "workitem", "transition",
        "--key", args.key,
        "--status", args.status,
        "--yes",
    ]
    if args.json:
        cmd.append("--json")
    return _run_acli(*cmd)


def command_comment(args: argparse.Namespace) -> str:
    cmd = [
        "jira", "workitem", "comment", "create",
        "--key", args.key,
        "--body", args.body,
    ]
    if args.json:
        cmd.append("--json")
    return _run_acli(*cmd)


def command_assign(args: argparse.Namespace) -> str:
    cmd = [
        "jira", "workitem", "assign",
        "--key", args.key,
        "--assignee", args.assignee,
        "--yes",
    ]
    if args.json:
        cmd.append("--json")
    return _run_acli(*cmd)


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Jira operations via acli with auto-auth and read-only enforcement."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- view --
    view = subparsers.add_parser("view", help="View a Jira work item")
    view.add_argument("--key", required=True, help="Work item key (e.g. DEMO-123)")
    view.add_argument(
        "--fields", default="*all",
        help="Comma-separated fields (default: *all)",
    )
    view.add_argument(
        "--json", action="store_true", default=True,
        help="JSON output (default: on)",
    )
    view.set_defaults(func=command_view)

    # -- search --
    search = subparsers.add_parser("search", help="Search work items with JQL")
    search.add_argument("--jql", required=True, help="JQL query string")
    search.add_argument("--limit", type=int, default=10, help="Max results")
    search.add_argument("--fields", default=None, help="Comma-separated fields")
    search.add_argument("--json", action="store_true", default=True, help="JSON output")
    search.set_defaults(func=command_search)

    # -- create --
    create = subparsers.add_parser("create", help="Create a Jira work item")
    create.add_argument("--project", help="Project key (e.g. DEMO)")
    create.add_argument("--type", help="Work item type (e.g. Task, Bug, Story)")
    create.add_argument("--summary", help="Summary text")
    create.add_argument("--description", default=None, help="Description text or ADF")
    create.add_argument("--assignee", default=None, help="Assignee email or @me")
    create.add_argument("--label", default=None, help="Comma-separated labels")
    create.add_argument("--parent", default=None, help="Parent work item key")
    create.add_argument("--from-json", default=None, help="Create from JSON file")
    create.add_argument("--json", action="store_true", default=True, help="JSON output")
    create.set_defaults(func=command_create)

    # -- edit --
    edit = subparsers.add_parser("edit", help="Edit a Jira work item")
    edit.add_argument("--key", required=True, help="Work item key")
    edit.add_argument("--summary", default=None, help="New summary")
    edit.add_argument("--description", default=None, help="New description")
    edit.add_argument("--assignee", default=None, help="New assignee email")
    edit.add_argument("--labels", default=None, help="New labels")
    edit.add_argument("--type", default=None, help="New work item type")
    edit.add_argument("--from-json", default=None, help="Edit from JSON file")
    edit.add_argument("--json", action="store_true", default=True, help="JSON output")
    edit.set_defaults(func=command_edit)

    # -- transition --
    transition = subparsers.add_parser("transition", help="Transition a work item")
    transition.add_argument("--key", required=True, help="Work item key")
    transition.add_argument("--status", required=True, help="Target status name")
    transition.add_argument(
        "--json", action="store_true", default=True, help="JSON output",
    )
    transition.set_defaults(func=command_transition)

    # -- comment --
    comment = subparsers.add_parser("comment", help="Add a comment to a work item")
    comment.add_argument("--key", required=True, help="Work item key")
    comment.add_argument("--body", required=True, help="Comment body text")
    comment.add_argument(
        "--json", action="store_true", default=True, help="JSON output",
    )
    comment.set_defaults(func=command_comment)

    # -- assign --
    assign = subparsers.add_parser("assign", help="Assign a work item")
    assign.add_argument("--key", required=True, help="Work item key")
    assign.add_argument(
        "--assignee", required=True, help="Assignee email, @me, or default",
    )
    assign.add_argument(
        "--json", action="store_true", default=True, help="JSON output",
    )
    assign.set_defaults(func=command_assign)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        _enforce_read_only(args.command)
        _ensure_authenticated()
        output = args.func(args)
        if output and output.strip():
            print(output.strip())
    except AcliError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
