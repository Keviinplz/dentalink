from typing import Generic, TypeVar, Union

from pydantic import BaseModel

ResponseModel = TypeVar("ResponseModel")


class DentalinkCursor(BaseModel):
    current: str
    next: Union[str, None] = None
    prev: Union[str, None] = None


class DentalinkDataCursor(BaseModel):
    rel: str
    href: str
    method: str


class DentalinkResponse(BaseModel, Generic[ResponseModel]):
    links: Union[DentalinkCursor, None] = None
    data: ResponseModel
