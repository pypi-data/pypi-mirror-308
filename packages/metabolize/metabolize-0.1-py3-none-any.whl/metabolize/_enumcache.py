from collections import defaultdict
from collections.abc import Mapping
from enum import Enum
from typing import Any


class EnumMap(dict[type[Enum], Mapping[Any, Enum]]):
    def __missing__(self, enum: type[Enum]) -> Mapping[Any, Enum]:
        valuemap: dict[Any, Enum] = dict()
        for e in enum:
            valuemap[e.name] = e
            valuemap[e.value] = e
        return valuemap


class CaseInsensitiveEnumMap(dict[type[Enum], Mapping[str, Enum]]):
    def __missing__(self, enum: type[Enum]) -> Mapping[str, Enum]:
        valuemap: dict[str, Enum] = dict()
        identifiers: defaultdict[str, int] = defaultdict(lambda: 0)
        for e in enum:
            identifiers[nl := e.name.lower()] += 1
            if isinstance(e.value, str):
                if (vl := e.value.lower()) != nl:
                    identifiers[vl] += 1
        for e in enum:
            if identifiers[nl := e.name.lower()] == 1:
                valuemap[nl] = e
            if isinstance(e.value, str):
                if identifiers[vl := e.value.lower()] == 1:
                    valuemap[vl] = e
        return valuemap


enumcache: Mapping[type[Enum], Mapping[Any, Enum]] = EnumMap()
enumcacheci: Mapping[type[Enum], Mapping[Any, Enum]] = CaseInsensitiveEnumMap()
