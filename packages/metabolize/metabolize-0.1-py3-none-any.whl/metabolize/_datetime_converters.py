import re
from datetime import date, time, datetime, timedelta
from typing import Final, Any

from ._defs import (
    Duration,
    FailedConversionError,
    UnknownConversionError,
    ConversionContext,
)


def to_date(v: Any, ctx: ConversionContext) -> date:
    if isinstance(v, str):
        v = v.strip()
        return date.fromisoformat(v)
    if isinstance(v, (int, float)):
        return to_datetime(v, ctx).date()
    raise UnknownConversionError(date, v)


def to_time(v: Any, ctx: ConversionContext) -> time:
    if isinstance(v, str):
        v = v.strip()
        t = time.fromisoformat(v)
        if not t.tzinfo:
            t = t.replace(tzinfo=ctx.options.default_timezone)
        return t
    raise UnknownConversionError(time, v)


def to_datetime(v: Any, ctx: ConversionContext) -> datetime:
    if isinstance(v, str):
        v = v.strip()
        t = datetime.fromisoformat(v)
        if not t.tzinfo:
            t = t.replace(tzinfo=ctx.options.default_timezone)
        return t
    if isinstance(v, (int, float)):
        if v > ctx.options.largest_unix_timestamp:
            v /= 1000
        return datetime.fromtimestamp(v, tz=ctx.options.default_timezone)
    raise UnknownConversionError(datetime, v)


_ISO1: Final[re.Pattern] = re.compile(
    r"^P((?P<Y>\d+)Y)?((?P<M>\d+)M)?((?P<D>\d+)D)?(T((?P<h>\d+)H)?((?P<m>\d+)M)?((?P<s>\d+)S)?)?$",
    flags=re.IGNORECASE,
)

_ISO2: Final[re.Pattern] = re.compile(
    r"^P(?P<Y>\d+)-(?P<M>\d+)-(?P<D>\d+)T(?P<h>\d+)(:(?P<m>\d+)(:(?P<s>\d+))?)?$",
    flags=re.IGNORECASE,
)

_DURATION: Final[re.Pattern] = re.compile(
    r"^"
    r"((?P<Y>\d+) *([Yy](ears?)?|yrs?) *)?"
    r"((?P<M>\d+) *(M|[Mm]onths?) *)?"
    r"((?P<D>\d+) *([Dd](ays?)?) *)?"
    r"((?P<h>\d+) *(h(ours?)?|hrs?) *)?"
    r"((?P<m>\d+)('| *min(utes?)?) *)?"
    r"((?P<s>\d+)(''| *s(ec(onds?)?)?) *)?"
    r"((?P<ms>\d+) *(ms|millis?|milliseconds?))?"
    r"$"
)


def to_duration(v: Any, _ctx: ConversionContext) -> Duration:
    if isinstance(v, str):
        if (m := _ISO1.match(v)) or (m := _ISO2.match(v)) or (m := _DURATION.match(v)):
            g = m.groupdict()
            return Duration(
                int(g.get("Y") or 0),
                int(g.get("M") or 0),
                int(g.get("D") or 0),
                int(g.get("h") or 0),
                int(g.get("m") or 0),
                int(g.get("s") or 0),
                int(g.get("ms") or 0),
            )
        raise FailedConversionError(Duration, v, "unrecognized duration pattern")
    if isinstance(v, int):
        # noinspection PyArgumentList
        return Duration(seconds=v)
    if isinstance(v, float):
        # noinspection PyArgumentList
        return Duration(seconds=int(v), millis=int(v * 1000) % 1000)

    raise UnknownConversionError(Duration, v)


def to_timedelta(v: Any, ctx: ConversionContext) -> timedelta:
    dur = to_duration(v, ctx)
    return timedelta(
        days=Duration.years * 365 + Duration.months * 30 + Duration.days,
        seconds=Duration.hours * 3600 + Duration.minutes * 60 + Duration.seconds,
        microseconds=dur.millis * 1000,
    )
