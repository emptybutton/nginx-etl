from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from clickhouse_connect.driver.asyncclient import AsyncClient as ClickHouse

from nginx_etl.application.ports.transformed_nginx_log_storage import (
    TransformedNginxLogStorage,
)
from nginx_etl.entities.transformed_nginx_log import TransformedNginxLog


@dataclass(kw_only=True, frozen=True, slots=True)
class ClickHouseTransformedNginxLogStorage(TransformedNginxLogStorage):
    clickhouse: ClickHouse

    async def load(
        self, transformed_nginx_logs: Sequence[TransformedNginxLog]
    ) -> None:
        await self.clickhouse.insert(
            "nginx_logs",
            [self._as_row(log) for log in transformed_nginx_logs],
        )

    def _as_row(self, log: TransformedNginxLog) -> tuple[Any, ...]:
        return (
            log.id,
            log.client_ipv4,
            log.client_ipv6,
            log.datetime,
            log.method,
            log.status_code,
            log.endpoint,
            log.protocol,
            log.user_agent,
        )
