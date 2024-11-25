from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    course_service = TermService(db)
    course = course_service.create_term(
        body.name, body.start_date, body.end_date, current_user.id
    )
    return course


@router.get("")
def list_terms(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    course_service = TermService(db)
    terms = course_service.list_terms(current_user.id)

    return terms


@router.get("/{course_id}")
def retrieve_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course_service = TermService(db)
    course = course_service.retrieve_course(course_id, current_user.id)

    return course


#
#
# @router.put("/{course_id}")
# @router.patch("/{course_id}")
# def update_course(
#     course_id: str,
#     body: CourseCreateUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     course_service = TermService(db)
#     course = course_service.update_course(course_id, body.name, current_user.id)
#     return course
#
#
# @router.delete("/{course_id}", status_code=204)
# def delete_task(
#     course_id: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     course_service = TermService(db)
#     course_service.delete_course(course_id, current_user.id)
#
#     return None
#
#
# @router.get("/{course_id}/assignments")
# def list_course_assignments(
#     course_id: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     assignment_service = AssignmentService(db)
#     assignments = assignment_service.list_assignments(current_user.id, course_id)
#
#     return assignments
#
