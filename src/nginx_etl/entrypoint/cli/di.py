from dishka import make_async_container

from nginx_etl.entrypoint.common.di import (
    ApplicationProvider,
    InfrastructureProvider,
)


container = make_async_container(
    InfrastructureProvider(),
    ApplicationProvider(),
)
