import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.exceptions import (
    NotFoundError,
    PauseInactiveSessionError,
    RepositoryError,
    SessionAlreadyFinishedError,
    SessionNotPausedError,
)
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current/{plan_id}", response_model=StudySessionResponse)
def current_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.retrieve_current_study_session_for_plan_id(plan_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/end/{plan_id}", response_model=StudySessionResponse)
def end_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.end_study_session(plan_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except SessionAlreadyFinishedError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/history/{plan_id}", response_model=List[StudySessionResponse])
def list_study_sessions(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.list_session_plan_history(plan_id)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pause/{plan_id}", response_model=StudySessionResponse)
def pause_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.pause_study_session(plan_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except PauseInactiveSessionError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/unpause/{plan_id}", response_model=StudySessionResponse)
def unpause_study_session(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.unpause_study_session(plan_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except (PauseInactiveSessionError, SessionNotPausedError) as e:
        raise HTTPException(status_code=409, detail=str(e))
