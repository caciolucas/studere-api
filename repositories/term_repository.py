from uuid import UUID

from core.repository import BaseRepository
from models.term import Term


class TermRepository(BaseRepository):
    def create_term(self, term: Term) -> Term:
        self.db.add(term)
        self.db.commit()
        self.db.refresh(term)
        return term

    def retrieve_term(self, term_id: UUID) -> Term:
        return self.db.query(Term).filter(Term.id == term_id).first()

    def update_term(self, term: Term) -> Term:
        self.db.merge(term)
        self.db.commit()
        self.db.refresh(term)
        return term

    def delete_term(self, term_id: UUID) -> None:
        term = self.db.query(Term).filter(Term.id == term_id).first()
        if term:
            self.db.delete(term)
            self.db.commit()

    def list_terms(self, user_id) -> list[Term]:
        if user_id:
            return self.db.query(Term).filter(Term.user_id == user_id).all()
        return self.db.query(Term).all()
