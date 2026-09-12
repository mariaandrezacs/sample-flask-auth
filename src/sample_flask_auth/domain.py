from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class DomainException(Exception):
    pass


class ValidationException(DomainException):
    pass


class ForbiddenException(DomainException):
    pass


class NotFoundException(DomainException):
    pass


@dataclass
class User:
    username: str
    password_hash: str
    role: Role = Role.USER
    id: Optional[int] = None

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    def can_update_password(self, target_id: int) -> bool:
        return self.is_admin or self.id == target_id

    def can_delete(self, target_id: int) -> bool:
        return self.is_admin and self.id != target_id


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get(self, id_user: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id_user: int) -> None:
        raise NotImplementedError
