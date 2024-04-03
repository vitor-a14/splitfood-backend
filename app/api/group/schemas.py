from pydantic import BaseModel
from enum import Enum


class GroupStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class GroupSchema(BaseModel):
    id : int
    name : str
    description : str
    creator_id : str
    status : GroupStatus

    class Config:
        orm_mode = True