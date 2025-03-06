from collections.abc import AsyncIterable, AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from nginx_etl.application.ports.raw_nginx_log_queue import RawNginxLogQueue
from nginx_etl.entities.raw_nginx_log import RawNginxLog
from nginx_etl.infrastructure.file_line_parser import FileLineParser
from nginx_etl.infrastructure.in_redis_file_line_parser import (
    InRedisFileLineParser,
)
from nginx_etl.infrastructure.parsed_raw_nginx_log import (
    parsed_raw_nginx_log_from,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class NginxLogFileAsRawNginxLogQueue(RawNginxLogQueue):
    in_redis_file_line_parser: InRedisFileLineParser

    @asynccontextmanager
    async def pull_commitable_batches(
        self
    ) -> AsyncIterator[AsyncIterable[tuple[RawNginxLog, ...]]]:
        file_line_parser = await (
            self.in_redis_file_line_parser.as_file_line_parser()
        )
        yield self.__parse_raw_nginx_log_batches_using(file_line_parser)
        await self.in_redis_file_line_parser.be_like(file_line_parser)

    async def __parse_raw_nginx_log_batches_using(
        self, file_line_parser: FileLineParser
    ) -> AsyncIterable[tuple[RawNginxLog, ...]]:
        line_batches = file_line_parser.parse_line_batches()

        for line_batch in line_batches:
            yield tuple(
                parsed_raw_nginx_log_from(line) for line in line_batch if line
            )
