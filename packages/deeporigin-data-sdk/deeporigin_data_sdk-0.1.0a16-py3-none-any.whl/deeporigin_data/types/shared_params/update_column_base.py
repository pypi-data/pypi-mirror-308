# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["UpdateColumnBase"]


class UpdateColumnBase(TypedDict, total=False):
    cardinality: Literal["one", "many"]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    name: str

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]

    type: Literal[
        "boolean",
        "date",
        "editor",
        "expression",
        "file",
        "float",
        "integer",
        "lookup",
        "reference",
        "select",
        "text",
        "url",
        "user",
    ]
