#!/usr/bin/env python3
"""Shared Atlassian HTTP client with auth, retries, and payload helpers."""

from __future__ import annotations

import base64
import json
import logging
import mimetypes
import os
import random
import re
import shlex
import ssl
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib import error, parse, request

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
RETRYABLE_STATUS_CODES = {408, 409, 425, 429, 500, 502, 503, 504}
READ_ONLY_ALLOWED_METHODS = {"GET", "HEAD", "OPTIONS"}
WRITE_ENABLE_TOKEN = "I_UNDERSTAND"
OP_SECRET_REFERENCE_PREFIX = "op://"
ERROR_BODY_PREVIEW_LIMIT = 1000
SENSITIVE_KEY_MARKERS = (
    "accesstoken",
    "apikey",
    "authorization",
    "clientsecret",
    "cookie",
    "credential",
    "password",
    "privatekey",
    "refreshtoken",
    "secret",
    "session",
    "token",
)
SENSITIVE_TEXT_PATTERNS = (
    re.compile(r"(?i)\b(bearer|basic)\s+[a-z0-9._~+/=-]+\b"),
    re.compile(
        r"(?i)\b((?:api_)?token|access_token|refresh_token|password|secret|client_secret|authorization|cookie)\b(\s*[:=]\s*)([^\s,;\"'}]+)"
    ),
)


class AtlassianClientError(RuntimeError):
    """Raised when an Atlassian API request fails."""


@dataclass(frozen=True)
class AtlassianConfig:
    """Resolved configuration for one Atlassian product."""

    product: str
    base_url: str
    deployment: str
    username: str | None = field(repr=False)
    api_token: str = field(repr=False)
    ca_bundle: str | None = None
    insecure_skip_verify: bool = False
    timeout: int = DEFAULT_TIMEOUT
    retries: int = DEFAULT_RETRIES

    @property
    def is_cloud(self) -> bool:
        return self.deployment == "cloud"


def _env_candidates(product: str, suffix: str) -> list[str]:
    upper = product.upper()
    return [f"{upper}_{suffix}", f"ATLASSIAN_{suffix}"]


def _read_first_env(names: list[str]) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return _resolve_env_value(value.strip(), env_name=name)
    return None


def _parse_dotenv_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].strip()
    if "=" not in stripped:
        return None
    key, raw_value = stripped.split("=", 1)
    key = key.strip()
    if not key:
        return None

    value = raw_value.strip()
    if value and value[0] in {"'", '"'}:
        try:
            parsed = shlex.split(f"dotenv_value={value}", posix=True)
        except ValueError:
            stripped_value = value.strip("\"'")
            parsed = [f"dotenv_value={stripped_value}"]
        if parsed and "=" in parsed[0]:
            value = parsed[0].split("=", 1)[1]
    else:
        value = value.split(" #", 1)[0].strip()
    return key, value


def _dotenv_search_paths() -> list[Path]:
    current = Path.cwd().resolve()
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent.resolve()
    paths: list[Path] = [current]

    if current == skill_root or skill_root in current.parents:
        cursor = current
        while cursor != skill_root:
            cursor = cursor.parent
            if cursor not in paths:
                paths.append(cursor)
    elif skill_root not in paths:
        paths.append(skill_root)

    return paths


def load_dotenv_if_present(filename: str = ".env") -> Path | None:
    """Load the nearest .env file without overriding existing environment variables."""

    for directory in _dotenv_search_paths():
        candidate = directory / filename
        if not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            parsed = _parse_dotenv_line(line)
            if parsed is None:
                continue
            key, value = parsed
            os.environ.setdefault(key, value)
        return candidate
    return None


def _enforce_read_only(method: str, path: str) -> None:
    normalized_method = method.upper()
    if normalized_method in READ_ONLY_ALLOWED_METHODS:
        return
    read_only_value = os.getenv("ATLASSIAN_READ_ONLY", "true").strip().lower()
    writes_enabled = os.getenv("ATLASSIAN_ENABLE_WRITES", "").strip()
    read_only_disabled = read_only_value in {"false", "0", "no", "off"}
    if read_only_disabled and writes_enabled == WRITE_ENABLE_TOKEN:
        return
    raise AtlassianClientError(
        "Read-only mode is enforced for this skill. "
        f"Blocked {normalized_method} request to '{path}'. "
        "To enable writes intentionally, set ATLASSIAN_READ_ONLY=false "
        f"and ATLASSIAN_ENABLE_WRITES={WRITE_ENABLE_TOKEN}."
    )


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _ssl_ca_bundle() -> str | None:
    return _read_first_env(
        [
            "ATLASSIAN_CA_BUNDLE",
            "REQUESTS_CA_BUNDLE",
            "SSL_CERT_FILE",
        ]
    )


