from typer import Typer

from nginx_etl.presentation.typer.cli.dev.db import db_commands


dev_commands = Typer(name="dev", help="Commands for test cases.")

dev_commands.add_typer(db_commands)
