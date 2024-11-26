from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.exceptions import (
    NotFoundError,
    RepositoryError,
)
from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.study_session_schemas import (
    StudySessionResponse,
    StudySessionStart,
)
from services.study_session_service import StudySessionService

router = APIRouter()


@router.post("/start", response_model=StudySessionResponse, status_code=201)
def start_study_session(
    body: StudySessionStart,
    db: Session = Depends(get_db),
):
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
def current_study_session(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        study_session_service = StudySessionService(db)
        return study_session_service.retrieve_study_session(study_session_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/end", response_model=StudySessionResponse)
# def end_study_session(
#     study_session_id: uuid.UUID,
#     db: Session = Depends(get_db),
# ):
#     try:
#         study_session_service = StudySessionService(db)
#         return study_session_service.end_study_session(study_session_id)
#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except RepositoryError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     except (
#         PauseInactiveSessionError,
#         SessionAlreadyPausedError,
#         SessionAlreadyFinishedError,
#     ) as e:
#         raise HTTPException(status_code=409, detail=str(e))


# @router.delete("/{study_session_id}", status_code=204)
# def delete_study_session(
#     study_session_id: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     try:
#         study_session_service = StudySessionService(db)
#         study_session_service.delete_study_session(study_session_id)
#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except RepositoryError as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/list_sessions/", response_model=List[StudySessionResponse])
# def list_study_sessions(
#     db: Session = Depends(get_db), curr_user: User = Depends(get_current_user)
# ):
#     try:
#         study_session_service = StudySessionService(db)
#         return study_session_service.list_study_sessions(curr_user.id)
#     except RepositoryError as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/pause/{study_session_id}", response_model=StudySessionResponse)
# def pause_study_session(
#     study_session_id: uuid.UUID,
#     db: Session = Depends(get_db),
#     curr_user: User = Depends(get_current_user),
# ):
#     try:
#         study_session_service = StudySessionService(db)
#         return study_session_service.pause_study_session(study_session_id)
#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except RepositoryError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     except (PauseInactiveSessionError, SessionAlreadyPausedError) as e:
#         raise HTTPException(status_code=409, detail=str(e))


# @router.post("/unpause/{study_session_id}", response_model=StudySessionResponse)
# def unpause_study_session(
#     study_session_id: uuid.UUID,
#     db: Session = Depends(get_db),
#     curr_user: User = Depends(get_current_user),
# ):
#     try:
#         study_session_service = StudySessionService(db)
#         return study_session_service.unpause_study_session(study_session_id)
#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except RepositoryError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     except (PauseInactiveSessionError, SessionNotPausedError) as e:
#         raise HTTPException(status_code=409, detail=str(e))


# @router.get("/study_time_by_course/", response_model=List[StudyTimeByCourseResponse])
# def get_study_time_by_course(
#     db: Session = Depends(get_db),
#     curr_user: User = Depends(get_current_user),
# ):
#     try:
#         study_session_service = StudySessionService(db)

#         return study_session_service.get_study_time_by_discipline(curr_user.id)

#     except NotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except RepositoryError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
