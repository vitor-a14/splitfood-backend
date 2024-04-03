from ..db.db import Session, get_db
from ..models.models import User
from fastapi import Depends

from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, User)

    def get_by_id(self, cpf: str):
        return self.session.query(self.model).filter_by(cpf=cpf).first()