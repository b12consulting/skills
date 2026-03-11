"""
logging-config.py — Reference logging configuration for Python services.

Demonstrates two patterns:
  1. Basic structured logging using the stdlib `logging` module with a JSON
     formatter (zero extra dependencies).
  2. Structured logging with `structlog` (recommended for production services).

Usage
-----
Copy the relevant section into your application's entry point (e.g. main.py,
cli.py, or the WSGI/ASGI app factory).  Call the setup function exactly once
at startup — never inside library code or individual modules.

In library / module code, always obtain a logger like this:

    import logging
    logger = logging.getLogger(__name__)

Do NOT call basicConfig() or add handlers in library modules.
"""

from __future__ import annotations

import json
import logging
import logging.config
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Pattern 1 — stdlib JSON formatter (no extra dependencies)
# ---------------------------------------------------------------------------

class JsonFormatter(logging.Formatter):
    """Format log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        # Merge any extra fields passed via logger.info("msg", extra={"key": val})
        for key, value in record.__dict__.items():
            if key not in logging.LogRecord.__dict__ and not key.startswith("_"):
                payload[key] = value
        return json.dumps(payload, default=str)


def setup_stdlib_logging(level: str = "INFO") -> None:
    """Configure stdlib logging with a JSON formatter.

    Call once at application startup.

    Args:
        level: Minimum log level to emit (e.g. "DEBUG", "INFO", "WARNING").
    """
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "json",
                },
            },
            "root": {
                "level": level,
                "handlers": ["stdout"],
            },
        }
    )


# ---------------------------------------------------------------------------
# Pattern 2 — structlog (recommended for production services)
# Requires:  pip install structlog
# ---------------------------------------------------------------------------

def setup_structlog(level: str = "INFO") -> None:
    """Configure structlog for structured, context-rich logging.

    Call once at application startup.

    Args:
        level: Minimum log level to emit.

    Example usage in modules::

        import structlog
        logger = structlog.get_logger()

        logger.info("processing_started", records=len(records), source=source)
        logger.warning("missing_field", field="email", record_id=record.id)
        logger.error("fetch_failed", url=url, status=resp.status_code)
    """
    try:
        import structlog
    except ImportError as exc:
        raise ImportError(
            "structlog is required for this configuration. "
            "Install it with: pip install structlog"
        ) from exc

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


# ---------------------------------------------------------------------------
# Example — run this file directly to see sample output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Demonstrate stdlib JSON logging
    setup_stdlib_logging(level="DEBUG")
    log = logging.getLogger("example")

    log.debug("debug message", extra={"request_id": "abc-123"})
    log.info("server started", extra={"port": 8080})
    log.warning("high memory usage", extra={"used_mb": 950, "limit_mb": 1024})

    try:
        raise ValueError("something went wrong")
    except ValueError:
        log.exception("unhandled error")
