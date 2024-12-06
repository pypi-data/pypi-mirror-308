# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .update_column_base import UpdateColumnBase
from .update_column_union import UpdateColumnUnion

__all__ = ["UpdateColumn"]

UpdateColumn: TypeAlias = Union[UpdateColumnBase, UpdateColumnUnion]
