from abc import ABC, abstractmethod
from collections.abc import Sequence

from nginx_etl.entities.transformed_nginx_log import TransformedNginxLog


class TransformedNginxLogStorage(ABC):
    @abstractmethod
    async def load(
        self, transformed_nginx_logs: Sequence[TransformedNginxLog]
    ) -> None: ...
