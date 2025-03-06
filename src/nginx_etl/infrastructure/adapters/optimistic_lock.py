from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from redis.asyncio import Redis
from redis.asyncio.lock import Lock as InRedisLock

from nginx_etl.application.ports.optimistic_lock import (
    ActiveOptimisticLock,
    OptimisticLockActor,
    OptimisticLockWhen,
)


@dataclass(kw_only=True, frozen=True, unsafe_hash=False, slots=True)
class InRedisOptimisticLockWhen(OptimisticLockWhen):
    redis: Redis
    lock_max_age_seconds: int | float | None
    _lock_by_actor: dict[OptimisticLockActor, InRedisLock] = field(
        init=False, default_factory=dict
    )

    def __new_lock_of(self, actor: OptimisticLockActor) -> InRedisLock:
        return InRedisLock(
            redis=self.redis,
            name=self.__lock_name_when(actor=actor),
            blocking=False,
            timeout=self.lock_max_age_seconds,
        )

    def __lock_name_when(self, *, actor: OptimisticLockActor) -> bytes:
        match actor:
            case OptimisticLockActor.etl:
                return b"optimistic_lock_for_etl"

    def __lock_of(self, actor: OptimisticLockActor) -> InRedisLock:
        lock = self._lock_by_actor.get(actor)

        if lock is not None:
            return lock

        lock = self.__new_lock_of(actor)
        self._lock_by_actor[actor] = lock

        return lock

    @asynccontextmanager
    async def __call__(
        self, *, actor: OptimisticLockActor
    ) -> AsyncIterator[ActiveOptimisticLock]:
        lock = self.__lock_of(actor)

        is_active_lock_owned = await lock.acquire()
        active_lock = ActiveOptimisticLock(is_owned=is_active_lock_owned)

        if not is_active_lock_owned:
            yield active_lock
            return

        try:
            yield active_lock
        except Exception as error:
            await lock.release()
            raise error from error
        else:
            await lock.release()
