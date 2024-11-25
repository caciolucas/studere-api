from fastapi import FastAPI

from api.routers import (
    assignment_router,
    course_router,
    study_session_router,
    studyplan_router,
    term_router,
    user_router,
)

app = FastAPI()

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(studyplan_router.router, prefix="/study-plans", tags=["Study Plans"])
app.include_router(
    assignment_router.router, prefix="/assignments", tags=["Assignments"]
)
app.include_router(course_router.router, prefix="/courses", tags=["Courses"])
app.include_router(study_session_router.router, prefix="/sessions", tags=["Sessions"])
app.include_router(term_router.router, prefix="/terms", tags=["Terms"])
