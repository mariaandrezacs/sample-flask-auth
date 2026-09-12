from typing import Protocol

from .domain import (
    ForbiddenException,
    NotFoundException,
    Role,
    User,
    UserRepository,
    ValidationException,
)
from .dto import CreateUserInput, LoginInput, UpdatePasswordInput, UserOutput


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        raise NotImplementedError

    def verify(self, password: str, hash: str) -> bool:
        raise NotImplementedError


class UserService:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self.repository = repository
        self.hasher = hasher

    def create_user(self, dto: CreateUserInput) -> UserOutput:
        if self.repository.get_by_username(dto.username):
            raise ValidationException("Username already exists")

        try:
            role = Role(dto.role)
        except ValueError:
            raise ValidationException("Invalid role")

        user = User(
            username=dto.username,
            password_hash=self.hasher.hash(dto.password),
            role=role,
        )
        created = self.repository.add(user)
        return _to_output(created)

    def get_user(self, id_user: int, requester: User) -> UserOutput:
        user = self.repository.get(id_user)
        if not user:
            raise NotFoundException("User not found")
        return _to_output(user)

    def update_password(
        self, id_user: int, dto: UpdatePasswordInput, requester: User
    ) -> UserOutput:
        if not requester.can_update_password(id_user):
            raise ForbiddenException("Operation not allowed")

        user = self.repository.get(id_user)
        if not user:
            raise NotFoundException("User not found")

        user.password_hash = self.hasher.hash(dto.password)
        updated = self.repository.update(user)
        if not updated:
            raise NotFoundException("User not found")
        return _to_output(updated)

    def delete_user(self, id_user: int, requester: User) -> None:
        if not requester.can_delete(id_user):
            raise ForbiddenException("Operation not allowed")

        user = self.repository.get(id_user)
        if not user:
            raise NotFoundException("User not found")

        self.repository.delete(id_user)


class AuthService:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self.repository = repository
        self.hasher = hasher

    def authenticate(self, dto: LoginInput) -> User:
        user = self.repository.get_by_username(dto.username)
        if not user or not self.hasher.verify(dto.password, user.password_hash):
            raise ValidationException("Invalid credentials")
        return user


def _to_output(user: User) -> UserOutput:
    return UserOutput(id=user.id, username=user.username, role=user.role.value)
