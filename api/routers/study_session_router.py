import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.study_session_schemas import (
    StudySessionResponse,
    StudySessionStart,
)
from services.study_session_service import StudySessionService

router = APIRouter()


@router.post("/start", response_model=StudySessionResponse, status_code=201)
def start_study_session(body: StudySessionStart, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.start_study_session(
            title=body.title,
            plan_id=body.plan_id,
            description=body.description,
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/current/{plan_id}", response_model=StudySessionResponse)
def current_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.retrieve_current_study_session_for_plan_id(plan_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.post("/end/{plan_id}", response_model=StudySessionResponse)
def end_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.end_study_session(plan_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/history/{plan_id}", response_model=List[StudySessionResponse])
def list_study_sessions(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.list_session_plan_history(plan_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.post("/pause/{plan_id}", response_model=StudySessionResponse)
def pause_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.pause_study_session(plan_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.post("/unpause/{plan_id}", response_model=StudySessionResponse)
def unpause_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.unpause_study_session(plan_id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e
