from typing import List, Dict

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
    StudyTimeByCourseResponse,
)
from services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/study_time_by_course/", response_model=List[StudyTimeByCourseResponse])
def get_study_time_by_course(
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user),
):
    try:
        dashboard_service = DashboardService(db)
        return dashboard_service.get_study_time_by_course(curr_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/streaks", response_model=Dict[str, List[bool]])
def get_streaks(
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user),
):
    try:
        dashboard_service = DashboardService(db)
        streaks = dashboard_service.get_study_streaks(curr_user.id)
        return {"streaks": streaks}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time-distribution")
def get_time_distribution(
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user),
):
    try:
        dashboard_service = DashboardService(db)
        data = dashboard_service.get_time_distribution(curr_user.id)
        return {"data": data}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
