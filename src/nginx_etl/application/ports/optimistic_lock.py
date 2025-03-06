from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from enum import Enum, auto


@dataclass(kw_only=True, frozen=True, slots=True)
class ActiveOptimisticLock:
    is_owned: bool


type OptimisticLock = (
    AbstractAsyncContextManager[ActiveOptimisticLock]
)


class OptimisticLockActor(Enum):
    etl = auto()


class OptimisticLockWhen(ABC):
    @abstractmethod
    def __call__(self, *, actor: OptimisticLockActor) -> OptimisticLock: ...
