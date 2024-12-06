# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .lookup_external_column import LookupExternalColumn

__all__ = ["UpdateColumnUnion", "ConfigSelect", "ConfigFile", "ConfigNumeric"]


class ConfigSelect(BaseModel):
    options: List[str]

    can_create: Optional[bool] = FieldInfo(alias="canCreate", default=None)


class ConfigFile(BaseModel):
    allowed_extensions: Optional[List[str]] = FieldInfo(alias="allowedExtensions", default=None)


class ConfigNumeric(BaseModel):
    unit: Optional[str] = None


class UpdateColumnUnion(BaseModel):
    config_select: ConfigSelect = FieldInfo(alias="configSelect")

    expression_code: str = FieldInfo(alias="expressionCode")

    expression_return_type: Literal["text", "float", "integer"] = FieldInfo(alias="expressionReturnType")

    lookup_external_column: LookupExternalColumn = FieldInfo(alias="lookupExternalColumn")

    lookup_external_column_id: str = FieldInfo(alias="lookupExternalColumnId")

    lookup_source_column_id: str = FieldInfo(alias="lookupSourceColumnId")

    reference_database_row_id: str = FieldInfo(alias="referenceDatabaseRowId")

    type: Literal[
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

    config_file: Optional[ConfigFile] = FieldInfo(alias="configFile", default=None)

    config_numeric: Optional[ConfigNumeric] = FieldInfo(alias="configNumeric", default=None)
