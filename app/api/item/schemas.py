from pydantic import BaseModel
from ..user.schemas import UserSchema
from ..group.schemas import GroupSchema


class ItemSchema(BaseModel):
    id: int
    name: str
    group_id: int
    owner_id: str
    value: int

    class Config:
        orm_mode = True
        
class GetItemSchema(BaseModel):
    id: int
    name: str
    group_id: int
    owner_id: str
    value: int
    owner: UserSchema
    group: GroupSchema

    class Config:
        orm_mode = True