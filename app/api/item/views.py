from typing import List

from ...models.models import Item
from ...repositories.item_repository import ItemRepository
from fastapi import APIRouter, Depends, status, HTTPException

from .schemas import ItemSchema, GetItemSchema

router = APIRouter()


@router.post('/', response_model=ItemSchema,
             status_code=status.HTTP_201_CREATED)
def create(item: ItemSchema,
           repository: ItemRepository = Depends()):
    
    if item.value < 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Item value must be greater than R$ 1.00')
    
    return repository.create(Item(**item.dict()))


@router.get('/', response_model=List[ItemSchema])
def read(repository: ItemRepository = Depends()):
    return repository.get_all()


@router.get('/{id}', response_model=GetItemSchema)
def get_by_id(id: int, repository: ItemRepository = Depends()):
    return repository.get_by_id(id)


@router.put('/{id}', response_model=GetItemSchema)
def update(item: ItemSchema, id: int,
           repository: ItemRepository = Depends()):
    return repository.update(id, item.dict())


@router.delete('/{id}')
def delete(id: int, repository: ItemRepository = Depends()):
    return repository.delete(id)
