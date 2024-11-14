import uuid

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
    study_plan_service = StudyPlanService(db)
    study_plan = study_plan_service.create_study_plan(
        title=body.title,
        course_id=body.course_id,
        topics=body.topics,
        current_user_id=current_user.id,
    )
    return study_plan


@router.get("/{study_plan_id}", response_model=StudyPlanResponse)
def get_study_plan(
    study_plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_plan_service = StudyPlanService(db)
    study_plan = study_plan_service.retrieve_study_plan(study_plan_id, current_user.id)
    if not study_plan:
        raise HTTPException(status_code=404, detail="Study Plan not found")
    return study_plan


@router.put("/{study_plan_id}", response_model=StudyPlanResponse)
def update_study_plan(
    study_plan_id: uuid.UUID,
    body: StudyPlanCreateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_plan_service = StudyPlanService(db)
    study_plan = study_plan_service.update_study_plan(
        study_plan_id=study_plan_id,
        title=body.title,
        course_id=body.course_id,
        topics=body.topics,
    )
    if not study_plan:
        raise HTTPException(status_code=404, detail="Study Plan not found")
    return study_plan


@router.delete("/{study_plan_id}", status_code=204)
def delete_study_plan(
    study_plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_plan_service = StudyPlanService(db)
    if not study_plan_service.delete_study_plan(study_plan_id):
        raise HTTPException(status_code=404, detail="Study Plan not found")


@router.post("/ai-generate", response_model=StudyPlanResponse, status_code=201)
def generate_study_plan(
    body: StudyPlanAIGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_plan_service = StudyPlanService(db)
    response = study_plan_service.ai_generate_study_plan(
        body.prompt, body.course_id, current_user.id
    )

    return response
