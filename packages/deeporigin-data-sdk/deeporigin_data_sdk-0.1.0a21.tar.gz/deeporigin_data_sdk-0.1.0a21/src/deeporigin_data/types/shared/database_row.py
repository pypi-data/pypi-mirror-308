# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "DatabaseRow",
    "Field",
    "FieldText",
    "FieldTextInvalidData",
    "FieldInteger",
    "FieldIntegerInvalidData",
    "FieldFloat",
    "FieldFloatInvalidData",
    "FieldBoolean",
    "FieldBooleanInvalidData",
    "FieldReference",
    "FieldReferenceInvalidData",
    "FieldReferenceValue",
    "FieldEditor",
    "FieldEditorInvalidData",
    "FieldEditorValue",
    "FieldFile",
    "FieldFileInvalidData",
    "FieldFileValue",
    "FieldSelect",
    "FieldSelectInvalidData",
    "FieldSelectValue",
    "FieldDate",
    "FieldDateInvalidData",
    "FieldURL",
    "FieldURLInvalidData",
    "FieldURLValue",
    "FieldURLValueURL",
    "FieldUser",
    "FieldUserInvalidData",
    "FieldUserValue",
    "FieldExpression",
    "FieldExpressionValue",
    "FieldExpressionInvalidData",
    "FieldLookup",
    "FieldLookupInvalidData",
    "FieldLookupValue",
    "FieldLookupValueText",
    "FieldLookupValueTextInvalidData",
    "FieldLookupValueInteger",
    "FieldLookupValueIntegerInvalidData",
    "FieldLookupValueFloat",
    "FieldLookupValueFloatInvalidData",
    "FieldLookupValueBoolean",
    "FieldLookupValueBooleanInvalidData",
    "FieldLookupValueReference",
    "FieldLookupValueReferenceInvalidData",
    "FieldLookupValueReferenceValue",
    "FieldLookupValueEditor",
    "FieldLookupValueEditorInvalidData",
    "FieldLookupValueEditorValue",
    "FieldLookupValueFile",
    "FieldLookupValueFileInvalidData",
    "FieldLookupValueFileValue",
    "FieldLookupValueSelect",
    "FieldLookupValueSelectInvalidData",
    "FieldLookupValueSelectValue",
    "FieldLookupValueDate",
    "FieldLookupValueDateInvalidData",
    "FieldLookupValueURL",
    "FieldLookupValueURLInvalidData",
    "FieldLookupValueURLValue",
    "FieldLookupValueURLValueURL",
    "FieldLookupValueUser",
    "FieldLookupValueUserInvalidData",
    "FieldLookupValueUserValue",
]


class FieldTextInvalidData(BaseModel):
    message: Optional[str] = None


class FieldText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class FieldInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class FieldFloatInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class FieldBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class FieldBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class FieldReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class FieldReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class FieldReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldReferenceValue] = None

    version: Optional[float] = None


class FieldEditorInvalidData(BaseModel):
    message: Optional[str] = None


class FieldEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class FieldEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldEditorValue] = None

    version: Optional[float] = None


class FieldFileInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class FieldFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFileValue] = None

    version: Optional[float] = None


class FieldSelectInvalidData(BaseModel):
    message: Optional[str] = None


class FieldSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class FieldSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldSelectValue] = None

    version: Optional[float] = None


class FieldDateInvalidData(BaseModel):
    message: Optional[str] = None


class FieldDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldURLInvalidData(BaseModel):
    message: Optional[str] = None


class FieldURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class FieldURLValue(BaseModel):
    urls: List[FieldURLValueURL]


class FieldURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldURLValue] = None

    version: Optional[float] = None


class FieldUserInvalidData(BaseModel):
    message: Optional[str] = None


class FieldUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class FieldUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldUserValue] = None

    version: Optional[float] = None


class FieldExpressionValue(BaseModel):
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """The error message from executing the expression, if one occurred."""

    invalid_result: Optional[object] = FieldInfo(alias="invalidResult", default=None)
    """Expression result that is not a valid return value type."""

    result: Union[str, float, None] = None
    """The return value from executing the expression."""


class FieldExpressionInvalidData(BaseModel):
    message: Optional[str] = None


class FieldExpression(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["expression"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    value: FieldExpressionValue

    invalid_data: Optional[FieldExpressionInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    version: Optional[float] = None


class FieldLookupInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueTextInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldLookupValueIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class FieldLookupValueFloatInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class FieldLookupValueBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class FieldLookupValueReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class FieldLookupValueReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValueReferenceValue] = None

    version: Optional[float] = None


class FieldLookupValueEditorInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class FieldLookupValueEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValueEditorValue] = None

    version: Optional[float] = None


class FieldLookupValueFileInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class FieldLookupValueFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValueFileValue] = None

    version: Optional[float] = None


class FieldLookupValueSelectInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class FieldLookupValueSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValueSelectValue] = None

    version: Optional[float] = None


class FieldLookupValueDateInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldLookupValueURLInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class FieldLookupValueURLValue(BaseModel):
    urls: List[FieldLookupValueURLValueURL]


class FieldLookupValueURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValueURLValue] = None

    version: Optional[float] = None


class FieldLookupValueUserInvalidData(BaseModel):
    message: Optional[str] = None


class FieldLookupValueUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class FieldLookupValueUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupValueUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValueUserValue] = None

    version: Optional[float] = None


FieldLookupValue: TypeAlias = Annotated[
    Union[
        FieldLookupValueText,
        FieldLookupValueInteger,
        FieldLookupValueFloat,
        FieldLookupValueBoolean,
        FieldLookupValueReference,
        FieldLookupValueEditor,
        FieldLookupValueFile,
        FieldLookupValueSelect,
        FieldLookupValueDate,
        FieldLookupValueURL,
        FieldLookupValueUser,
    ],
    PropertyInfo(discriminator="type"),
]


class FieldLookup(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["lookup"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldLookupInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldLookupValue] = None

    version: Optional[float] = None


Field: TypeAlias = Annotated[
    Union[
        FieldText,
        FieldInteger,
        FieldFloat,
        FieldBoolean,
        FieldReference,
        FieldEditor,
        FieldFile,
        FieldSelect,
        FieldDate,
        FieldURL,
        FieldUser,
        FieldExpression,
        FieldLookup,
    ],
    PropertyInfo(discriminator="type"),
]


class DatabaseRow(BaseModel):
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

    fields: Optional[List[Field]] = None

    is_template: Optional[bool] = FieldInfo(alias="isTemplate", default=None)

    name: Optional[str] = None

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)

    validation_status: Optional[Literal["valid", "invalid"]] = FieldInfo(alias="validationStatus", default=None)
