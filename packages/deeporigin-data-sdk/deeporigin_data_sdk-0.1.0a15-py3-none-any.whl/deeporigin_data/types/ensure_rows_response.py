# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "EnsureRowsResponse",
    "Data",
    "DataRow",
    "DataRowField",
    "DataRowFieldText",
    "DataRowFieldTextInvalidData",
    "DataRowFieldInteger",
    "DataRowFieldIntegerInvalidData",
    "DataRowFieldFloat",
    "DataRowFieldFloatInvalidData",
    "DataRowFieldBoolean",
    "DataRowFieldBooleanInvalidData",
    "DataRowFieldReference",
    "DataRowFieldReferenceInvalidData",
    "DataRowFieldReferenceValue",
    "DataRowFieldEditor",
    "DataRowFieldEditorInvalidData",
    "DataRowFieldEditorValue",
    "DataRowFieldFile",
    "DataRowFieldFileInvalidData",
    "DataRowFieldFileValue",
    "DataRowFieldSelect",
    "DataRowFieldSelectInvalidData",
    "DataRowFieldSelectValue",
    "DataRowFieldDate",
    "DataRowFieldDateInvalidData",
    "DataRowFieldURL",
    "DataRowFieldURLInvalidData",
    "DataRowFieldURLValue",
    "DataRowFieldURLValueURL",
    "DataRowFieldUser",
    "DataRowFieldUserInvalidData",
    "DataRowFieldUserValue",
    "DataRowFieldExpression",
    "DataRowFieldExpressionValue",
    "DataRowFieldExpressionInvalidData",
    "DataRowFieldLookup",
    "DataRowFieldLookupInvalidData",
    "DataRowFieldLookupValue",
    "DataRowFieldLookupValueText",
    "DataRowFieldLookupValueTextInvalidData",
    "DataRowFieldLookupValueInteger",
    "DataRowFieldLookupValueIntegerInvalidData",
    "DataRowFieldLookupValueFloat",
    "DataRowFieldLookupValueFloatInvalidData",
    "DataRowFieldLookupValueBoolean",
    "DataRowFieldLookupValueBooleanInvalidData",
    "DataRowFieldLookupValueReference",
    "DataRowFieldLookupValueReferenceInvalidData",
    "DataRowFieldLookupValueReferenceValue",
    "DataRowFieldLookupValueEditor",
    "DataRowFieldLookupValueEditorInvalidData",
    "DataRowFieldLookupValueEditorValue",
    "DataRowFieldLookupValueFile",
    "DataRowFieldLookupValueFileInvalidData",
    "DataRowFieldLookupValueFileValue",
    "DataRowFieldLookupValueSelect",
    "DataRowFieldLookupValueSelectInvalidData",
    "DataRowFieldLookupValueSelectValue",
    "DataRowFieldLookupValueDate",
    "DataRowFieldLookupValueDateInvalidData",
    "DataRowFieldLookupValueURL",
    "DataRowFieldLookupValueURLInvalidData",
    "DataRowFieldLookupValueURLValue",
    "DataRowFieldLookupValueURLValueURL",
    "DataRowFieldLookupValueUser",
    "DataRowFieldLookupValueUserInvalidData",
    "DataRowFieldLookupValueUserValue",
]


class DataRowFieldTextInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataRowFieldFloatInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataRowFieldBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataRowFieldReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataRowFieldReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldReferenceValue] = None

    version: Optional[float] = None


class DataRowFieldEditorInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataRowFieldEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldEditorValue] = None

    version: Optional[float] = None


class DataRowFieldFileInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataRowFieldFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldFileValue] = None

    version: Optional[float] = None


class DataRowFieldSelectInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataRowFieldSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldSelectValue] = None

    version: Optional[float] = None


class DataRowFieldDateInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldURLInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataRowFieldURLValue(BaseModel):
    urls: List[DataRowFieldURLValueURL]


class DataRowFieldURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldURLValue] = None

    version: Optional[float] = None


class DataRowFieldUserInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataRowFieldUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldUserValue] = None

    version: Optional[float] = None


class DataRowFieldExpressionValue(BaseModel):
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """The error message from executing the expression, if one occurred."""

    invalid_result: Optional[object] = FieldInfo(alias="invalidResult", default=None)
    """Expression result that is not a valid return value type."""

    result: Union[str, float, None] = None
    """The return value from executing the expression."""


class DataRowFieldExpressionInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldExpression(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["expression"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    value: DataRowFieldExpressionValue

    invalid_data: Optional[DataRowFieldExpressionInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    version: Optional[float] = None


class DataRowFieldLookupInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueTextInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldLookupValueIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataRowFieldLookupValueFloatInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataRowFieldLookupValueBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataRowFieldLookupValueReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataRowFieldLookupValueReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValueReferenceValue] = None

    version: Optional[float] = None


class DataRowFieldLookupValueEditorInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataRowFieldLookupValueEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValueEditorValue] = None

    version: Optional[float] = None


class DataRowFieldLookupValueFileInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataRowFieldLookupValueFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValueFileValue] = None

    version: Optional[float] = None


class DataRowFieldLookupValueSelectInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataRowFieldLookupValueSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValueSelectValue] = None

    version: Optional[float] = None


class DataRowFieldLookupValueDateInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataRowFieldLookupValueURLInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataRowFieldLookupValueURLValue(BaseModel):
    urls: List[DataRowFieldLookupValueURLValueURL]


class DataRowFieldLookupValueURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValueURLValue] = None

    version: Optional[float] = None


class DataRowFieldLookupValueUserInvalidData(BaseModel):
    message: Optional[str] = None


class DataRowFieldLookupValueUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataRowFieldLookupValueUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupValueUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValueUserValue] = None

    version: Optional[float] = None


DataRowFieldLookupValue: TypeAlias = Annotated[
    Union[
        DataRowFieldLookupValueText,
        DataRowFieldLookupValueInteger,
        DataRowFieldLookupValueFloat,
        DataRowFieldLookupValueBoolean,
        DataRowFieldLookupValueReference,
        DataRowFieldLookupValueEditor,
        DataRowFieldLookupValueFile,
        DataRowFieldLookupValueSelect,
        DataRowFieldLookupValueDate,
        DataRowFieldLookupValueURL,
        DataRowFieldLookupValueUser,
    ],
    PropertyInfo(discriminator="type"),
]


class DataRowFieldLookup(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["lookup"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataRowFieldLookupInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataRowFieldLookupValue] = None

    version: Optional[float] = None


DataRowField: TypeAlias = Annotated[
    Union[
        DataRowFieldText,
        DataRowFieldInteger,
        DataRowFieldFloat,
        DataRowFieldBoolean,
        DataRowFieldReference,
        DataRowFieldEditor,
        DataRowFieldFile,
        DataRowFieldSelect,
        DataRowFieldDate,
        DataRowFieldURL,
        DataRowFieldUser,
        DataRowFieldExpression,
        DataRowFieldLookup,
    ],
    PropertyInfo(discriminator="type"),
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
