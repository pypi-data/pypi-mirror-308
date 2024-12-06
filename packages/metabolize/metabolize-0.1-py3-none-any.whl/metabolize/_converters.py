import re
from collections.abc import Callable, Mapping, Iterable
from datetime import date, time, datetime, timedelta
from typing import Final, Any
from uuid import UUID

from ._datetime_converters import (
    to_datetime,
    to_date,
    to_time,
    to_timedelta,
    to_duration,
)
from ._defs import (
    Duration,
    UnknownConversionError,
    ConversionContext,
)


def to_bool(v: Any, ctx: ConversionContext) -> bool:
    if ctx.options.bool_conversions != "only":
        if v in ctx.options.true_values:
            return True
        if v in ctx.options.false_values:
            return False
        if isinstance(v, str):
            v_lower = v.lower().strip()
            if v_lower in ctx.options.true_values:
                return True
            if v_lower in ctx.options.false_values:
                return False
    if ctx.options.bool_conversions:
        return bool(v)
    raise UnknownConversionError(bool, v)


def to_int(v: Any, ctx: ConversionContext) -> int:
    if ctx.options.int_conversions != "only":
        if isinstance(v, float):
            return int(v)
        if isinstance(v, (bytes, bytearray, memoryview)):
            acc = 0
            for b in v if ctx.options.big_endian else reversed(v):  # type: ignore[union-attr]
                acc *= 256
                acc += b
            return acc
        if isinstance(v, UUID):
            return v.int
        if isinstance(v, str):
            if v.startswith("0x"):
                return int(v[2:].replace("_", ""), base=16)
            return int(v)
    if ctx.options.int_conversions:
        return int(v)
    raise UnknownConversionError(int, v)


def to_float(v: Any, ctx: ConversionContext) -> float:
    if ctx.options.float_conversions != "only":
        if isinstance(v, int):
            return float(v)
        if isinstance(v, str):
            return float(v.replace("_", ""))
    if ctx.options.float_conversions:
        return float(v)
    raise UnknownConversionError(float, v)


_NON_HEXDIGIT: Final[re.Pattern] = re.compile(r"[^a-fA-F0-9]+")


def to_uuid(v: Any, ctx: ConversionContext) -> UUID:
    if isinstance(v, int):
        return UUID(int=v)
    if isinstance(v, bytes):
        return UUID(bytes=v) if ctx.options.big_endian else UUID(bytes_le=v)
    if isinstance(v, (bytearray, memoryview)):
        return (
            UUID(bytes=bytes(v)) if ctx.options.big_endian else UUID(bytes_le=bytes(v))
        )
    if isinstance(v, str):
        return UUID(hex=re.sub(_NON_HEXDIGIT, "", v))
    raise UnknownConversionError(UUID, v)


def to_bytes(v: Any, ctx: ConversionContext) -> bytes:
    if ctx.options.bytes_conversions != "only":
        if isinstance(v, str):
            return v.encode(ctx.options.encoding)
        if isinstance(v, int):
            arr = bytearray()
            while v > 0:
                b = v % 256
                arr.append(b)
                v //= 256
            return bytes(reversed(arr) if ctx.options.big_endian else arr)
        if isinstance(v, UUID):
            if ctx.options.big_endian:
                return v.bytes
            return v.bytes_le
    if ctx.options.bytes_conversions:
        return bytes(v)
    raise UnknownConversionError(bytes, v)


def to_bytearray(v: Any, ctx: ConversionContext) -> bytearray:
    try:
        if isinstance(v, str):
            return bytearray(v.encode(ctx.options.encoding))
        if isinstance(v, int):
            arr = bytearray()
            while v > 0:
                b = v % 256
                arr.append(b)
                v //= 256
            if ctx.options.big_endian:
                arr.reverse()
            return arr
        if isinstance(v, UUID):
            if ctx.options.big_endian:
                return bytearray(v.bytes)
            return bytearray(v.bytes_le)
    except UnknownConversionError as e:
        raise UnknownConversionError(bytearray, v) from e
    raise UnknownConversionError(bytearray, v)


def to_str(v: Any, ctx: ConversionContext) -> str:
    if ctx.options.str_conversions != "only":
        if isinstance(v, (bytes, bytearray, memoryview)):
            return str(v, ctx.options.encoding)
        if isinstance(v, (date, time, datetime)):
            return v.isoformat()
        if isinstance(v, (bool, int, float, UUID)):
            return str(v)
        if isinstance(v, Mapping) and (sep := ctx.options.mapping_separator):
            return sep.join(
                ctx.options.key_value_format
                % (ctx.convert(k, str), ctx.convert(x, str))
                for k, x in v.items()
            )
        if isinstance(v, Iterable) and (sep := ctx.options.collection_separator):
            return sep.join(ctx.convert(x, str) for x in v)
    if ctx.options.str_conversions:
        return str(v)
    raise UnknownConversionError(str, v)


CONVERTERS: Final[dict[type, Callable[[Any, ConversionContext], Any]]] = {
    bool: to_bool,
    int: to_int,
    float: to_float,
    bytes: to_bytes,
    bytearray: to_bytearray,
    str: to_str,
    UUID: to_uuid,
    date: to_date,
    time: to_time,
    datetime: to_datetime,
    timedelta: to_timedelta,
    Duration: to_duration,
}
