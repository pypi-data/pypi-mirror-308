# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from . import update_column_union
from ..._utils import PropertyInfo

__all__ = [
    "UpdateColumnUnion",
    "Boolean",
    "Date",
    "Editor",
    "Expression",
    "File",
    "FileConfigFile",
    "Float",
    "FloatConfigNumeric",
    "Integer",
    "IntegerConfigNumeric",
    "Reference",
    "Select",
    "SelectConfigSelect",
    "Text",
    "URL",
    "User",
    "Lookup",
]


class Boolean(TypedDict, total=False):
    type: Required[Literal["boolean"]]


class Date(TypedDict, total=False):
    type: Required[Literal["date"]]


class Editor(TypedDict, total=False):
    type: Required[Literal["editor"]]


class Expression(TypedDict, total=False):
    expression_code: Required[Annotated[str, PropertyInfo(alias="expressionCode")]]

    expression_return_type: Required[
        Annotated[Literal["text", "float", "integer"], PropertyInfo(alias="expressionReturnType")]
    ]

    type: Required[Literal["expression"]]


class FileConfigFile(TypedDict, total=False):
    allowed_extensions: Annotated[List[str], PropertyInfo(alias="allowedExtensions")]


class File(TypedDict, total=False):
    type: Required[Literal["file"]]

    config_file: Annotated[FileConfigFile, PropertyInfo(alias="configFile")]


class FloatConfigNumeric(TypedDict, total=False):
    unit: str


class Float(TypedDict, total=False):
    type: Required[Literal["float"]]

    config_numeric: Annotated[FloatConfigNumeric, PropertyInfo(alias="configNumeric")]


class IntegerConfigNumeric(TypedDict, total=False):
    unit: str


class Integer(TypedDict, total=False):
    type: Required[Literal["integer"]]

    config_numeric: Annotated[IntegerConfigNumeric, PropertyInfo(alias="configNumeric")]


class Reference(TypedDict, total=False):
    reference_database_row_id: Required[Annotated[str, PropertyInfo(alias="referenceDatabaseRowId")]]

    type: Required[Literal["reference"]]


class SelectConfigSelect(TypedDict, total=False):
    options: Required[List[str]]

    can_create: Annotated[bool, PropertyInfo(alias="canCreate")]


class Select(TypedDict, total=False):
    config_select: Required[Annotated[SelectConfigSelect, PropertyInfo(alias="configSelect")]]

    type: Required[Literal["select"]]


class Text(TypedDict, total=False):
    type: Required[Literal["text"]]


class URL(TypedDict, total=False):
    type: Required[Literal["url"]]


class User(TypedDict, total=False):
    type: Required[Literal["user"]]


class Lookup(TypedDict, total=False):
    lookup_external_column: Required[
        Annotated[update_column_union.LookupLookupExternalColumn, PropertyInfo(alias="lookupExternalColumn")]
    ]

    lookup_external_column_id: Required[Annotated[str, PropertyInfo(alias="lookupExternalColumnId")]]

    lookup_source_column_id: Required[Annotated[str, PropertyInfo(alias="lookupSourceColumnId")]]

    type: Required[Literal["lookup"]]


UpdateColumnUnion: TypeAlias = Union[
    Boolean, Date, Editor, Expression, File, Float, Integer, Reference, Select, Text, URL, User, Lookup
]
