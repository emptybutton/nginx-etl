from datetime import datetime
from ipaddress import AddressValueError, IPv4Address, IPv6Address

from nginx_etl.entities.raw_nginx_log import RawNginxLog


def parsed_raw_nginx_log_from(line: str) -> RawNginxLog:
    """
    Line example:
    1.1.1.1 - - [05/Mar/2025:15:25:04 +0000] "GET / HTTP/1.1" 200 2 "-" "Wget"
    """

    (
        raw_id,
        _,
        _,
        raw_dateime,
        _,
        raw_method,
        endpoint,
        raw_protocol,
        raw_status_code,
        _,
        _,
        *split_user_agent,
    ) = line.split()

    return RawNginxLog(
        client_ip=_id_when(raw_ip=raw_id),
        datetime=_datetime_when(raw_dateime=raw_dateime),
        method=raw_method[1:],
        status_code=int(raw_status_code),
        endpoint=endpoint,
        protocol=raw_protocol[:-1],
        user_agent=" ".join(split_user_agent)[1:-1],
    )


def _datetime_when(raw_dateime: str) -> datetime:
    raw_dateime = raw_dateime[1:]
    day, raw_month, other = raw_dateime.split("/")
    year, hour, minute, second = other.split(":")

    month = _month_when(raw_month=raw_month)

    return datetime(
        int(year), month, int(day), int(hour), int(minute), int(second)
    )


def _month_when(raw_month: str) -> int:
    month_by_raw_month = dict(
        Jan=1,
        Feb=2,
        Mar=3,
        Apr=4,
        May=5,
        Jun=6,
        Jul=7,
        Aug=8,
        Sep=9,
        Oct=10,
        Nov=11,
        Dec=12,
    )

    return month_by_raw_month[raw_month]


def _id_when(*, raw_ip: str) -> IPv4Address | IPv6Address:
    try:
        return IPv4Address(raw_ip)
    except AddressValueError:
        return IPv6Address(raw_ip)
