from enum import Enum
from typing import Any, TypeVar, get_origin, get_args, Literal

from ._converters import CONVERTERS
from ._defs import (
    ConversionContext,
    ConversionOptions,
    FailedConversionError,
    UnknownConversionError,
)
from ._special_converters import to_enum, to_literal

T = TypeVar("T")

_T_LITERAL: type = type(Literal[None])


def _convert(
    source_value: Any,
    target_type: type[T],
    ctx: ConversionContext,
) -> T:
    try:
        # noinspection PyTypeHints
        if isinstance(source_value, target_type):
            return source_value
    except TypeError:
        pass
    origin = get_origin(target_type)
    try:
        if origin is None:
            if target_type in ctx.options.custom_converters:
                return ctx.options.custom_converters[target_type](source_value)
            if target_type in CONVERTERS:
                return CONVERTERS[target_type](source_value, ctx)
            if issubclass(target_type, Enum):
                return to_enum(target_type, source_value, ctx)  # type: ignore[return-value]
        args = get_args(target_type)
        if origin is Literal:
            return to_literal(args, source_value, ctx)
    except UnknownConversionError as e:
        if e.target_type is not target_type or e.given_value is not source_value:
            raise UnknownConversionError(target_type, source_value) from e
        raise e
    except Exception as e:
        raise FailedConversionError(target_type, source_value) from e
    raise UnknownConversionError(target_type, source_value)


def convert(
    source_value: Any,
    target_type: type[T],
    conversion_options: ConversionOptions = ConversionOptions(),
) -> T:
    try:
        # noinspection PyTypeHints
        if isinstance(source_value, target_type):
            return source_value
    except TypeError:
        pass
    context = ConversionContext(_convert, conversion_options)
    return _convert(source_value, target_type, context)
