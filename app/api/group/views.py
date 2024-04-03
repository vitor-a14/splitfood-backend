from typing import List

from ...models.models import Group
from ...repositories.group_repository import GroupRepository
from ...repositories.user_repository import UserRepository
from fastapi import APIRouter, Depends, status, HTTPException

from .schemas import GroupSchema
from ..user.schemas import UserSchema

router = APIRouter()


@router.post('/', response_model=GroupSchema,
             status_code=status.HTTP_201_CREATED)
def create(group: GroupSchema,
           repository: GroupRepository = Depends(),
           userRepository: UserRepository = Depends()):
    
    user = userRepository.get_by_id(group.creator_id)
    if user == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CPF")
    
    currentGroupsForCreator = repository.get_by_creator_id(group.creator_id)
    
    if currentGroupsForCreator != None:
        if has_active_group(currentGroupsForCreator):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has an active group")
    
    return repository.create(Group(**group.dict()))


def has_active_group(groups):
    for group in groups:
        if group.status == 'active':
            return True
    return False

@router.get('/', response_model=List[GroupSchema])
def read(repository: GroupRepository = Depends()):
    return repository.get_all()


@router.get('/{id}', response_model=GroupSchema)
def get_by_id(id: int, repository: GroupRepository = Depends()):
    return repository.get_by_id(id)


@router.put('/{id}', response_model=GroupSchema)
def update(Group: GroupSchema, id: int,
           repository: GroupRepository = Depends()):
    return repository.update(id, Group.dict())

@router.put('/{id}/addParticipant', response_model=UserSchema)
def addParticipant(userId: str, id: int,
           repository: GroupRepository = Depends(),
           userRepository: UserRepository = Depends()):
    
    user = userRepository.get_by_id(userId)
    if user == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CPF")
    
    group = repository.get_by_id(id)
    if group == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Group ID")

    group.participants.append(user)
    
    return repository.create(group)

@router.put('/{id}/deactivate', response_model=GroupSchema)
def deactivateGroup(id: int,
           repository: GroupRepository = Depends()):
    
    group = repository.get_by_id(id)
    
    if group == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Group ID")
    
    group.status = 'inactive'
    
    return repository.create(group)

@router.delete('/{id}')
def delete(id: int, repository: GroupRepository = Depends()):
    return repository.delete(id)
