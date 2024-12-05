# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "EnsureRowsResponse",
    "Data",
    "DataRow",
    "DataRowField",
    "DataRowFieldUnionMember0",
    "DataRowFieldUnionMember0InvalidData",
    "DataRowFieldUnionMember1",
    "DataRowFieldUnionMember1InvalidData",
    "DataRowFieldUnionMember2",
    "DataRowFieldUnionMember2InvalidData",
    "DataRowFieldUnionMember3",
    "DataRowFieldUnionMember3InvalidData",
    "DataRowFieldUnionMember4",
    "DataRowFieldUnionMember4InvalidData",
    "DataRowFieldUnionMember4Value",
    "DataRowFieldUnionMember5",
    "DataRowFieldUnionMember5InvalidData",
    "DataRowFieldUnionMember5Value",
    "DataRowFieldUnionMember6",
    "DataRowFieldUnionMember6InvalidData",
    "DataRowFieldUnionMember6Value",
    "DataRowFieldUnionMember7",
    "DataRowFieldUnionMember7InvalidData",
    "DataRowFieldUnionMember7Value",
    "DataRowFieldUnionMember8",
    "DataRowFieldUnionMember8InvalidData",
    "DataRowFieldUnionMember9",
    "DataRowFieldUnionMember9InvalidData",
    "DataRowFieldUnionMember9Value",
    "DataRowFieldUnionMember9ValueURL",
    "DataRowFieldUnionMember10",
    "DataRowFieldUnionMember10InvalidData",
    "DataRowFieldUnionMember10Value",
    "DataRowFieldUnionMember11",
    "DataRowFieldUnionMember11Value",
    "DataRowFieldUnionMember11InvalidData",
    "DataRowFieldUnionMember12",
    "DataRowFieldUnionMember12InvalidData",
    "DataRowFieldUnionMember12Value",
    "DataRowFieldUnionMember12ValueUnionMember0",
    "DataRowFieldUnionMember12ValueUnionMember0InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember1",
    "DataRowFieldUnionMember12ValueUnionMember1InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember2",
    "DataRowFieldUnionMember12ValueUnionMember2InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember3",
    "DataRowFieldUnionMember12ValueUnionMember3InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember4",
    "DataRowFieldUnionMember12ValueUnionMember4InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember4Value",
    "DataRowFieldUnionMember12ValueUnionMember5",
    "DataRowFieldUnionMember12ValueUnionMember5InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember5Value",
    "DataRowFieldUnionMember12ValueUnionMember6",
    "DataRowFieldUnionMember12ValueUnionMember6InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember6Value",
    "DataRowFieldUnionMember12ValueUnionMember7",
    "DataRowFieldUnionMember12ValueUnionMember7InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember7Value",
    "DataRowFieldUnionMember12ValueUnionMember8",
    "DataRowFieldUnionMember12ValueUnionMember8InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember9",
    "DataRowFieldUnionMember12ValueUnionMember9InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember9Value",
    "DataRowFieldUnionMember12ValueUnionMember9ValueURL",
    "DataRowFieldUnionMember12ValueUnionMember10",
    "DataRowFieldUnionMember12ValueUnionMember10InvalidData",
    "DataRowFieldUnionMember12ValueUnionMember10Value",
]


