import dataclasses
import datetime
from collections.abc import Hashable
from typing import Literal, Any, Callable, NamedTuple, TypeVar

from frzn import frozendict

Date = datetime.date
Time = datetime.time
DateTime = datetime.datetime
TimeDelta = datetime.timedelta
TimeZone = datetime.timezone


class ConversionError(ValueError):
    def __init__(self, *, target_type: type, given_value: Any, message: str):
        super().__init__(message)
        self._target_type = target_type
        self._given_value = given_value

    @property
    def target_type(self) -> type:
        return self._target_type

    @property
    def given_value(self) -> Any:
        return self._given_value


class FailedConversionError(ConversionError):
    def __init__(
        self,
        target_type: type,
        given_value: Any,
        msg: str | None = None,
    ) -> None:
        super().__init__(
            target_type=target_type,
            given_value=given_value,
            message=(
                f"failed to convert to {target_type.__name__} from {type(given_value).__name__}"
                + (f": {msg}" if msg else "")
            ),
        )


class UnknownConversionError(ConversionError):
    def __init__(self, target_type: type, given_value: Any) -> None:
        super().__init__(
            target_type=target_type,
            given_value=given_value,
            message=f"don't know how to convert to {target_type.__name__} from {type(given_value).__name__}",
        )


@dataclasses.dataclass(frozen=True)
class ConversionOptions:
    true_values: frozenset[Hashable] = frozenset({"true", "yes", "on", "1", True})
    false_values: frozenset[Hashable] = frozenset({"false", "no", "off", "0", False})
    big_endian: bool = True
    encoding: str = "utf8"
    collection_separator: str | None = ", "
    mapping_separator: str | None = "; "
    key_value_format: str = "%s=%s"
    time_values: frozendict[str, Time] = frozendict(
        {"midnight": Time.fromisoformat("00:00")},
        {"noon": Time.fromisoformat("00:00")},
    )
    default_timezone: TimeZone = TimeZone.utc

    # larger than 9999-12-31 23:59:59, smallest milliseconds timestamp is 1978-01-11 22:31:37.200000
    largest_unix_timestamp: int = 253402297199

    custom_converters: frozendict[type, Callable[[Any], Any]] = frozendict()
    bytes_conversions: Literal["only", True, False] = True
    str_conversions: Literal["only", True, False] = True
    bool_conversions: Literal["only", True, False] = True
    int_conversions: Literal["only", True, False] = True
    float_conversions: Literal["only", True, False] = True


T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class ConversionContext:
    convertfn: "Callable[[Any, Any, ConversionContext], Any]"
    options: ConversionOptions

    def convert(self, source_value: Any, target_type: type[T]) -> T:
        return self.convertfn(source_value, target_type, self)


class Duration(NamedTuple):
    years: int = 0
    months: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    millis: int = 0
