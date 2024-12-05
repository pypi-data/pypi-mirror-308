# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "ListMessagesResponse",
    "Data",
    "DataMessage",
    "DataMessageContent",
    "DataMessageContentUnionMember0",
    "DataMessageContentUnionMember0Text",
    "DataMessageContentUnionMember1",
    "DataMessageContentUnionMember1ImageFile",
    "DataMessageContentUnionMember2",
    "DataMessageContentUnionMember2ImageURL",
    "DataMessageContentUnionMember3",
]


class DataMessageContentUnionMember0Text(BaseModel):
    value: str


class DataMessageContentUnionMember0(BaseModel):
    text: DataMessageContentUnionMember0Text

    type: Literal["text"]


class DataMessageContentUnionMember1ImageFile(BaseModel):
    file_id: str


class DataMessageContentUnionMember1(BaseModel):
    image_file: DataMessageContentUnionMember1ImageFile

    type: Literal["image_file"]


class DataMessageContentUnionMember2ImageURL(BaseModel):
    url: str


class DataMessageContentUnionMember2(BaseModel):
    image_url: DataMessageContentUnionMember2ImageURL

    type: Literal["image_url"]


class DataMessageContentUnionMember3(BaseModel):
    refusal: str

    type: Literal["refusal"]


DataMessageContent: TypeAlias = Union[
    DataMessageContentUnionMember0,
    DataMessageContentUnionMember1,
    DataMessageContentUnionMember2,
    DataMessageContentUnionMember3,
]


class DataMessage(BaseModel):
    id: str
    """Deep Origin system ID."""

    role: Literal["user", "assistant"]

    content: Optional[List[DataMessageContent]] = None


class Data(BaseModel):
    messages: List[DataMessage]


class ListMessagesResponse(BaseModel):
    data: Data
