from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.term_schemas import TermCreateUpdate, TermResponse
from schemas.course_schemas import CourseResponse
from services.term_service import TermService

router = APIRouter()


@router.post("", response_model=TermResponse, status_code=201)
def create_term(
    body: TermCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        term_service = TermService(db)
        term = term_service.create_term(
            body.name, body.start_date, body.end_date, current_user.id
        )
        return term
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("", response_model=List[TermResponse])
def list_terms(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        term_service = TermService(db)
        return term_service.list_terms(current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/{term_id}", response_model=TermResponse)
def retrieve_term(
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        term_service = TermService(db)
        return term_service.retrieve_term(term_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/{term_id}/courses", response_model=List[CourseResponse])
def list_term_courses(
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        term_service = TermService(db)
        return term_service.list_term_courses(term_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.put("/{term_id}", response_model=TermResponse, status_code=201)
def update_term(
    term_id: UUID,
    body: TermCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        term_service = TermService(db)
        return term_service.update_term(
            term_id, current_user.id, body.name, body.start_date, body.end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.delete("/{term_id}", status_code=204)
def delete_term(
    term_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        term_service = TermService(db)
        term_service.delete_term(term_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e
