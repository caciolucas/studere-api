import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.session import get_db
from models.user import User
from schemas.study_plan_schemas import (
    StudyPlanAIGenerate,
    StudyPlanCreateUpdate,
    StudyPlanResponse,
)
from services.study_plan_service import StudyPlanService

router = APIRouter()


@router.post("/", response_model=StudyPlanResponse, status_code=201)
def create_study_plan(
    body: StudyPlanCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        study_plan_service = StudyPlanService(db)
        return study_plan_service.create_study_plan(
            title=body.title,
            course_id=body.course_id,
            topics=body.topics,
            current_user_id=current_user.id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/{study_plan_id}", response_model=StudyPlanResponse)
def get_study_plan(
    study_plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        study_plan_service = StudyPlanService(db)
        return study_plan_service.retrieve_study_plan(study_plan_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.get("/", response_model=List[StudyPlanResponse], status_code=201)
def list_study_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        study_plan_service = StudyPlanService(db)
        return study_plan_service.list_study_plans(
            user_id=current_user.id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.delete("/{study_plan_id}", status_code=204)
def delete_study_plan(
    study_plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        study_plan_service = StudyPlanService(db)
        study_plan_service.delete_study_plan(study_plan_id, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.post("/ai-generate", response_model=StudyPlanResponse, status_code=201)
def generate_study_plan(
    body: StudyPlanAIGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        study_plan_service = StudyPlanService(db)
        return study_plan_service.ai_generate_study_plan(
            body.prompt, body.course_id, current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e
