from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.course_schemas import CourseCreateUpdate, CourseResponse
from services.assignment_service import AssignmentService
from services.course_service import CourseService

router = APIRouter()


@router.post("", response_model=CourseResponse, status_code=201)
def create_course(
    body: CourseCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course_service = CourseService(db)
    course = course_service.create_course(body.name, current_user.id)
    return course


@router.get("")
def list_courses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    course_service = CourseService(db)
    courses = course_service.list_courses(current_user.id)

    return courses


@router.get("/{course_id}")
def retrieve_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course_service = CourseService(db)
    course = course_service.retrieve_course(course_id, current_user.id)

    return course


@router.put("/{course_id}")
@router.patch("/{course_id}")
def update_course(
    course_id: str,
    body: CourseCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course_service = CourseService(db)
    course = course_service.update_course(course_id, body.name, current_user.id)
    return course


@router.delete("/{course_id}", status_code=204)
def delete_task(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course_service = CourseService(db)
    course_service.delete_course(course_id, current_user.id)

    return None


@router.get("/{course_id}/assignments")
def list_course_assignments(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment_service = AssignmentService(db)
    assignments = assignment_service.list_assignments(current_user.id, course_id)

    return assignments
