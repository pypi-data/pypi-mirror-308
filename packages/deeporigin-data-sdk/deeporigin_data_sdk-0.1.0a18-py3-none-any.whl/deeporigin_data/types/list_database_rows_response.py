# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "ListDatabaseRowsResponse",
    "Data",
    "DataField",
    "DataFieldText",
    "DataFieldTextInvalidData",
    "DataFieldInteger",
    "DataFieldIntegerInvalidData",
    "DataFieldFloat",
    "DataFieldFloatInvalidData",
    "DataFieldBoolean",
    "DataFieldBooleanInvalidData",
    "DataFieldReference",
    "DataFieldReferenceInvalidData",
    "DataFieldReferenceValue",
    "DataFieldEditor",
    "DataFieldEditorInvalidData",
    "DataFieldEditorValue",
    "DataFieldFile",
    "DataFieldFileInvalidData",
    "DataFieldFileValue",
    "DataFieldSelect",
    "DataFieldSelectInvalidData",
    "DataFieldSelectValue",
    "DataFieldDate",
    "DataFieldDateInvalidData",
    "DataFieldURL",
    "DataFieldURLInvalidData",
    "DataFieldURLValue",
    "DataFieldURLValueURL",
    "DataFieldUser",
    "DataFieldUserInvalidData",
    "DataFieldUserValue",
    "DataFieldExpression",
    "DataFieldExpressionValue",
    "DataFieldExpressionInvalidData",
    "DataFieldLookup",
    "DataFieldLookupInvalidData",
    "DataFieldLookupValue",
    "DataFieldLookupValueText",
    "DataFieldLookupValueTextInvalidData",
    "DataFieldLookupValueInteger",
    "DataFieldLookupValueIntegerInvalidData",
    "DataFieldLookupValueFloat",
    "DataFieldLookupValueFloatInvalidData",
    "DataFieldLookupValueBoolean",
    "DataFieldLookupValueBooleanInvalidData",
    "DataFieldLookupValueReference",
    "DataFieldLookupValueReferenceInvalidData",
    "DataFieldLookupValueReferenceValue",
    "DataFieldLookupValueEditor",
    "DataFieldLookupValueEditorInvalidData",
    "DataFieldLookupValueEditorValue",
    "DataFieldLookupValueFile",
    "DataFieldLookupValueFileInvalidData",
    "DataFieldLookupValueFileValue",
    "DataFieldLookupValueSelect",
    "DataFieldLookupValueSelectInvalidData",
    "DataFieldLookupValueSelectValue",
    "DataFieldLookupValueDate",
    "DataFieldLookupValueDateInvalidData",
    "DataFieldLookupValueURL",
    "DataFieldLookupValueURLInvalidData",
    "DataFieldLookupValueURLValue",
    "DataFieldLookupValueURLValueURL",
    "DataFieldLookupValueUser",
    "DataFieldLookupValueUserInvalidData",
    "DataFieldLookupValueUserValue",
]


class DataFieldTextInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataFieldIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataFieldFloatInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataFieldBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataFieldReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataFieldReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldReferenceValue] = None

    version: Optional[float] = None


class DataFieldEditorInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataFieldEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldEditorValue] = None

    version: Optional[float] = None


class DataFieldFileInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataFieldFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldFileValue] = None

    version: Optional[float] = None


class DataFieldSelectInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataFieldSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldSelectValue] = None

    version: Optional[float] = None


class DataFieldDateInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataFieldURLInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataFieldURLValue(BaseModel):
    urls: List[DataFieldURLValueURL]


class DataFieldURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldURLValue] = None

    version: Optional[float] = None


class DataFieldUserInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataFieldUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldUserValue] = None

    version: Optional[float] = None


class DataFieldExpressionValue(BaseModel):
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """The error message from executing the expression, if one occurred."""

    invalid_result: Optional[object] = FieldInfo(alias="invalidResult", default=None)
    """Expression result that is not a valid return value type."""

    result: Union[str, float, None] = None
    """The return value from executing the expression."""


class DataFieldExpressionInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldExpression(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["expression"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    value: DataFieldExpressionValue

    invalid_data: Optional[DataFieldExpressionInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    version: Optional[float] = None


class DataFieldLookupInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueTextInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataFieldLookupValueIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class DataFieldLookupValueFloatInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class DataFieldLookupValueBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class DataFieldLookupValueReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class DataFieldLookupValueReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValueReferenceValue] = None

    version: Optional[float] = None


class DataFieldLookupValueEditorInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class DataFieldLookupValueEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValueEditorValue] = None

    version: Optional[float] = None


class DataFieldLookupValueFileInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class DataFieldLookupValueFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValueFileValue] = None

    version: Optional[float] = None


class DataFieldLookupValueSelectInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class DataFieldLookupValueSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValueSelectValue] = None

    version: Optional[float] = None


class DataFieldLookupValueDateInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class DataFieldLookupValueURLInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class DataFieldLookupValueURLValue(BaseModel):
    urls: List[DataFieldLookupValueURLValueURL]


class DataFieldLookupValueURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValueURLValue] = None

    version: Optional[float] = None


class DataFieldLookupValueUserInvalidData(BaseModel):
    message: Optional[str] = None


class DataFieldLookupValueUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class DataFieldLookupValueUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupValueUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValueUserValue] = None

    version: Optional[float] = None


DataFieldLookupValue: TypeAlias = Annotated[
    Union[
        DataFieldLookupValueText,
        DataFieldLookupValueInteger,
        DataFieldLookupValueFloat,
        DataFieldLookupValueBoolean,
        DataFieldLookupValueReference,
        DataFieldLookupValueEditor,
        DataFieldLookupValueFile,
        DataFieldLookupValueSelect,
        DataFieldLookupValueDate,
        DataFieldLookupValueURL,
        DataFieldLookupValueUser,
    ],
    PropertyInfo(discriminator="type"),
]


class DataFieldLookup(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["lookup"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[DataFieldLookupInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[DataFieldLookupValue] = None

    version: Optional[float] = None


DataField: TypeAlias = Annotated[
    Union[
        DataFieldText,
        DataFieldInteger,
        DataFieldFloat,
        DataFieldBoolean,
        DataFieldReference,
        DataFieldEditor,
        DataFieldFile,
        DataFieldSelect,
        DataFieldDate,
        DataFieldURL,
        DataFieldUser,
        DataFieldExpression,
        DataFieldLookup,
    ],
    PropertyInfo(discriminator="type"),
]


class Data(BaseModel):
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

    fields: Optional[List[DataField]] = None

    is_template: Optional[bool] = FieldInfo(alias="isTemplate", default=None)

    name: Optional[str] = None

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)

    validation_status: Optional[Literal["valid", "invalid"]] = FieldInfo(alias="validationStatus", default=None)


class ListDatabaseRowsResponse(BaseModel):
    data: List[Data]
