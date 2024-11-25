from uuid import UUID

from core.repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, id: UUID) -> User:
        return self.db.query(User).filter(User.id == id).first()
