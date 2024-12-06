# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .shared_params.add_column_base import AddColumnBase
from .shared_params.add_column_union import AddColumnUnion

__all__ = ["ClientAddDatabaseColumnParams", "Column"]


class ClientAddDatabaseColumnParams(TypedDict, total=False):
    column: Required[Column]

    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]


Column: TypeAlias = Union[AddColumnBase, AddColumnUnion]
