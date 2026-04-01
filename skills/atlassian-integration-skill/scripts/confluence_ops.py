#!/usr/bin/env python3
"""CLI wrappers for Confluence REST API operations."""

from __future__ import annotations

import argparse
import json
from html import escape
from html.parser import HTMLParser
from typing import Any

from auth_client import (
    AtlassianClient,
    AtlassianClientError,
    dump_output,
    load_json_file,
)

TEXT_BLOCK_NODE_TYPES = {
    "paragraph",
    "heading",
    "blockquote",
    "listItem",
    "tableCell",
    "tableHeader",
}
CONTAINER_NODE_TYPES = {"bulletList", "orderedList", "table", "tableRow", "doc"}


def _join_extracted_text(items: list[Any]) -> str:
    return "\n".join(part for part in (adf_to_text(item) for item in items) if part)


def search_path() -> str:
    """Return the Confluence search endpoint."""

    return "rest/api/search"


def page_path(client: AtlassianClient, page_id: str | None = None) -> str:
    """Return the page endpoint for the configured Confluence deployment."""

    if client.config.is_cloud:
        base = "api/v2/pages"
    else:
        base = "rest/api/content"
    return f"{base}/{page_id}" if page_id else base


def footer_comment_path(client: AtlassianClient, page_id: str) -> str:
    """Return the footer comment endpoint for a page."""

    if client.config.is_cloud:
        return f"api/v2/pages/{page_id}/footer-comments"
    return f"rest/api/content/{page_id}/child/comment"


def attachment_path(client: AtlassianClient, page_id: str) -> str:
    """Return the attachment endpoint for a page."""

    if client.config.is_cloud:
        return f"api/v2/pages/{page_id}/attachments"
    return f"rest/api/content/{page_id}/child/attachment"


def build_page_markdown(page: dict[str, Any]) -> str:
    """Render a compact markdown summary for a Confluence page."""

    version_info = page.get("version")
    title = page.get("title", "(no title)")
    page_id = page.get("id", "Unknown")
    version = (
        version_info.get("number") if isinstance(version_info, dict) else "Unknown"
    )
    space_value = (
        page.get("spaceId")
        or (page.get("space") or {}).get("key")
        or (page.get("space") or {}).get("id")
        or "Unknown"
    )
    updated = (
        page.get("updatedAt") or (version_info or {}).get("createdAt") or "Unknown"
    )

    return "\n".join(
        [
            "## Confluence Page Summary",
            "",
            f"- Title: {title}",
            f"- Page ID: {page_id}",
            f"- Space: {space_value}",
            f"- Version: {version}",
            f"- Updated: {updated}",
            "",
            "### Contents",
            "Review the body payload for the authoritative content.",
        ]
    )


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return "\n".join(self.parts)


def strip_html_to_text(value: str) -> str:
    """Extract plain text from an HTML fragment."""

    parser = _HTMLTextExtractor()
    parser.feed(value)
    return parser.text()


def adf_to_text(node: Any) -> str:
    """Extract readable text from Atlassian Document Format content."""

    if isinstance(node, str):
        try:
            return adf_to_text(json.loads(node))
        except json.JSONDecodeError:
            return node
    if isinstance(node, list):
        return _join_extracted_text(node)
    if not isinstance(node, dict):
        return ""

    node_type = node.get("type")
    content = node.get("content", [])

    if node_type == "text":
        return node.get("text", "")
    if node_type in TEXT_BLOCK_NODE_TYPES:
        return _join_extracted_text(content)
    if node_type in CONTAINER_NODE_TYPES:
        return _join_extracted_text(content)
    if node_type == "codeBlock":
        return _join_extracted_text(content)

    return _join_extracted_text(content)


def extract_page_body_text(page: dict[str, Any]) -> str:
    """Extract readable text from common Confluence body payload shapes."""

    body = page.get("body")
    if not isinstance(body, dict):
        return ""

    # Confluence Cloud v2 often returns body as {"representation": "...", "value": "..."}
    if "representation" in body and "value" in body:
        representation = body.get("representation")
        value = body.get("value", "")
        if representation == "atlas_doc_format":
            return adf_to_text(value).strip()
        if representation == "storage":
            return strip_html_to_text(str(value)).strip()

    # Confluence Server/DC typically returns body.storage.value
    storage = body.get("storage")
    if isinstance(storage, dict) and "value" in storage:
        return strip_html_to_text(str(storage["value"])).strip()

    # Some Cloud payloads may nest atlas_doc_format data.
    atlas_doc = body.get("atlas_doc_format")
    if isinstance(atlas_doc, dict) and "value" in atlas_doc:
        return adf_to_text(atlas_doc["value"]).strip()

    return ""


