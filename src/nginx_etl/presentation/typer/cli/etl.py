from contextlib import suppress

from dishka.integrations.click import FromDishka
from typer.models import CommandInfo

from nginx_etl.application.etl import ConcurrentEtlError, Etl
from nginx_etl.presentation.typer.di_point import di_point


@di_point
async def _callback(etl: FromDishka[Etl]) -> None:
    with suppress(ConcurrentEtlError):
        await etl()


etl_command = CommandInfo(
    name="run", help="Starts the etl pipeline.", callback=_callback
)
