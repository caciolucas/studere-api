from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import (
    assignment_router,
    course_router,
    study_session_router,
    study_plan_router,
    term_router,
    user_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(study_plan_router.router, prefix="/plans", tags=["Study Plans"])
app.include_router(
    assignment_router.router, prefix="/assignments", tags=["Assignments"]
)
app.include_router(course_router.router, prefix="/courses", tags=["Courses"])
app.include_router(study_session_router.router, prefix="/sessions", tags=["Sessions"])
app.include_router(term_router.router, prefix="/terms", tags=["Terms"])
