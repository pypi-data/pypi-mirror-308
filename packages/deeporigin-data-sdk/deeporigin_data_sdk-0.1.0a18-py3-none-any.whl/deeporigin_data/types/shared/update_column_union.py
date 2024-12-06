# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from ..._utils import PropertyInfo
from ..._models import BaseModel

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
    "LookupLookupExternalColumn",
]


class Boolean(BaseModel):
    type: Literal["boolean"]


class Date(BaseModel):
    type: Literal["date"]


class Editor(BaseModel):
    type: Literal["editor"]


class Expression(BaseModel):
    expression_code: str = FieldInfo(alias="expressionCode")

    expression_return_type: Literal["text", "float", "integer"] = FieldInfo(alias="expressionReturnType")

    type: Literal["expression"]


class FileConfigFile(BaseModel):
    allowed_extensions: Optional[List[str]] = FieldInfo(alias="allowedExtensions", default=None)


class File(BaseModel):
    type: Literal["file"]

    config_file: Optional[FileConfigFile] = FieldInfo(alias="configFile", default=None)


class FloatConfigNumeric(BaseModel):
    unit: Optional[str] = None


class Float(BaseModel):
    type: Literal["float"]

    config_numeric: Optional[FloatConfigNumeric] = FieldInfo(alias="configNumeric", default=None)


class IntegerConfigNumeric(BaseModel):
    unit: Optional[str] = None


class Integer(BaseModel):
    type: Literal["integer"]

    config_numeric: Optional[IntegerConfigNumeric] = FieldInfo(alias="configNumeric", default=None)


class Reference(BaseModel):
    reference_database_row_id: str = FieldInfo(alias="referenceDatabaseRowId")

    type: Literal["reference"]


class SelectConfigSelect(BaseModel):
    options: List[str]

    can_create: Optional[bool] = FieldInfo(alias="canCreate", default=None)


class Select(BaseModel):
    config_select: SelectConfigSelect = FieldInfo(alias="configSelect")

    type: Literal["select"]


class Text(BaseModel):
    type: Literal["text"]


class URL(BaseModel):
    type: Literal["url"]


class User(BaseModel):
    type: Literal["user"]


class LookupLookupExternalColumn:
    pass


class Lookup(BaseModel):
    lookup_external_column: LookupLookupExternalColumn = FieldInfo(alias="lookupExternalColumn")

    lookup_external_column_id: str = FieldInfo(alias="lookupExternalColumnId")

    lookup_source_column_id: str = FieldInfo(alias="lookupSourceColumnId")

    type: Literal["lookup"]


UpdateColumnUnion: TypeAlias = Annotated[
    Union[Boolean, Date, Editor, Expression, File, Float, Integer, Reference, Select, Text, URL, User, Lookup],
    PropertyInfo(discriminator="type"),
]
