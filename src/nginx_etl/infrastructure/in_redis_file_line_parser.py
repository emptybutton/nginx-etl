from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from redis.asyncio import Redis

from nginx_etl.infrastructure.file_line_parser import FileLineParser


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisFileLineParser:
    id: bytes
    file_path: Path
    line_batch_max_size: int
    redis: Redis

    _redis_key: ClassVar = b"file_line_parsers"

    async def as_file_line_parser(self) -> FileLineParser:
        encoded_commited_file_offset: bytes | None = await self.redis.hget(  # type: ignore[misc]
            self._redis_key, self.id  # type: ignore[arg-type]
        )

        if encoded_commited_file_offset is None:
            commited_file_offset = 0
        else:
            commited_file_offset = int(encoded_commited_file_offset.decode())

        return FileLineParser(
            file_path=self.file_path,
            _line_batch_max_size=self.line_batch_max_size,
            _commited_file_offset=commited_file_offset,
        )

    async def be_like(self, file_line_parser: FileLineParser) -> None:
        await self.redis.hset(  # type: ignore[misc]
            self._redis_key,
            self.id,  # type: ignore[arg-type]
            file_line_parser.commited_file_offset,  # type: ignore[arg-type]
        )
