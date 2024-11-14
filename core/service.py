from core.repository import BaseRepository
from core.singleton import SingletonMeta


class BaseService(metaclass=SingletonMeta):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
