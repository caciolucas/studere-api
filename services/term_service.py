from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from core.service import BaseService
from models.term import Term
from repositories.term_repository import TermRepository
from services.user_service import UserService


class TermService(BaseService):
    def __init__(self, db: Session):
        self.repository = TermRepository(db)
        self.user_service = UserService(db)

    def create_term(self, name: str, start_date: date, end_date: date, user_id: UUID):
        user = self.user_service.retrieve_user(user_id)
        term = Term(
            name=name, start_date=start_date, end_date=end_date, user_id=user.id
        )
        return self.repository.create_term(term)

    def list_terms(self, user_id: Optional[UUID] = None):
        return self.repository.list_terms(user_id)

    def retrieve_term(self, term_id: UUID, current_user_id: UUID):
        term = self.repository.retrieve_term(term_id)
        if term is None or term.user_id != current_user_id:
            raise NotFoundError(
                f"Term not found: {term_id} (user: {current_user_id})"
            )
        return term

    def update_term(
        self,
        term_id: UUID,
        current_user_id: UUID,
        name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        term = self.retrieve_term(term_id, current_user_id)

        if name:
            term.name = name
        if start_date:
            term.start_date = start_date
        if end_date:
            term.end_date = end_date

        return self.repository.update_term(term)

    def delete_term(self, term_id: UUID, current_user_id: UUID):
        self.retrieve_term(term_id, current_user_id)
        return self.repository.delete_term(term_id)

    def list_term_courses(self, term_id: UUID, current_user_id: UUID):
        term = self.retrieve_term(term_id, current_user_id)
        return term.courses
