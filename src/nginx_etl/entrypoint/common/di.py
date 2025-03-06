from collections.abc import AsyncIterable
from pathlib import Path

from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient as ClickHouse
from dishka import Provider, Scope, make_async_container, provide
from redis.asyncio import BlockingConnectionPool as RedisBlockingConnectionPool
from redis.asyncio import ConnectionPool as RedisConnectionPool
from redis.asyncio import Redis

from nginx_etl.application.etl import Etl
from nginx_etl.application.ports.logger import Logger
from nginx_etl.application.ports.optimistic_lock import OptimisticLockWhen
from nginx_etl.application.ports.raw_nginx_log_queue import RawNginxLogQueue
from nginx_etl.application.ports.transformed_nginx_log_storage import (
    TransformedNginxLogStorage,
)
from nginx_etl.infrastructure.adapters.logger import HumanReadableLogger
from nginx_etl.infrastructure.adapters.optimistic_lock import (
    InRedisOptimisticLockWhen,
)
from nginx_etl.infrastructure.adapters.raw_nginx_log_queue import (
    NginxLogFileAsRawNginxLogQueue,
)
from nginx_etl.infrastructure.adapters.transformed_nginx_log_storage import (
    ClickHouseTransformedNginxLogStorage,
)
from nginx_etl.infrastructure.clickhouse.flush_dev import FlushDevClickHouse
from nginx_etl.infrastructure.clickhouse.init_dev import InitDevClickHouse
from nginx_etl.infrastructure.in_redis_file_line_parser import (
    InRedisFileLineParser,
)
from nginx_etl.infrastructure.typenv.envs import Envs


class InfrastructureProvider(Provider):
    scope = Scope.APP

    provide_envs = provide(source=Envs.load)

    @provide
    async def provide_clickhouse(self, envs: Envs) -> ClickHouse:
        return await get_async_client(
            host=envs.clickhouse_host,
            username=envs.clickhouse_user,
            password=envs.clickhouse_password,
            database=envs.clickhouse_db,
            port=envs.clickhouse_port,
        )

    @provide
    async def provide_redis_connection_pool(
        self, envs: Envs
    ) -> AsyncIterable[RedisConnectionPool]:
        pool = RedisBlockingConnectionPool.from_url(envs.redis_url)
        try:
            yield pool
        finally:
            await pool.aclose()

    @provide
    async def provide_redis(
        self, redis_connection_pool: RedisConnectionPool
    ) -> AsyncIterable[Redis]:
        redis = Redis.from_pool(redis_connection_pool)
        redis.auto_close_connection_pool = False

        async with redis:
            yield redis

    @provide
    async def provide_logger(self) -> Logger:
        return HumanReadableLogger()

    @provide(scope=Scope.REQUEST)
    async def provide_optimistic_log_when(
        self, redis: Redis
    ) -> OptimisticLockWhen:
        return InRedisOptimisticLockWhen(
            redis=redis, lock_max_age_seconds=int(60 * 7.5)
        )

    @provide
    async def provide_transformed_nginx_log_storage(
        self, clickhouse: ClickHouse
    ) -> TransformedNginxLogStorage:
        return ClickHouseTransformedNginxLogStorage(clickhouse=clickhouse)

    @provide(scope=Scope.REQUEST)
    async def provide_in_redis_file_line_parser(
        self, redis: Redis, envs: Envs
    ) -> InRedisFileLineParser:
        return InRedisFileLineParser(
            id=b"main",
            redis=redis,
            file_path=Path(envs.nginx_log_file_path),
            line_batch_max_size=envs.nginx_log_file_line_batch_max_size,
        )

    provide_raw_nginx_log_queue = provide(
        NginxLogFileAsRawNginxLogQueue,
        provides=RawNginxLogQueue,
        scope=Scope.REQUEST,
    )

    provide_init_dev_clickhouse = provide(InitDevClickHouse)
    provide_flush_dev_clickhoue = provide(FlushDevClickHouse)


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    provide_register_user = provide(Etl)


container = make_async_container(
    InfrastructureProvider(),
    ApplicationProvider(),
)
