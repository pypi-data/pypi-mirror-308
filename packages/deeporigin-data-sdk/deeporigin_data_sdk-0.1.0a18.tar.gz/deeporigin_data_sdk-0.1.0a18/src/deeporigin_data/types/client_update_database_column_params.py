# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .shared_params.update_column import UpdateColumn

__all__ = ["ClientUpdateDatabaseColumnParams"]


class ClientUpdateDatabaseColumnParams(TypedDict, total=False):
    column: Required[UpdateColumn]

    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]
