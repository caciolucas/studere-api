from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.course_schemas import CourseCreateUpdate, CourseResponse
from schemas.assignment_schemas import AssignmentResponse
from services.assignment_service import AssignmentService
from services.course_service import CourseService

router = APIRouter()


@router.post("", response_model=CourseResponse, status_code=201)
def create_course(
    body: CourseCreateUpdate,
    db: Session = Depends(get_db),
):
    try:
        course_service = CourseService(db)
        return course_service.create_course(body.name, body.term_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("", response_model=List[CourseResponse])
def list_courses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        course_service = CourseService(db)
        return course_service.list_courses(current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/{course_id}", response_model=CourseResponse)
def retrieve_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        course_service = CourseService(db)
        return course_service.retrieve_course(course_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.put("/{course_id}", response_model=CourseResponse, status_code=201)
def update_course(
    course_id: UUID,
    body: CourseCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        course_service = CourseService(db)
        return course_service.update_course(course_id, current_user.id, body.name)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.delete("/{course_id}", status_code=204)
def delete_task(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        course_service = CourseService(db)
        course_service.delete_course(course_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/{course_id}/assignments", response_model=List[AssignmentResponse])
def list_course_assignments(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        assignment_service = AssignmentService(db)
        return assignment_service.list_assignments(current_user.id, course_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e
