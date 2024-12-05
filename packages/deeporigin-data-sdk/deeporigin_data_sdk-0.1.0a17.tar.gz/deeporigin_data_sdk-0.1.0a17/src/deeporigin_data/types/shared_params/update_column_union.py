# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from . import update_column_union
from ..._utils import PropertyInfo

__all__ = [
    "UpdateColumnUnion",
    "Type",
    "UnionMember3",
    "UnionMember4",
    "UnionMember4ConfigFile",
    "UnionMember5",
    "UnionMember5ConfigNumeric",
    "UnionMember6",
    "UnionMember6ConfigNumeric",
    "UnionMember7",
    "UnionMember8",
    "UnionMember8ConfigSelect",
    "UnionMember12",
]


class Type(TypedDict, total=False):
    type: Required[Literal["boolean"]]


class UnionMember3(TypedDict, total=False):
    expression_code: Required[Annotated[str, PropertyInfo(alias="expressionCode")]]

    expression_return_type: Required[
        Annotated[Literal["text", "float", "integer"], PropertyInfo(alias="expressionReturnType")]
    ]

    type: Required[Literal["expression"]]


class UnionMember4ConfigFile(TypedDict, total=False):
    allowed_extensions: Annotated[List[str], PropertyInfo(alias="allowedExtensions")]


class UnionMember4(TypedDict, total=False):
    type: Required[Literal["file"]]

    config_file: Annotated[UnionMember4ConfigFile, PropertyInfo(alias="configFile")]


class UnionMember5ConfigNumeric(TypedDict, total=False):
    unit: str


class UnionMember5(TypedDict, total=False):
    type: Required[Literal["float"]]

    config_numeric: Annotated[UnionMember5ConfigNumeric, PropertyInfo(alias="configNumeric")]


class UnionMember6ConfigNumeric(TypedDict, total=False):
    unit: str


class UnionMember6(TypedDict, total=False):
    type: Required[Literal["integer"]]

    config_numeric: Annotated[UnionMember6ConfigNumeric, PropertyInfo(alias="configNumeric")]


class UnionMember7(TypedDict, total=False):
    reference_database_row_id: Required[Annotated[str, PropertyInfo(alias="referenceDatabaseRowId")]]

    type: Required[Literal["reference"]]


class UnionMember8ConfigSelect(TypedDict, total=False):
    options: Required[List[str]]

    can_create: Annotated[bool, PropertyInfo(alias="canCreate")]


class UnionMember8(TypedDict, total=False):
    config_select: Required[Annotated[UnionMember8ConfigSelect, PropertyInfo(alias="configSelect")]]

    type: Required[Literal["select"]]


class UnionMember12(TypedDict, total=False):
    lookup_external_column: Required[
        Annotated[update_column_union.UnionMember12LookupExternalColumn, PropertyInfo(alias="lookupExternalColumn")]
    ]

    lookup_external_column_id: Required[Annotated[str, PropertyInfo(alias="lookupExternalColumnId")]]

    lookup_source_column_id: Required[Annotated[str, PropertyInfo(alias="lookupSourceColumnId")]]

    type: Required[Literal["lookup"]]


UpdateColumnUnion: TypeAlias = Union[
    Type,
    Type,
    Type,
    UnionMember3,
    UnionMember4,
    UnionMember5,
    UnionMember6,
    UnionMember7,
    UnionMember8,
    Type,
    Type,
    Type,
    UnionMember12,
]
