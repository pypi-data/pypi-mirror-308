# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .shared_params.add_column_base import AddColumnBase
from .shared_params.add_column_union import AddColumnUnion

__all__ = ["ClientImportRowsParams", "AddColumn"]


class ClientImportRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    add_columns: Annotated[Iterable[AddColumn], PropertyInfo(alias="addColumns")]
    """Optionally add additional columns to the database during import."""

    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]


AddColumn: TypeAlias = Union[AddColumnBase, AddColumnUnion]
