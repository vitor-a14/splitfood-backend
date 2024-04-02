from typing import List

from ...models.models import User
from ...repositories.user_repository import UserRepository
from fastapi import APIRouter, Depends, status, HTTPException

from .schemas import UserSchema
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


@router.get('/{id}', response_model=List[UserSchema])
def get_by_id(id: int, repository: UserRepository = Depends()):
    return repository.get_by_id(int)


@router.put('/{id}', response_model=UserSchema)
def update(user: UserSchema, id: int,
           repository: UserRepository = Depends()):
    return repository.update(id, user.dict())


@router.delete('/{id}')
def delete(id: int, repository: UserRepository = Depends()):
    return repository.delete(id)
