from ..db.db import Session, get_db
from ..models.models import Group
from fastapi import Depends

from .base_repository import BaseRepository


class GroupRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Group)
        
    def get_by_creator_id(self, creator_id: str):
        return self.session.query(Group).filter(Group.creator_id == creator_id).all()
