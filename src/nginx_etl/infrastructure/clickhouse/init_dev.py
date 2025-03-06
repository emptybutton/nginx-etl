from dataclasses import dataclass

from clickhouse_connect.driver.asyncclient import AsyncClient as ClickHouse


@dataclass(kw_only=True, frozen=True, slots=True)
class InitDevClickHouse:
    clickhouse: ClickHouse

    async def __call__(self) -> None:
        await self.clickhouse.command("""
            CREATE TABLE IF NOT EXISTS nginx_logs(
                `id` UUID NOT NULL,
                PRIMARY KEY(`id`),
                `client_ipv4` IPv4 NULL,
                `client_ipv6` IPv6 NULL,
                `datetime` DateTime('UTC') NOT NULL,
                `method` String NOT NULL,
                `status_code` UInt16 NOT NULL,
                `endpoint` String NOT NULL,
                `protocol` String NOT NULL,
                `user_agent` String NOT NULL,
            )
        """)
