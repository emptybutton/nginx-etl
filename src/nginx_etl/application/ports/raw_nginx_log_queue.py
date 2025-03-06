from abc import ABC, abstractmethod
from collections.abc import AsyncIterable, Sequence
from contextlib import AbstractAsyncContextManager

from nginx_etl.entities.raw_nginx_log import RawNginxLog


type PulledCommitableRawNginxLogBatches = (
    AbstractAsyncContextManager[AsyncIterable[Sequence[RawNginxLog]]]
)


class RawNginxLogQueue(ABC):
    @abstractmethod
    def pull_commitable_batches(
        self
    ) -> PulledCommitableRawNginxLogBatches: ...
