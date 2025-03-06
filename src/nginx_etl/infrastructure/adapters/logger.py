from nginx_etl.application.ports.logger import Logger
from nginx_etl.infrastructure.structlog.loggers import human_readable_logger


class HumanReadableLogger(Logger):
    async def log_concurrent_etl(self) -> None:
        await human_readable_logger.aerror("concurrent etl")

    async def log_successful_etl(
        self,
        *,
        loaded_log_count: int,
        loaded_log_batch_count: int,
    ) -> None:
        await human_readable_logger.ainfo(
            "successful etl",
            loaded_log_count=loaded_log_count,
            loaded_log_batch_count=loaded_log_batch_count,
        )
