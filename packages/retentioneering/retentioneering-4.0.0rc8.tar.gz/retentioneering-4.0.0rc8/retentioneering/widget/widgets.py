from __future__ import annotations

import inspect
import types
from dataclasses import dataclass, field
from typing import Any, Callable, List, Type, Union

from retentioneering.common.constants import DATETIME_UNITS_LIST
from retentioneering.exceptions.widget import ParseReteFuncError


@dataclass
class StringWidget:
    default: str | None = None
    widget: str = "string"

    @classmethod
    def from_dict(cls: Type[StringWidget], **kwargs: Any) -> "StringWidget":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})


@dataclass
class IntegerWidget:
    default: int | None = None
    widget: str = "integer"

    @classmethod
    def from_dict(cls: Type[IntegerWidget], **kwargs: Any) -> "IntegerWidget":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})


@dataclass
class EnumWidget:
    default: Any | None = None
    params: list[str] | None = None
    widget: str = "enum"
    optional: bool | None = None

    @classmethod
    def from_dict(cls: Type[EnumWidget], **kwargs: Any) -> "EnumWidget":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls, value: str) -> str:
        return value

    @classmethod
    def _parse(cls, value: str) -> str:  # type: ignore
        return value


@dataclass
class BooleanWidget:
    default: bool = False
    widget: str = "boolean"

    @classmethod
    def from_dict(cls: Type[BooleanWidget], **kwargs: Any) -> "BooleanWidget":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})


@dataclass
class ReteTimeWidget:
    default: tuple[float, str] | None = None
    widget: str = "time_widget"
    params: list = field(
        default_factory=lambda: [{"widget": "float"}, {"params": DATETIME_UNITS_LIST, "widget": "enum"}]
    )

    @classmethod
    def from_dict(cls: Type[ReteTimeWidget], **kwargs: Any) -> "ReteTimeWidget":
        kwargs["params"] = [
            {"widget": "float"},
            {"widget": "enum", "params": ["Y", "M", "W", "D", "h", "m", "s", "ms", "us", "μs", "ns", "ps", "fs", "as"]},
        ]
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls, value: tuple[float, str]) -> tuple[float, str]:
        return value

    @classmethod
    def _parse(cls: Type[ReteTimeWidget], value: str) -> tuple[float, str]:  # type: ignore
        TIME, QUANT = 0, 1

        if type(value) is tuple:
            return value  # type: ignore

        if type(value) is list and len(value) != 2:
            raise Exception("Incorrect input")

        if type(value) is list:
            return float(value[TIME]), str(value[QUANT])

        data = value.split(",")

        if len(data) != 2:
            raise Exception("Incorrect input")
        return float(data[TIME]), str(data[QUANT])


@dataclass
class ReteFunction:
    default: Callable | None = None
    widget: str = "function"

    @classmethod
    def from_dict(cls: Type[ReteFunction], **kwargs: Any) -> "ReteFunction":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls, value: Callable) -> str:
        try:
            code = inspect.getsource(value)
            return code
        except OSError:
            return getattr(value, "_source_code", "")

    @classmethod
    def _parse(cls, value: str) -> Callable:  # type: ignore
        func_str = value.strip()
        try:
            code_obj = compile(func_str, "<string>", "exec")
        except:
            raise ParseReteFuncError("parsing error. You must implement a python function here")

        new_func_type = None

        for i in code_obj.co_consts:
            try:
                new_func_type = types.FunctionType(i, globals=globals())
                break
            except TypeError as err:
                continue

        if new_func_type is None:
            raise ParseReteFuncError("parsing error. You must implement a python function here")

        setattr(new_func_type, "_source_code", func_str)
        return new_func_type


@dataclass
class ListOfInt:
    default: list[int] | None = None
    widget: str = "list_of_int"

    @classmethod
    def from_dict(cls: Type[ListOfInt], **kwargs: Any) -> "ListOfInt":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls: Type[ListOfInt], value: list[int] | None) -> list[int] | None:
        return value

    @classmethod
    def _parse(cls: Type[ListOfInt], value: list[int]) -> list[int] | None:  # type: ignore
        return value


@dataclass
class ListOfUsers:
    # @TODO: remove this widget and make his functionality in ListOfInt. Vladimir Makhanov
    default: list[int] | list[str] | None = None
    params: dict[str, str] | None = field(default_factory=lambda: {"disable_value": "all"})
    widget: str = "list_of_ids"

    @classmethod
    def from_dict(cls: Type[ListOfUsers], **kwargs: Any) -> "ListOfUsers":
        kwargs["params"] = {"disable_value": "all"}
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls: Type[ListOfUsers], value: list[int] | list[str] | None) -> list[int] | list[str] | None:
        return value

    @classmethod
    def _parse(cls: Type[ListOfUsers], value: list[int] | list[str]) -> list[int] | list[str] | None:  # type: ignore
        return value


@dataclass
class ListOfIds:
    default: list[int] | list[str] | None = None
    widget: str = "list_of_ids"

    @classmethod
    def from_dict(cls: Type[ListOfIds], **kwargs: Any) -> "ListOfIds":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls: Type[ListOfIds], value: list[int] | list[str] | None) -> list[int] | list[str] | None:
        return value

    @classmethod
    def _parse(cls: Type[ListOfIds], value: list[int] | list[str]) -> list[int] | list[str] | None:  # type: ignore
        return value


@dataclass
class ListOfString:
    default: list[str] | None = None
    widget: str = "list_of_string"

    @classmethod
    def from_dict(cls: Type[ListOfString], **kwargs: Any) -> "ListOfString":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls: Type[ListOfString], value: list[str] | None) -> list[str] | None:
        return value

    @classmethod
    def _parse(cls: Type[ListOfString], value: list[str]) -> list[str] | None:  # type: ignore
        return value


@dataclass
class RenameRule:
    group_name: str
    child_events: List[str]


@dataclass
class RenameRulesWidget:
    default: list[RenameRule] | None = None
    widget: str = "rename_rules"

    @classmethod
    def from_dict(cls: Type[RenameRulesWidget], **kwargs: Any) -> "RenameRulesWidget":
        return cls(**{k: v for k, v in kwargs.items() if k in inspect.signature(cls).parameters})

    @classmethod
    def _serialize(cls: Type[RenameRulesWidget], value: list[RenameRule] | None) -> list[RenameRule] | None:
        return value

    @classmethod
    def _parse(cls: Type[RenameRulesWidget], value: list[RenameRule] | None) -> list[RenameRule] | None:
        return value


WIDGET_TYPE = Union[
    Type[StringWidget],
    Type[IntegerWidget],
    Type[EnumWidget],
    Type[BooleanWidget],
    Type[ReteTimeWidget],
    Type[ReteFunction],
    Type[RenameRulesWidget],
]

WIDGET = Union[StringWidget, IntegerWidget, EnumWidget, BooleanWidget, ReteTimeWidget, ReteFunction, RenameRulesWidget]

# @TODO: make default dict. Vladimir Makhanov
WIDGET_MAPPING: dict[str, WIDGET_TYPE] = {
    "string": StringWidget,
    "integer": IntegerWidget,
    "enum": EnumWidget,
    "boolean": BooleanWidget,
    "tuple": ReteTimeWidget,
    "callable": ReteFunction,
}
