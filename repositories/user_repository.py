from uuid import UUID

from core.exceptions import RepositoryError
from core.repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
    def create_user(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def get_user_by_email(self, email: str) -> User:
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def get_user_by_id(self, id: UUID) -> User:
        try:
            return self.db.query(User).filter(User.id == id).first()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e
