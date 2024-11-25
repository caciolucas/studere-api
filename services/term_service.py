from fastapi import HTTPException
from sqlalchemy.orm import Session

from datetime import date
from core.service import BaseService
from typing import Optional
from models.term import Term
from repositories.term_repository import TermRepository
from services.user_service import UserService


class TermService(BaseService):
    def __init__(self, db: Session):
        self.repository = TermRepository(db)
        self.user_service = UserService(db)

    def create_term(self, name: str, start_date: date, end_date: date, user_id: str):
        user = self.user_service.retrieve_user(user_id)
        term = Term(
            name=name, start_date=start_date, end_date=end_date, user_id=user.id
        )

        return self.repository.create_term(term)

    def list_terms(self, user_id: Optional[str] = None):
        return self.repository.list_terms(user_id)

    def retrieve_term(self, term_id: str, current_user_id: str):
        term = self.repository.retrieve_term(term_id)
        if term is None:
            raise HTTPException(status_code=404, detail="Term not found")
        if str(term.user_id) != current_user_id:
            raise HTTPException(status_code=404, detail="Term not found")

        return term

    def update_term(
        self,
        term_id: str,
        current_user_id: str,
        name: Optional[str] = None,
    ):
        term = self.retrieve_term(term_id, current_user_id)
        if name:
            term.name = name

        return self.repository.update_term(term)

    def delete_term(self, term_id: str, current_user_id: str):
        term = self.retrieve_term(term_id, current_user_id)
        return self.repository.delete_term(term.id)
