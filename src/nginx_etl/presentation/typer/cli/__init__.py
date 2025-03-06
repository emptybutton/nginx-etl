from typer import Typer

from nginx_etl.presentation.typer.cli.dev import (
    dev_commands,
)
from nginx_etl.presentation.typer.cli.etl import etl_command


cli = Typer()

cli.registered_commands += [
    etl_command,
]
cli.add_typer(dev_commands)
