from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import batched
from pathlib import Path


class InvalidLineBatchMaxSizeError(Exception): ...


class NotFileError(Exception): ...


@dataclass(kw_only=True, slots=True)
class FileLineParser:
    file_path: Path
    _line_batch_max_size: int
    _commited_file_offset: int = field(default=0)

    @property
    def commited_file_offset(self) -> int:
        return self._commited_file_offset

    def __post_init__(self) -> None:
        if self._line_batch_max_size <= 0:
            raise InvalidLineBatchMaxSizeError(self._line_batch_max_size)

        if not self.file_path.is_file():
            raise NotFileError(self.file_path.absolute())

    def parse_line_batches(self) -> Iterable[tuple[str, ...]]:
        with self.file_path.open() as file:
            file.seek(self._commited_file_offset)
            line_batches = batched(
                self._clean(file), self._line_batch_max_size, strict=False
            )

            for line_batch in line_batches:
                self._commited_file_offset += (
                    self._batch_sub_offset_of(line_batch)
                )
                yield line_batch

    def _clean(self, lines: Iterable[str]) -> Iterable[str]:
        for line in lines:
            clean_line = line.strip("\n")

            if clean_line:
                yield clean_line

    def _batch_sub_offset_of(self, line_batch: tuple[str, ...]) -> int:
        return sum(map(self._line_sub_offset_of, line_batch))

    def _line_sub_offset_of(self, line: str) -> int:
        return len(line.encode())
