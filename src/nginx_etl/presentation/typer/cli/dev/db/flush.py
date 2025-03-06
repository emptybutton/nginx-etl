from dishka.integrations.click import FromDishka
from typer import echo, style
from typer.models import CommandInfo

from nginx_etl.infrastructure.clickhouse.flush_dev import FlushDevClickHouse
from nginx_etl.presentation.typer.di_point import di_point


@di_point
async def _callback(
    flush_dev_clickhouse: FromDishka[FlushDevClickHouse]
) -> None:
    await flush_dev_clickhouse()
    echo(style("OK", fg="green", bold=True))


flush_command = CommandInfo(
    name="flush",
    help="Delete all rows in tables.",
    callback=_callback,
)