def get_page(client: AtlassianClient, page_id: str) -> dict[str, Any]:
    """Fetch a page with the body fields required for text extraction."""

    if client.config.is_cloud:
        return client.request_json(
            "GET",
            page_path(client, page_id),
            query={"body-format": "atlas_doc_format"},
        )
    return client.request_json(
        "GET",
        page_path(client, page_id),
        query={"expand": "body.storage,version,space"},
    )


def command_search(client: AtlassianClient, args: argparse.Namespace) -> str:
    data = client.request_json(
        "GET",
        search_path(),
        query={
            "cql": args.cql,
            "limit": args.limit,
            "expand": args.expand,
        },
    )
    return dump_output(data, fmt=args.output)


def command_get(client: AtlassianClient, args: argparse.Namespace) -> str:
    data = get_page(client, args.page_id)
    if args.output in {"body", "markdown"}:
        body_text = extract_page_body_text(data)
        if not body_text:
            raise AtlassianClientError(
                "No readable page body was found in the Confluence response."
            )
        if args.output == "body":
            return body_text
        if args.include_body:
            return "\n\n".join([build_page_markdown(data), body_text])
        return build_page_markdown(data)
    return dump_output(data, fmt=args.output)


def command_create_page(client: AtlassianClient, args: argparse.Namespace) -> str:
    payload = load_json_file(args.payload_file)
    endpoint = page_path(client)
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "confluence_create_page",
                "endpoint": endpoint,
                "payload": payload,
            },
            fmt=args.output,
        )
    data = client.request_json("POST", endpoint, payload=payload)
    return dump_output(data, fmt=args.output)


def command_update_page(client: AtlassianClient, args: argparse.Namespace) -> str:
    payload = load_json_file(args.payload_file)
    current = get_page(client, args.page_id)
    merged_payload = merge_page_update_payload(client, args.page_id, current, payload)
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "confluence_update_page",
                "endpoint": page_path(client, args.page_id),
                "current_version": extract_version_number(current),
                "payload": merged_payload,
            },
            fmt=args.output,
        )
    data = client.request_json(
        "PUT",
        page_path(client, args.page_id),
        payload=merged_payload,
    )
    return dump_output(data, fmt=args.output)


def command_comment(client: AtlassianClient, args: argparse.Namespace) -> str:
    payload = build_comment_payload(client, args.text)
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "confluence_add_comment",
                "endpoint": footer_comment_path(client, args.page_id),
                "payload": payload,
            },
            fmt=args.output,
        )
    data = client.request_json(
        "POST",
        footer_comment_path(client, args.page_id),
        payload=payload,
    )
    return dump_output(data, fmt=args.output)


def command_list_attachments(client: AtlassianClient, args: argparse.Namespace) -> str:
    data = client.request_json(
        "GET",
        attachment_path(client, args.page_id),
        query={"limit": args.limit},
    )
    return dump_output(data, fmt=args.output)


def command_upload_attachment(client: AtlassianClient, args: argparse.Namespace) -> str:
    if args.dry_run:
        return dump_output(
            {
                "dry_run": True,
                "operation": "confluence_upload_attachment",
                "endpoint": attachment_path(client, args.page_id),
                "file": args.file,
                "comment": args.comment,
            },
            fmt=args.output,
        )
    data = client.upload_file(
        attachment_path(client, args.page_id),
        file_field_name="file",
        file_path=args.file,
        fields={"comment": args.comment} if args.comment else None,
        headers={"X-Atlassian-Token": "nocheck"},
    )
    return dump_output(data, fmt=args.output)


