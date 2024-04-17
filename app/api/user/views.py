from typing import List

from ...models.models import User
from ...repositories.user_repository import UserRepository
from fastapi import APIRouter, Depends, status, HTTPException

from ..utils.token import encode_jwt, decode_jwt

from .schemas import UserSchema, GetUserSchema
import validate_cpf
import re

router = APIRouter()


@router.post('/', response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
def create(user: UserSchema,
           repository: UserRepository = Depends()):

    user.cpf = user.cpf.replace(".", "").replace("-", "")

    if not validate_cpf.is_valid(user.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CPF")

    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', user.password):
        print(user.password)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    
    return repository.create(User(**user.dict()))


@router.get('/', response_model=List[UserSchema])
def read(repository: UserRepository = Depends()):
    return repository.get_all()


@router.get('/{id}', response_model=UserSchema)
def get_by_id(id: str, repository: UserRepository = Depends()):
    return repository.get_by_id(id)


@router.put('/{cpf}', response_model=UserSchema, dependencies = [Depends(decode_jwt)])
def update(user: UserSchema, cpf: str,
           repository: UserRepository = Depends()):
    return repository.update(cpf, user.dict())


@router.delete('/{id}')
def delete(id: int, repository: UserRepository = Depends()):
    return repository.delete(id)

@router.get('login')
def login(username: str, password: str, repository: UserRepository = Depends()):
    user = repository.get_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.password != password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    encode_user = GetUserSchema(cpf=user.cpf, username=user.username, email=user.email)
    return encode_jwt(encode_user.dict())
