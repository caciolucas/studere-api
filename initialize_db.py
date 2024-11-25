from db.session import Base, engine
from models.assignment import Assignment  # noqa
from models.course import Course  # noqa
from models.study_plan import StudyPlan, StudyPlanTopic  # noqa
from models.study_session import StudySession
from models.user import User  # noqa
from models.term import Term  # noqa
from models.study_session import StudySession, study_session_topics  # noqa


# Cria todas as tabelas no banco de dados
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
