import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.study_session_schemas import StudySessionCreateUpdate, StudySessionResponse

from services.study_session_service import StudySessionService

router = APIRouter()


@router.post("/", response_model=StudySessionResponse, status_code=201)
def create_study_plan(
    body: StudySessionCreateUpdate,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)
):
    study_session_service = StudySessionService(db)
    study_session = study_session_service.create_study_session(
        title=body.title,
        plan_id=body.plan_id,
        topics=body.topics,
        description=body.description,
        notes=body.notes,
        started_at=body.started_at,
        ended_at=body.ended_at,
        total_pause_time=body.total_pause_time
    )
    return study_session


@router.get("/{study_session_id}", response_model=StudySessionResponse)
def get_study_session(
        study_session_id: uuid.UUID,
        db: Session = Depends(get_db),
        curr_user: User = Depends(get_current_user)
):
    study_session_service = StudySessionService(db)
    study_session = study_session_service.get_study_session(study_session_id)

    if not study_session:
        raise HTTPException(status_code=404, detail="Study session not found.")
    return study_session


@router.get("/list_sessions", response_model=List[StudySessionResponse])
def list_study_sessions(
        self,
        db: Session = Depends(get_db),
        curr_user: User = Depends(get_current_user)
):
    study_session_service = StudySessionService(db)
    return study_session_service.list_study_sessions(curr_user.id)
