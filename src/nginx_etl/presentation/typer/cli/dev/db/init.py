from dishka.integrations.click import FromDishka
from typer import echo, style
from typer.models import CommandInfo

from nginx_etl.infrastructure.clickhouse.init_dev import InitDevClickHouse
from nginx_etl.presentation.typer.di_point import di_point


@di_point
async def _callback(
    init_dev_clickhouse: FromDishka[InitDevClickHouse]
) -> None:
    await init_dev_clickhouse()
    echo(style("OK", fg="green", bold=True))


init_command = CommandInfo(
    name="init",
    help="Creates table structure.",
    callback=_callback,
)
