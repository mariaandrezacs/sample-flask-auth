from typing import Optional

from ..domain import Role, User, UserRepository
from .database import db
from .models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def add(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            password=user.password_hash,
            role=user.role.value,
        )
        db.session.add(model)
        db.session.commit()
        return self._to_entity(model)

    def get(self, id_user: int) -> Optional[User]:
        model = UserModel.query.get(id_user)
        return self._to_entity(model) if model else None

    def get_by_username(self, username: str) -> Optional[User]:
        model = UserModel.query.filter_by(username=username).first()
        return self._to_entity(model) if model else None

    def update(self, user: User) -> Optional[User]:
        model = UserModel.query.get(user.id)
        if not model:
            return None
        model.password = user.password_hash
        model.role = user.role.value
        db.session.commit()
        return self._to_entity(model)

    def delete(self, id_user: int) -> None:
        model = UserModel.query.get(id_user)
        if model:
            db.session.delete(model)
            db.session.commit()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            password_hash=model.password,
            role=Role(model.role),
        )