def merge_page_update_payload(
    client: AtlassianClient,
    page_id: str,
    current: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Merge the current page metadata needed for a safe update request."""

    next_version = extract_version_number(current) + 1
    merged = dict(payload)

    if client.config.is_cloud:
        merged.setdefault("id", page_id)
        merged.setdefault("status", current.get("status", "current"))
        merged["version"] = {"number": next_version}
    else:
        merged.setdefault("id", page_id)
        merged.setdefault("type", current.get("type", "page"))
        merged.setdefault("title", current.get("title"))
        merged["version"] = {"number": next_version}
        if "space" not in merged and current.get("space"):
            merged["space"] = current["space"]
    return merged


def extract_version_number(page: dict[str, Any]) -> int:
    """Return the current Confluence page version number."""

    version = page.get("version")
    if isinstance(version, dict) and isinstance(version.get("number"), int):
        return version["number"]
    raise AtlassianClientError("Unable to determine current Confluence page version.")


def build_comment_payload(client: AtlassianClient, text: str) -> dict[str, Any]:
    """Build the storage-format comment payload for the target deployment."""

    escaped_text = escape(text, quote=False)
    if client.config.is_cloud:
        return {
            "body": {
                "representation": "storage",
                "value": f"<p>{escaped_text}</p>",
            }
        }
    return {
        "type": "comment",
        "body": {
            "storage": {
                "value": f"<p>{escaped_text}</p>",
                "representation": "storage",
            }
        },
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the Confluence CLI argument parser."""

    parser = argparse.ArgumentParser(description="Confluence REST API helper CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search Confluence with CQL")
    search.add_argument("--cql", required=True, help="CQL query string")
    search.add_argument("--limit", type=int, default=10, help="Max results")
    search.add_argument("--expand", default=None, help="Optional v1 expand list")
    search.add_argument("--output", choices=("json", "markdown"), default="json")
    search.set_defaults(func=command_search)

    get_page_cmd = subparsers.add_parser("get", help="Get a Confluence page")
    get_page_cmd.add_argument("--page-id", required=True, help="Confluence page id")
    get_page_cmd.add_argument(
        "--include-body",
        action="store_true",
        help="Append readable page body when using markdown output",
    )
    get_page_cmd.add_argument(
        "--output", choices=("json", "markdown", "body"), default="body"
    )
    get_page_cmd.set_defaults(func=command_get)

    create_page = subparsers.add_parser("create-page", help="Create a Confluence page")
    create_page.add_argument("--payload-file", required=True, help="JSON payload file")
    create_page.add_argument("--dry-run", action="store_true", help="Validate only")
    create_page.add_argument("--output", choices=("json", "markdown"), default="json")
    create_page.set_defaults(func=command_create_page)

    update_page = subparsers.add_parser("update-page", help="Update a Confluence page")
    update_page.add_argument("--page-id", required=True, help="Confluence page id")
    update_page.add_argument("--payload-file", required=True, help="JSON payload file")
    update_page.add_argument("--dry-run", action="store_true", help="Validate only")
    update_page.add_argument("--output", choices=("json", "markdown"), default="json")
    update_page.set_defaults(func=command_update_page)

    comment = subparsers.add_parser("comment", help="Add a Confluence page comment")
    comment.add_argument("--page-id", required=True, help="Confluence page id")
    comment.add_argument("--text", required=True, help="Comment text")
    comment.add_argument("--dry-run", action="store_true", help="Validate only")
    comment.add_argument("--output", choices=("json", "markdown"), default="json")
    comment.set_defaults(func=command_comment)

    list_attachments = subparsers.add_parser(
        "list-attachments", help="List page attachments"
    )
    list_attachments.add_argument("--page-id", required=True, help="Confluence page id")
    list_attachments.add_argument("--limit", type=int, default=25, help="Max results")
    list_attachments.add_argument(
        "--output", choices=("json", "markdown"), default="json"
    )
    list_attachments.set_defaults(func=command_list_attachments)

    upload_attachment = subparsers.add_parser(
        "upload-attachment", help="Upload an attachment to a page"
    )
    upload_attachment.add_argument(
        "--page-id", required=True, help="Confluence page id"
    )
    upload_attachment.add_argument("--file", required=True, help="Path to file")
    upload_attachment.add_argument(
        "--comment", default=None, help="Optional attachment comment"
    )
    upload_attachment.add_argument(
        "--dry-run", action="store_true", help="Validate only"
    )
    upload_attachment.add_argument(
        "--output", choices=("json", "markdown"), default="json"
    )
    upload_attachment.set_defaults(func=command_upload_attachment)

    return parser


def main() -> int:
    """Run the Confluence CLI."""

    parser = build_parser()
    args = parser.parse_args()
    try:
        client = AtlassianClient.from_product("confluence")
        print(args.func(client, args))
    except AtlassianClientError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
