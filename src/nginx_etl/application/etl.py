from dataclasses import dataclass

from nginx_etl.application.ports.logger import Logger
from nginx_etl.application.ports.optimistic_lock import (
    OptimisticLockActor,
    OptimisticLockWhen,
)
from nginx_etl.application.ports.raw_nginx_log_queue import RawNginxLogQueue
from nginx_etl.application.ports.transformed_nginx_log_storage import (
    TransformedNginxLogStorage,
)
from nginx_etl.entities.transformed_nginx_log import transformed


class ConcurrentEtlError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Etl:
    """
    :raises nginx_etl.application.etl.ConcurrentEtlError:
    """

    raw_nginx_log_queue: RawNginxLogQueue
    transformed_nginx_log_storage: TransformedNginxLogStorage
    optimistic_lock_when: OptimisticLockWhen
    logger: Logger

    async def __call__(self) -> None:
        commitable_raw_log_batches = (
            self.raw_nginx_log_queue.pull_commitable_batches()
        )
        lock = self.optimistic_lock_when(actor=OptimisticLockActor.etl)

        async with lock as active_lock:
            if not active_lock.is_owned:
                await self.logger.log_concurrent_etl()
                raise ConcurrentEtlError

            async with commitable_raw_log_batches as raw_log_batches:
                loaded_log_batch_count = 0
                loaded_log_count = 0

                async for raw_log_batch in raw_log_batches:
                    transformed_log_batch = (
                        tuple(map(transformed, raw_log_batch))
                    )

                    await self.transformed_nginx_log_storage.load(
                        transformed_log_batch
                    )

                    loaded_log_batch_count += 1
                    loaded_log_count += len(transformed_log_batch)

        await self.logger.log_successful_etl(
            loaded_log_batch_count=loaded_log_batch_count,
            loaded_log_count=loaded_log_count,
        )
