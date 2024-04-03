from ..db.db import Session, get_db
from ..models.models import Item
from fastapi import Depends

from .base_repository import BaseRepository


class ItemRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Item)
