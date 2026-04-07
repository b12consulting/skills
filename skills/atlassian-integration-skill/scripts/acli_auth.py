#!/usr/bin/env python3
"""Authenticate the Atlassian CLI (acli) using the same 1Password-backed
credentials that the Confluence scripts use.

This script reuses ``auth_client.load_config("jira")`` so that environment
variables such as ``JIRA_URL``, ``JIRA_USERNAME``, ``JIRA_API_TOKEN`` (with
``ATLASSIAN_*`` fallbacks) are resolved through the standard dotenv loading
and 1Password ``op://`` secret reference resolution.

Usage
-----
::

    python scripts/acli_auth.py            # authenticate acli for Jira
    python scripts/acli_auth.py --status   # check current acli auth status

With 1Password wrapper::

    scripts/run_with_1password.sh python scripts/acli_auth.py
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from urllib.parse import urlparse

from auth_client import AtlassianClientError, load_config


def _extract_site(base_url: str) -> str:
    """Return the host portion of the Jira base URL for ``acli --site``."""
    return urlparse(base_url).netloc


def _check_acli_installed() -> None:
    """Ensure the ``acli`` binary is available on ``PATH``."""
    try:
        subprocess.run(
            ["acli", "--help"],
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise AtlassianClientError(
            "The Atlassian CLI 'acli' is required but was not found on PATH. "
            "Install it from https://developer.atlassian.com/cloud/acli/guides/introduction/"
        ) from exc


def authenticate(*, verbose: bool = False) -> None:
    """Log in to acli using the resolved Jira credentials."""
    _check_acli_installed()

    config = load_config("jira")
    site = _extract_site(config.base_url)

    if not config.username:
        raise AtlassianClientError(
            "JIRA_USERNAME or ATLASSIAN_USERNAME is required for acli authentication."
        )

    cmd = [
        "acli",
        "jira",
        "auth",
        "login",
        "--site",
        site,
        "--email",
        config.username,
        "--token",
    ]

    if verbose:
        print(f"Authenticating acli for site: {site}", file=sys.stderr)

    result = subprocess.run(
        cmd,
        input=config.api_token,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "unknown error"
        raise AtlassianClientError(f"acli auth login failed: {stderr}")

    if result.stdout.strip():
        print(result.stdout.strip())
    if verbose and result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    print(f"Successfully authenticated acli for {site}.", file=sys.stderr)


def check_status() -> None:
    """Print the current acli authentication status."""
    _check_acli_installed()
    result = subprocess.run(
        ["acli", "jira", "auth", "status"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    raise SystemExit(result.returncode)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Authenticate the Atlassian CLI (acli) using 1Password-backed credentials."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check current acli auth status instead of logging in.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print additional diagnostic output.",
    )
    return parser


def main() -> int:
    """Run the acli authentication helper."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            check_status()
        else:
            authenticate(verbose=args.verbose)
    except AtlassianClientError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
