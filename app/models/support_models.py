from pydantic import BaseModel
from typing import Optional, Union

class CreateTicket(BaseModel):
    userId: Union[str, int]
    isssueDescrption: str
    timestamp: int