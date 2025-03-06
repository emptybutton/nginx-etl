from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address


@dataclass(kw_only=True, frozen=True, slots=True)
class RawNginxLog:
    client_ip: IPv4Address | IPv6Address
    datetime: datetime
    method: str
    status_code: int
    endpoint: str
    protocol: str
    user_agent: str
