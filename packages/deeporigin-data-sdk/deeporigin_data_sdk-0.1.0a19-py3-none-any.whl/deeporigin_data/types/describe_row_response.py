# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel
from .database import Database

__all__ = [
    "DescribeRowResponse",
    "Data",
    "DataDatabaseRow",
    "DataDatabaseRowField",
    "DataDatabaseRowFieldText",
    "DataDatabaseRowFieldTextInvalidData",
    "DataDatabaseRowFieldInteger",
    "DataDatabaseRowFieldIntegerInvalidData",
    "DataDatabaseRowFieldFloat",
    "DataDatabaseRowFieldFloatInvalidData",
    "DataDatabaseRowFieldBoolean",
    "DataDatabaseRowFieldBooleanInvalidData",
    "DataDatabaseRowFieldReference",
    "DataDatabaseRowFieldReferenceInvalidData",
    "DataDatabaseRowFieldReferenceValue",
    "DataDatabaseRowFieldEditor",
    "DataDatabaseRowFieldEditorInvalidData",
    "DataDatabaseRowFieldEditorValue",
    "DataDatabaseRowFieldFile",
    "DataDatabaseRowFieldFileInvalidData",
    "DataDatabaseRowFieldFileValue",
    "DataDatabaseRowFieldSelect",
    "DataDatabaseRowFieldSelectInvalidData",
    "DataDatabaseRowFieldSelectValue",
    "DataDatabaseRowFieldDate",
    "DataDatabaseRowFieldDateInvalidData",
    "DataDatabaseRowFieldURL",
    "DataDatabaseRowFieldURLInvalidData",
    "DataDatabaseRowFieldURLValue",
    "DataDatabaseRowFieldURLValueURL",
    "DataDatabaseRowFieldUser",
    "DataDatabaseRowFieldUserInvalidData",
    "DataDatabaseRowFieldUserValue",
    "DataDatabaseRowFieldExpression",
    "DataDatabaseRowFieldExpressionValue",
    "DataDatabaseRowFieldExpressionInvalidData",
    "DataDatabaseRowFieldLookup",
    "DataDatabaseRowFieldLookupInvalidData",
    "DataDatabaseRowFieldLookupValue",
    "DataDatabaseRowFieldLookupValueText",
    "DataDatabaseRowFieldLookupValueTextInvalidData",
    "DataDatabaseRowFieldLookupValueInteger",
    "DataDatabaseRowFieldLookupValueIntegerInvalidData",
    "DataDatabaseRowFieldLookupValueFloat",
    "DataDatabaseRowFieldLookupValueFloatInvalidData",
    "DataDatabaseRowFieldLookupValueBoolean",
    "DataDatabaseRowFieldLookupValueBooleanInvalidData",
    "DataDatabaseRowFieldLookupValueReference",
    "DataDatabaseRowFieldLookupValueReferenceInvalidData",
    "DataDatabaseRowFieldLookupValueReferenceValue",
    "DataDatabaseRowFieldLookupValueEditor",
    "DataDatabaseRowFieldLookupValueEditorInvalidData",
    "DataDatabaseRowFieldLookupValueEditorValue",
    "DataDatabaseRowFieldLookupValueFile",
    "DataDatabaseRowFieldLookupValueFileInvalidData",
    "DataDatabaseRowFieldLookupValueFileValue",
    "DataDatabaseRowFieldLookupValueSelect",
    "DataDatabaseRowFieldLookupValueSelectInvalidData",
    "DataDatabaseRowFieldLookupValueSelectValue",
    "DataDatabaseRowFieldLookupValueDate",
    "DataDatabaseRowFieldLookupValueDateInvalidData",
    "DataDatabaseRowFieldLookupValueURL",
    "DataDatabaseRowFieldLookupValueURLInvalidData",
    "DataDatabaseRowFieldLookupValueURLValue",
    "DataDatabaseRowFieldLookupValueURLValueURL",
    "DataDatabaseRowFieldLookupValueUser",
    "DataDatabaseRowFieldLookupValueUserInvalidData",
    "DataDatabaseRowFieldLookupValueUserValue",
    "DataWorkspace",
]


class DataDatabaseRowFieldTextInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataDatabaseRowFieldIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataDatabaseRowFieldFloatInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataDatabaseRowFieldBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataDatabaseRowFieldReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataDatabaseRowFieldReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldReferenceValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldEditorInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataDatabaseRowFieldEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldEditorValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldFileInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataDatabaseRowFieldFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldFileValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldSelectInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataDatabaseRowFieldSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldSelectValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldDateInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataDatabaseRowFieldURLInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataDatabaseRowFieldURLValue(BaseModel):
    urls: List[DataDatabaseRowFieldURLValueURL]


class DataDatabaseRowFieldURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldURLValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldUserInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataDatabaseRowFieldUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldUserValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldExpressionValue(BaseModel):
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """The error message from executing the expression, if one occurred."""

    invalid_result: Optional[object] = FieldInfo(alias="invalidResult", default=None)
    """Expression result that is not a valid return value type."""

    result: Union[str, float, None] = None
    """The return value from executing the expression."""


class DataDatabaseRowFieldExpressionInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldExpression(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["expression"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    value: DataDatabaseRowFieldExpressionValue

    invalid_data: Optional[DataDatabaseRowFieldExpressionInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    version: Optional[float] = None


class DataDatabaseRowFieldLookupInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueTextInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueTextInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueIntegerInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueFloatInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueFloatInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueBooleanInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataDatabaseRowFieldLookupValueReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueReferenceInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValueReferenceValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueEditorInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataDatabaseRowFieldLookupValueEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueEditorInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValueEditorValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueFileInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataDatabaseRowFieldLookupValueFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueFileInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValueFileValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueSelectInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataDatabaseRowFieldLookupValueSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueSelectInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValueSelectValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueDateInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueDateInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueURLInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataDatabaseRowFieldLookupValueURLValue(BaseModel):
    urls: List[DataDatabaseRowFieldLookupValueURLValueURL]


class DataDatabaseRowFieldLookupValueURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValueURLValue] = None

    version: Optional[float] = None


class DataDatabaseRowFieldLookupValueUserInvalidData(BaseModel):
    message: Optional[str] = None


class DataDatabaseRowFieldLookupValueUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataDatabaseRowFieldLookupValueUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupValueUserInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValueUserValue] = None

    version: Optional[float] = None


DataDatabaseRowFieldLookupValue: TypeAlias = Annotated[
    Union[
        DataDatabaseRowFieldLookupValueText,
        DataDatabaseRowFieldLookupValueInteger,
        DataDatabaseRowFieldLookupValueFloat,
        DataDatabaseRowFieldLookupValueBoolean,
        DataDatabaseRowFieldLookupValueReference,
        DataDatabaseRowFieldLookupValueEditor,
        DataDatabaseRowFieldLookupValueFile,
        DataDatabaseRowFieldLookupValueSelect,
        DataDatabaseRowFieldLookupValueDate,
        DataDatabaseRowFieldLookupValueURL,
        DataDatabaseRowFieldLookupValueUser,
    ],
    PropertyInfo(discriminator="type"),
]


class DataDatabaseRowFieldLookup(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["lookup"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataDatabaseRowFieldLookupInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataDatabaseRowFieldLookupValue] = None

    version: Optional[float] = None


DataDatabaseRowField: TypeAlias = Annotated[
    Union[
        DataDatabaseRowFieldText,
        DataDatabaseRowFieldInteger,
        DataDatabaseRowFieldFloat,
        DataDatabaseRowFieldBoolean,
        DataDatabaseRowFieldReference,
        DataDatabaseRowFieldEditor,
        DataDatabaseRowFieldFile,
        DataDatabaseRowFieldSelect,
        DataDatabaseRowFieldDate,
        DataDatabaseRowFieldURL,
        DataDatabaseRowFieldUser,
        DataDatabaseRowFieldExpression,
        DataDatabaseRowFieldLookup,
    ],
    PropertyInfo(discriminator="type"),
]


class DataDatabaseRow(BaseModel):
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

    fields: Optional[List[DataDatabaseRowField]] = None

    is_template: Optional[bool] = FieldInfo(alias="isTemplate", default=None)

    name: Optional[str] = None

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)

    validation_status: Optional[Literal["valid", "invalid"]] = FieldInfo(alias="validationStatus", default=None)


class DataWorkspace(BaseModel):
    id: str
    """Deep Origin system ID."""

    date_created: str = FieldInfo(alias="dateCreated")

    hid: str

    name: str

    type: Literal["workspace"]

    created_by_user_drn: Optional[str] = FieldInfo(alias="createdByUserDrn", default=None)

    creation_block_id: Optional[str] = FieldInfo(alias="creationBlockId", default=None)

    creation_parent_id: Optional[str] = FieldInfo(alias="creationParentId", default=None)

    date_updated: Optional[str] = FieldInfo(alias="dateUpdated", default=None)

    edited_by_user_drn: Optional[str] = FieldInfo(alias="editedByUserDrn", default=None)

    editor: Optional[object] = None

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)


Data: TypeAlias = Annotated[Union[Database, DataDatabaseRow, DataWorkspace], PropertyInfo(discriminator="type")]


class DescribeRowResponse(BaseModel):
    data: Data
