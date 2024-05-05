from typing import Union, Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")

class StatusResponse(GenericModel, Generic[DataT]):
    success: bool
    message: Optional[str] = None
    data: Optional[DataT] = None