def _resolve_env_value(value: str, *, env_name: str) -> str:
    if not value.startswith(OP_SECRET_REFERENCE_PREFIX):
        return value

    try:
        result = subprocess.run(
            ["op", "read", value],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise AtlassianClientError(
            f"{env_name} uses a 1Password secret reference, but the 'op' CLI is not installed or not on PATH."
        ) from exc

    if result.returncode != 0:
        stderr = (
            _sanitize_text(result.stderr.strip()) if result.stderr else "unknown error"
        )
        raise AtlassianClientError(
            f"Failed to resolve 1Password secret reference in {env_name}: {stderr}"
        )

    return result.stdout.rstrip("\r\n")


def load_config(product: str) -> AtlassianConfig:
    """Load product configuration from environment variables."""

    load_dotenv_if_present()
    base_url = _read_first_env(_env_candidates(product, "URL"))
    username = _read_first_env(_env_candidates(product, "USERNAME"))
    api_token = _read_first_env(_env_candidates(product, "API_TOKEN"))
    deployment = os.getenv("ATLASSIAN_DEPLOYMENT", "").strip().lower()
    ca_bundle = _ssl_ca_bundle()
    insecure_skip_verify = _env_bool("ATLASSIAN_INSECURE_SKIP_VERIFY", default=False)
    timeout = int(os.getenv("ATLASSIAN_TIMEOUT", str(DEFAULT_TIMEOUT)))
    retries = int(os.getenv("ATLASSIAN_RETRIES", str(DEFAULT_RETRIES)))

    if not base_url:
        raise AtlassianClientError(
            f"Missing {product.upper()}_URL or ATLASSIAN_URL environment variable."
        )
    if not api_token:
        raise AtlassianClientError(
            f"Missing {product.upper()}_API_TOKEN or ATLASSIAN_API_TOKEN environment variable."
        )

    normalized_url = base_url.rstrip("/")
    parsed_base_url = parse.urlparse(normalized_url)
    if parsed_base_url.scheme not in {"http", "https"} or not parsed_base_url.netloc:
        raise AtlassianClientError(
            f"{product.upper()}_URL must be a valid absolute http(s) URL."
        )
    if parsed_base_url.username or parsed_base_url.password:
        raise AtlassianClientError(f"{product.upper()}_URL must not embed credentials.")
    if parsed_base_url.query or parsed_base_url.fragment:
        raise AtlassianClientError(
            f"{product.upper()}_URL must not include a query string or fragment."
        )
    if not deployment:
        host = parsed_base_url.netloc.casefold()
        deployment = "cloud" if host.endswith("atlassian.net") else "server"

    if deployment not in {"cloud", "server"}:
        raise AtlassianClientError(
            "ATLASSIAN_DEPLOYMENT must be either 'cloud' or 'server'."
        )

    if deployment == "cloud" and not username:
        raise AtlassianClientError(
            f"Missing {product.upper()}_USERNAME or ATLASSIAN_USERNAME for Cloud auth."
        )

    return AtlassianConfig(
        product=product.lower(),
        base_url=normalized_url,
        deployment=deployment,
        username=username,
        api_token=api_token,
        ca_bundle=ca_bundle,
        insecure_skip_verify=insecure_skip_verify,
        timeout=timeout,
        retries=retries,
    )


def load_json_file(path: str | os.PathLike[str]) -> dict[str, Any]:
    """Load and validate a JSON object from disk."""

    payload_path = Path(path)
    try:
        data = json.loads(payload_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AtlassianClientError(f"Payload file not found: {payload_path}") from exc
    except json.JSONDecodeError as exc:
        raise AtlassianClientError(
            f"Payload file is not valid JSON: {payload_path} ({exc})"
        ) from exc

    if not isinstance(data, dict):
        raise AtlassianClientError("Payload file must contain a JSON object.")
    return data


def dump_output(data: Any, *, fmt: str = "json") -> str:
    """Render JSON or markdown output."""

    if fmt == "json":
        return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)
    if fmt == "markdown":
        if isinstance(data, str):
            return data
        return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
    raise AtlassianClientError(f"Unsupported output format: {fmt}")


def _encode_basic_auth(username: str, api_token: str) -> str:
    raw = f"{username}:{api_token}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def _json_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _merge_query(url: str, query: dict[str, Any] | None) -> str:
    if not query:
        return url
    filtered = {key: value for key, value in query.items() if value is not None}
    encoded = parse.urlencode(filtered, doseq=True)
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{encoded}" if encoded else url


def _is_sensitive_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", key.casefold())
    return any(marker in normalized for marker in SENSITIVE_KEY_MARKERS)


def _sanitize_text(value: str) -> str:
    sanitized = value
    sanitized = SENSITIVE_TEXT_PATTERNS[0].sub(
        lambda match: f"{match.group(1)} <redacted>",
        sanitized,
    )
    sanitized = SENSITIVE_TEXT_PATTERNS[1].sub(
        lambda match: f"{match.group(1)}{match.group(2)}<redacted>",
        sanitized,
    )
    if len(sanitized) > ERROR_BODY_PREVIEW_LIMIT:
        return f"{sanitized[:ERROR_BODY_PREVIEW_LIMIT]}... [truncated]"
    return sanitized


def _sanitize_error_value(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            sanitized[key] = (
                "<redacted>" if _is_sensitive_key(key) else _sanitize_error_value(item)
            )
        return sanitized
    if isinstance(value, list):
        return [_sanitize_error_value(item) for item in value]
    if isinstance(value, str):
        return _sanitize_text(value)
    return value


def _build_multipart_body(
    fields: dict[str, str] | None,
    files: dict[str, str | os.PathLike[str]],
) -> tuple[bytes, str]:
    boundary = f"----AtlassianSkill{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    def append_line(value: bytes) -> None:
        chunks.append(value + b"\r\n")

    def sanitize_header_value(value: str, label: str) -> str:
        if "\r" in value or "\n" in value:
            raise AtlassianClientError(
                f"{label} must not contain carriage returns or newlines."
            )
        return value.replace("\\", "\\\\").replace('"', '\\"')

    for name, value in (fields or {}).items():
        safe_name = sanitize_header_value(name, "Multipart field name")
        append_line(f"--{boundary}".encode("utf-8"))
        append_line(
            f'Content-Disposition: form-data; name="{safe_name}"'.encode("utf-8")
        )
        append_line(b"")
        append_line(str(value).encode("utf-8"))

    for name, file_path in files.items():
        path = Path(file_path)
        if not path.exists():
            raise AtlassianClientError(f"Attachment file not found: {path}")
        safe_name = sanitize_header_value(name, "Multipart field name")
        safe_filename = sanitize_header_value(path.name, "Attachment filename")
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        append_line(f"--{boundary}".encode("utf-8"))
        append_line(
            (
                f'Content-Disposition: form-data; name="{safe_name}"; '
                f'filename="{safe_filename}"'
            ).encode("utf-8")
        )
        append_line(f"Content-Type: {mime_type}".encode("utf-8"))
        append_line(b"")
        chunks.append(path.read_bytes())
        chunks.append(b"\r\n")

    append_line(f"--{boundary}--".encode("utf-8"))
    return b"".join(chunks), boundary


def _default_ssl_context() -> ssl.SSLContext:
    """Build an SSL context that works reliably on macOS.

    Python on macOS does not use the system Keychain by default, so
    ``ssl.create_default_context()`` may fail to verify certificates.
    When the ``certifi`` package is available, its CA bundle is used
    automatically — the same strategy the ``requests`` library uses.
    Verification is never skipped.
    """
    try:
        import certifi  # type: ignore[import-untyped]

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


class AtlassianClient:
    """HTTP client for Jira or Confluence."""

    def __init__(self, config: AtlassianConfig):
        self.config = config
        self.ssl_context = self._build_ssl_context()
        self._base_url = parse.urlparse(self.config.base_url)

    @classmethod
    def from_product(cls, product: str) -> "AtlassianClient":
        """Build a client from environment-based product configuration."""

        return cls(load_config(product))

    def build_url(self, path: str) -> str:
        """Resolve a request path against the configured Atlassian base URL."""

        if path.startswith("http://") or path.startswith("https://"):
            parsed_path = parse.urlparse(path)
            if parsed_path.username or parsed_path.password:
                raise AtlassianClientError(
                    "Absolute request URLs must not embed credentials."
                )
            if (
                parsed_path.scheme != self._base_url.scheme
                or parsed_path.netloc.casefold() != self._base_url.netloc.casefold()
            ):
                raise AtlassianClientError(
                    "Absolute request URLs must stay within the configured Atlassian origin."
                )
            return path
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _build_ssl_context(self) -> ssl.SSLContext:
        if self.config.insecure_skip_verify:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            return ssl_context
        if self.config.ca_bundle:
            return ssl.create_default_context(cafile=self.config.ca_bundle)
        return _default_ssl_context()

    def _build_headers(
        self, extra_headers: dict[str, str] | None = None
    ) -> dict[str, str]:
        headers = _json_headers()
        if self.config.is_cloud:
            assert self.config.username is not None
            headers["Authorization"] = (
                f"Basic {_encode_basic_auth(self.config.username, self.config.api_token)}"
            )
        else:
            headers["Authorization"] = f"Bearer {self.config.api_token}"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def request_json(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        payload: dict[str, Any] | list[Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Send an HTTP request and decode the response body as JSON."""

        body = None if payload is None else json.dumps(payload).encode("utf-8")
        response = self.request(
            method,
            path,
            query=query,
            body=body,
            headers=headers,
        )
        if not response:
            return {}
        try:
            return json.loads(response)
        except json.JSONDecodeError as exc:
            raise AtlassianClientError("Response body was not valid JSON.") from exc

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> str:
        """Send an HTTP request and return the decoded response body."""

        _enforce_read_only(method, path)
        url = _merge_query(self.build_url(path), query)
        request_headers = self._build_headers(headers)

        if body is None:
            request_headers.pop("Content-Type", None)

        last_error: Exception | None = None
        for attempt in range(self.config.retries + 1):
            req = request.Request(
                url=url,
                data=body,
                headers=request_headers,
                method=method.upper(),
            )
            try:
                with request.urlopen(
                    req,
                    timeout=self.config.timeout,
                    context=self.ssl_context,
                ) as response:
                    return response.read().decode("utf-8")
            except error.HTTPError as exc:
                last_error = self._build_http_error(exc)
                if (
                    exc.code not in RETRYABLE_STATUS_CODES
                    or attempt >= self.config.retries
                ):
                    raise last_error from exc
                self._sleep_before_retry(
                    attempt, retry_after=exc.headers.get("Retry-After")
                )
            except ssl.SSLCertVerificationError as exc:
                raise AtlassianClientError(
                    "TLS certificate verification failed. "
                    "Set ATLASSIAN_CA_BUNDLE to a trusted CA bundle path, or set "
                    "ATLASSIAN_INSECURE_SKIP_VERIFY=true only for temporary testing."
                ) from exc
            except error.URLError as exc:
                last_error = AtlassianClientError(f"Connection error: {exc.reason}")
                if attempt >= self.config.retries:
                    raise last_error from exc
                self._sleep_before_retry(attempt, retry_after=None)

        if last_error is not None:
            raise last_error
        raise AtlassianClientError("Request failed without an explicit error.")

    def upload_file(
        self,
        path: str,
        *,
        file_field_name: str,
        file_path: str | os.PathLike[str],
        fields: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Upload a multipart file payload and decode the JSON response."""

        _enforce_read_only("POST", path)
        body, boundary = _build_multipart_body(fields, {file_field_name: file_path})
        merged_headers = {
            "Accept": "application/json",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
        if headers:
            merged_headers.update(headers)
        response = self.request("POST", path, body=body, headers=merged_headers)
        if not response:
            return {}
        return json.loads(response)

    @staticmethod
    def _sleep_before_retry(attempt: int, retry_after: str | None) -> None:
        if retry_after and retry_after.isdigit():
            delay = float(retry_after)
        else:
            base_delay = min(2**attempt, 8)
            delay = base_delay + random.uniform(0, 0.25)
        logger.warning("Retrying after %.2fs", delay)
        time.sleep(delay)

    @staticmethod
    def _build_http_error(exc: error.HTTPError) -> AtlassianClientError:
        body = exc.read().decode("utf-8", errors="replace")
        parsed_url = parse.urlparse(exc.url)
        sanitized_target = parsed_url.path or "<unknown endpoint>"
        message = f"HTTP {exc.code} for {sanitized_target}"
        if body:
            try:
                parsed = json.loads(body)
                rendered = json.dumps(
                    _sanitize_error_value(parsed),
                    ensure_ascii=False,
                )
            except json.JSONDecodeError:
                rendered = _sanitize_text(body)
            message = f"{message}: {rendered}"
        return AtlassianClientError(message)
