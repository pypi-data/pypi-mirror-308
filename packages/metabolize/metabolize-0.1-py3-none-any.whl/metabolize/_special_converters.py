from enum import Enum, IntEnum
from typing import Any, TypeVar

from ._defs import ConversionContext, FailedConversionError
from ._enumcache import enumcache, enumcacheci


E = TypeVar("E", bound=Enum)


class E0(Enum):
    pass


class E1(IntEnum):
    pass


def to_enum(t: type[E], v: Any, ctx: ConversionContext) -> E:
    if (r := enumcache[t].get(v)) is not None:
        return r  # type: ignore[return-value]
    if (r := enumcacheci[t].get(ctx.convert(v, str).lower())) is not None:
        return r  # type: ignore[return-value]
    raise FailedConversionError(t, v, "Don't know how to convert to target enum type.")


def to_literal(options: tuple[Any, ...], v: Any, _ctx: ConversionContext):
    if v in options:
        return v
