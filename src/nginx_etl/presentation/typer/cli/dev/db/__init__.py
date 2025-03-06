from typer import Typer

from nginx_etl.presentation.typer.cli.dev.db.flush import flush_command
from nginx_etl.presentation.typer.cli.dev.db.init import init_command


db_commands = Typer(name="db", help="Commands for local ClickHouse.")

db_commands.registered_commands += [
    init_command,
    flush_command,
]
