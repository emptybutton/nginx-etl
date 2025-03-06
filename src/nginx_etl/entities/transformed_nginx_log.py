from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID, uuid4

from nginx_etl.entities.raw_nginx_log import RawNginxLog


@dataclass(kw_only=True, frozen=True, slots=True)
class TransformedNginxLog:
    id: UUID
    client_ipv4: IPv4Address | None
    client_ipv6: IPv6Address | None
    datetime: datetime
    method: str
    status_code: int
    endpoint: str
    protocol: str
    user_agent: str


def transformed(raw_nginx_log: RawNginxLog) -> TransformedNginxLog:
    if isinstance(raw_nginx_log.client_ip, IPv4Address):
        client_ipv4 = raw_nginx_log.client_ip
        client_ipv6 = None
    else:
        client_ipv4 = None
        client_ipv6 = raw_nginx_log.client_ip

    return TransformedNginxLog(
        id=uuid4(),
        client_ipv4=client_ipv4,
        client_ipv6=client_ipv6,
        datetime=raw_nginx_log.datetime,
        method=raw_nginx_log.method,
        status_code=raw_nginx_log.status_code,
        endpoint=raw_nginx_log.endpoint,
        protocol=raw_nginx_log.protocol,
        user_agent=raw_nginx_log.user_agent,
    )
