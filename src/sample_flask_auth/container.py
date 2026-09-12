from .infrastructure.repositories import SqlAlchemyUserRepository
from .infrastructure.security import BcryptPasswordHasher
from .services import AuthService, UserService


class Container:
    def __init__(self):
        self.user_repository = SqlAlchemyUserRepository()
        self.password_hasher = BcryptPasswordHasher()
        self.auth_service = AuthService(self.user_repository, self.password_hasher)
        self.user_service = UserService(self.user_repository, self.password_hasher)


_container = Container()


def get_container():
    return _container
