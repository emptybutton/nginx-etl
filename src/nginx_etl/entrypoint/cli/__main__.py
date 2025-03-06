import asyncio

from typer.main import get_command

from nginx_etl.entrypoint.cli.di import container
from nginx_etl.presentation.typer.cli import cli
from nginx_etl.presentation.typer.di_point import di_point


async def amain() -> None:
    try:
        async with container() as request_container:
            di_point.container = request_container
            command = get_command(cli)
            command()
    finally:
        await container.close()


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
