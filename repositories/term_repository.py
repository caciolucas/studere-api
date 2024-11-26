from uuid import UUID
from typing import List

from core.exceptions import RepositoryError
from core.repository import BaseRepository
from models.term import Term


class TermRepository(BaseRepository):
    def create_term(self, term: Term) -> Term:
        try:
            self.db.add(term)
            self.db.commit()
            self.db.refresh(term)
            return term
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def retrieve_term(self, term_id: UUID) -> Term:
        try:
            return self.db.query(Term).filter(Term.id == term_id).first()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def update_term(self, term: Term) -> Term:
        try:
            self.db.merge(term)
            self.db.commit()
            self.db.refresh(term)
            return term
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def delete_term(self, term_id: UUID) -> None:
        try:
            term = self.db.query(Term).filter(Term.id == term_id).first()
            self.db.delete(term)
            self.db.commit()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def list_terms(self, user_id) -> List[Term]:
        try:
            if user_id:
                return self.db.query(Term).filter(Term.user_id == user_id).all()
            return self.db.query(Term).all()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e