class DataRowFieldUnionMember0InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember0(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember0InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldUnionMember1InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember1(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember1InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataRowFieldUnionMember2InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember2(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember2InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataRowFieldUnionMember3InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember3(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember3InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataRowFieldUnionMember4InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember4Value(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataRowFieldUnionMember4(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember4InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember4Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember5InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember5Value(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataRowFieldUnionMember5(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember5InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember5Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember6InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember6Value(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataRowFieldUnionMember6(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember6InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember6Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember7InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember7Value(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataRowFieldUnionMember7(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember7InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember7Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember8InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember8(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember8InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldUnionMember9InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember9ValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataRowFieldUnionMember9Value(BaseModel):
    urls: List[DataRowFieldUnionMember9ValueURL]


class DataRowFieldUnionMember9(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember9InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember9Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember10InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember10Value(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataRowFieldUnionMember10(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember10InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember10Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember11Value(BaseModel):
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """The error message from executing the expression, if one occurred."""

    invalid_result: Optional[object] = FieldInfo(alias="invalidResult", default=None)
    """Expression result that is not a valid return value type."""

    result: Union[str, float, None] = None
    """The return value from executing the expression."""


class DataRowFieldUnionMember11InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember11(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["expression"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    value: DataRowFieldUnionMember11Value

    invalid_data: Optional[DataRowFieldUnionMember11InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    version: Optional[float] = None


class DataRowFieldUnionMember12InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember0InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember0(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember0InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember1InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember1(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember1InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember2InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember2(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember2InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember3InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember3(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember3InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember4InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember4Value(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataRowFieldUnionMember12ValueUnionMember4(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember4InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12ValueUnionMember4Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember5InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember5Value(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataRowFieldUnionMember12ValueUnionMember5(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember5InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12ValueUnionMember5Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember6InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember6Value(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataRowFieldUnionMember12ValueUnionMember6(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember6InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12ValueUnionMember6Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember7InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember7Value(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataRowFieldUnionMember12ValueUnionMember7(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember7InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12ValueUnionMember7Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember8InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember8(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember8InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember9InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember9ValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember9Value(BaseModel):
    urls: List[DataRowFieldUnionMember12ValueUnionMember9ValueURL]


class DataRowFieldUnionMember12ValueUnionMember9(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember9InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12ValueUnionMember9Value] = None

    version: Optional[float] = None


class DataRowFieldUnionMember12ValueUnionMember10InvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUnionMember12ValueUnionMember10Value(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataRowFieldUnionMember12ValueUnionMember10(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12ValueUnionMember10InvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12ValueUnionMember10Value] = None

    version: Optional[float] = None


DataRowFieldUnionMember12Value: TypeAlias = Union[
    DataRowFieldUnionMember12ValueUnionMember0,
    DataRowFieldUnionMember12ValueUnionMember1,
    DataRowFieldUnionMember12ValueUnionMember2,
    DataRowFieldUnionMember12ValueUnionMember3,
    DataRowFieldUnionMember12ValueUnionMember4,
    DataRowFieldUnionMember12ValueUnionMember5,
    DataRowFieldUnionMember12ValueUnionMember6,
    DataRowFieldUnionMember12ValueUnionMember7,
    DataRowFieldUnionMember12ValueUnionMember8,
    DataRowFieldUnionMember12ValueUnionMember9,
    DataRowFieldUnionMember12ValueUnionMember10,
]


class DataRowFieldUnionMember12(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["lookup"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUnionMember12InvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUnionMember12Value] = None

    version: Optional[float] = None


DataRowField: TypeAlias = Union[
    DataRowFieldUnionMember0,
    DataRowFieldUnionMember1,
    DataRowFieldUnionMember2,
    DataRowFieldUnionMember3,
    DataRowFieldUnionMember4,
    DataRowFieldUnionMember5,
    DataRowFieldUnionMember6,
    DataRowFieldUnionMember7,
    DataRowFieldUnionMember8,
    DataRowFieldUnionMember9,
    DataRowFieldUnionMember10,
    DataRowFieldUnionMember11,
    DataRowFieldUnionMember12,
]


class DataRow(BaseModel):
    id: str
    """Deep Origin system ID."""

    date_created: str = FieldInfo(alias="dateCreated")

    hid: str

    type: Literal["row"]

    created_by_user_drn: Optional[str] = FieldInfo(alias="createdByUserDrn", default=None)

    creation_block_id: Optional[str] = FieldInfo(alias="creationBlockId", default=None)

    creation_parent_id: Optional[str] = FieldInfo(alias="creationParentId", default=None)

    date_updated: Optional[str] = FieldInfo(alias="dateUpdated", default=None)

    edited_by_user_drn: Optional[str] = FieldInfo(alias="editedByUserDrn", default=None)

    fields: Optional[List[DataRowField]] = None

    is_template: Optional[bool] = FieldInfo(alias="isTemplate", default=None)

    name: Optional[str] = None

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)

    validation_status: Optional[Literal["valid", "invalid"]] = FieldInfo(alias="validationStatus", default=None)


class Data(BaseModel):
    rows: List[DataRow]


class EnsureRowsResponse(BaseModel):
    data: Data
