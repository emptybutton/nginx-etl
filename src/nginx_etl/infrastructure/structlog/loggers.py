import structlog
from structlog.types import FilteringBoundLogger


human_readable_logger: FilteringBoundLogger = structlog.wrap_logger(
    structlog.PrintLogger(),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(
            fmt="iso", utc=True, key="current_time"
        ),
        structlog.dev.ConsoleRenderer(),
    ],
)
