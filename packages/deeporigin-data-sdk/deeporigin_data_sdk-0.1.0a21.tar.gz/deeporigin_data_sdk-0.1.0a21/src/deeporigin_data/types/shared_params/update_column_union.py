# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .lookup_external_column import LookupExternalColumn

__all__ = ["UpdateColumnUnion", "ConfigSelect", "ConfigFile", "ConfigNumeric"]


class ConfigSelect(TypedDict, total=False):
    options: Required[List[str]]

    can_create: Annotated[bool, PropertyInfo(alias="canCreate")]


class ConfigFile(TypedDict, total=False):
    allowed_extensions: Annotated[List[str], PropertyInfo(alias="allowedExtensions")]


class ConfigNumeric(TypedDict, total=False):
    unit: str


class UpdateColumnUnion(TypedDict, total=False):
    config_select: Required[Annotated[ConfigSelect, PropertyInfo(alias="configSelect")]]

    expression_code: Required[Annotated[str, PropertyInfo(alias="expressionCode")]]

    expression_return_type: Required[
        Annotated[Literal["text", "float", "integer"], PropertyInfo(alias="expressionReturnType")]
    ]

    lookup_external_column: Required[Annotated[LookupExternalColumn, PropertyInfo(alias="lookupExternalColumn")]]

    lookup_external_column_id: Required[Annotated[str, PropertyInfo(alias="lookupExternalColumnId")]]

    lookup_source_column_id: Required[Annotated[str, PropertyInfo(alias="lookupSourceColumnId")]]

    reference_database_row_id: Required[Annotated[str, PropertyInfo(alias="referenceDatabaseRowId")]]

    type: Required[
        Literal[
            "lookup",
            "user",
            "url",
            "text",
            "select",
            "reference",
            "integer",
            "float",
            "file",
            "expression",
            "editor",
            "date",
            "boolean",
        ]
    ]

    config_file: Annotated[ConfigFile, PropertyInfo(alias="configFile")]

    config_numeric: Annotated[ConfigNumeric, PropertyInfo(alias="configNumeric")]
