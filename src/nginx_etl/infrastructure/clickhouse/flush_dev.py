from dataclasses import dataclass

from clickhouse_connect.driver.asyncclient import AsyncClient as ClickHouse


@dataclass(kw_only=True, frozen=True, slots=True)
class FlushDevClickHouse:
    clickhouse: ClickHouse

    async def __call__(self) -> None:
        await self.clickhouse.command("TRUNCATE TABLE nginx_logs")
