import asyncio
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from functools import wraps
from threading import Thread
from typing import Any

from click import Abort
from dishka import AsyncContainer
from dishka.integrations.base import is_dishka_injected, wrap_injection


@dataclass(kw_only=True, slots=True)
class DIPoint:
    container: AsyncContainer | None = None

    def __call__[R, **Pm](
        self, callback: Callable[Pm, Coroutine[Any, Any, R]],
    ) -> Callable[Pm, Any]:
        if is_dishka_injected(callback):
            return callback

        injected_callback = wrap_injection(
            func=callback,
            container_getter=lambda _, __: self._get_container(),
            remove_depends=True,
            is_async=True,
        )

        return self._marked_as_dishka_injected(
            self._in_isolated_event_loop(injected_callback)
        )

    def _get_container(self) -> AsyncContainer:
        assert self.container is not None, "set the container"  # noqa: S101
        return self.container

    def _marked_as_dishka_injected[V](self, value: V) -> V:
        value.__dishka_injected__ = True  # type: ignore[attr-defined]
        return value

    def _in_isolated_event_loop[R, **Pm](
        self, func: Callable[Pm, Coroutine[Any, Any, R]]
    ) -> Callable[Pm, None]:
        @wraps(func)
        def wrapper(*args: Pm.args, **kwargs: Pm.kwargs) -> None:
            try:
                thread = Thread(
                    target=lambda: asyncio.run(func(*args, **kwargs))
                )
                thread.start()
                thread.join()
            except Abort as abort:
                raise abort from None

        return wrapper
