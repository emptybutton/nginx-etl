from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    async def log_concurrent_etl(self) -> None: ...

    @abstractmethod
    async def log_successful_etl(
        self, *, loaded_log_count: int, loaded_log_batch_count: int
    ) -> None: ...
