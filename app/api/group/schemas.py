from pydantic import BaseModel
from typing import List


class GroupSchema(BaseModel):
    id : int
    name : str
    description : str
    creator_id : str

    class Config:
        orm_mode = True