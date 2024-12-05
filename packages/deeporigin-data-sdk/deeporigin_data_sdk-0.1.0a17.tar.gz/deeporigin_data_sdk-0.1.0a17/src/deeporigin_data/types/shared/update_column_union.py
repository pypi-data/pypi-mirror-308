# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

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
    "UnionMember12LookupExternalColumn",
]


class Type(BaseModel):
    type: Literal["boolean"]


class UnionMember3(BaseModel):
    expression_code: str = FieldInfo(alias="expressionCode")

    expression_return_type: Literal["text", "float", "integer"] = FieldInfo(alias="expressionReturnType")

    type: Literal["expression"]


class UnionMember4ConfigFile(BaseModel):
    allowed_extensions: Optional[List[str]] = FieldInfo(alias="allowedExtensions", default=None)


class UnionMember4(BaseModel):
    type: Literal["file"]

    config_file: Optional[UnionMember4ConfigFile] = FieldInfo(alias="configFile", default=None)


class UnionMember5ConfigNumeric(BaseModel):
    unit: Optional[str] = None


class UnionMember5(BaseModel):
    type: Literal["float"]

    config_numeric: Optional[UnionMember5ConfigNumeric] = FieldInfo(alias="configNumeric", default=None)


class UnionMember6ConfigNumeric(BaseModel):
    unit: Optional[str] = None


class UnionMember6(BaseModel):
    type: Literal["integer"]

    config_numeric: Optional[UnionMember6ConfigNumeric] = FieldInfo(alias="configNumeric", default=None)


class UnionMember7(BaseModel):
    reference_database_row_id: str = FieldInfo(alias="referenceDatabaseRowId")

    type: Literal["reference"]


class UnionMember8ConfigSelect(BaseModel):
    options: List[str]

    can_create: Optional[bool] = FieldInfo(alias="canCreate", default=None)


class UnionMember8(BaseModel):
    config_select: UnionMember8ConfigSelect = FieldInfo(alias="configSelect")

    type: Literal["select"]


class UnionMember12LookupExternalColumn:
    pass


class UnionMember12(BaseModel):
    lookup_external_column: UnionMember12LookupExternalColumn = FieldInfo(alias="lookupExternalColumn")

    lookup_external_column_id: str = FieldInfo(alias="lookupExternalColumnId")

    lookup_source_column_id: str = FieldInfo(alias="lookupSourceColumnId")

    type: Literal["lookup"]


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
