import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict

_RESERVED_LOG_ATTRIBUTES = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "message",
}

_LOGGER_CONFIGURED = False


def _stringify(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (list, dict)):
        try:
            json.dumps(value)
            return value
        except TypeError:
            return str(value)
    return str(value)


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(timespec="milliseconds") + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_record["stack"] = self.formatStack(record.stack_info)

        for key, value in record.__dict__.items():
            if key in _RESERVED_LOG_ATTRIBUTES or key.startswith("_"):
                continue
            if value is None:
                continue
            log_record[key] = _stringify(value)

        return json.dumps(log_record, ensure_ascii=True)


def configure_logging(level: str | int | None = None) -> None:
    global _LOGGER_CONFIGURED
    if _LOGGER_CONFIGURED:
        return

    resolved_level: int = logging.INFO
    env_level = os.getenv("CRAWLER_LOG_LEVEL")

    if isinstance(level, str):
        level = level.strip().upper()
        resolved_level = getattr(logging, level, logging.INFO)
    elif isinstance(level, int):
        resolved_level = level

    if env_level:
        env_level = env_level.strip().upper()
        resolved_level = getattr(logging, env_level, resolved_level)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(_JsonFormatter())

    logging.basicConfig(level=resolved_level, handlers=[handler], force=True)
    _LOGGER_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
