from db.session import Base, engine
from models.assignment import Assignment  # noqa
from models.course import Course  # noqa
from models.study_plan import StudyPlan, StudyPlanTopic, StudySession  # noqa
from models.user import User  # noqa

# Cria todas as tabelas no banco de dados
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
