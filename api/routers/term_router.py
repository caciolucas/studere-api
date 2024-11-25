from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.term_schemas import TermResponse, TermCreateUpdate
from services.term_service import TermService

router = APIRouter()


@router.post("", response_model=TermResponse, status_code=201)
def create_term(
    body: TermCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = TermService(db)
    term = term_service.create_term(
        body.name, body.start_date, body.end_date, current_user.id
    )
    return term


@router.get("")
def list_terms(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    term_service = TermService(db)
    terms = term_service.list_terms(current_user.id)

    return terms


@router.get("/{term_id}")
def retrieve_term(
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = TermService(db)
    term = term_service.retrieve_term(term_id, current_user.id)

    return term


@router.get("/{term_id}/courses")
def list_term_courses(
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = TermService(db)
    term = term_service.list_term_courses(term_id, current_user.id)

    return term


@router.put("/{term_id}")
def update_term(
    term_id: UUID,
    body: TermCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = TermService(db)
    term = term_service.update_term(
        term_id, current_user.id, body.name, body.start_date, body.end_date
    )
    return term


@router.delete("/{term_id}", status_code=204)
def delete_term(
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = TermService(db)
    term_service.delete_term(term_id, current_user.id)

    return None
