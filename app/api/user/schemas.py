from pydantic import BaseModel


class UserSchema(BaseModel):
    cpf : str
    username : str
    email : str
    password : str
    role : str

    class Config:
        orm_mode = True
        
class GetUserSchema(BaseModel):
    cpf : str
    username : str
    email : str

    class Config:
        orm_mode = True