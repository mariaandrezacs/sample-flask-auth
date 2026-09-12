from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from ..container import get_container
from ..domain import Role, User
from ..dto import CreateUserInput, LoginInput, UpdatePasswordInput

api_bp = Blueprint("api", __name__)


def _get_services():
    return get_container()


def _to_entity(model):
    return User(
        id=model.id,
        username=model.username,
        password_hash=model.password,
        role=Role(model.role),
    )


def _to_model(user):
    from ..infrastructure.models import UserModel

    return UserModel.query.get(user.id)


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    dto = LoginInput(
        username=data.get("username", ""),
        password=data.get("password", ""),
    )
    user = _get_services().auth_service.authenticate(dto)
    login_user(_to_model(user))
    return jsonify({"message": "Autenticação realizada com sucesso"})


@api_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso."})


@api_bp.route("/user", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    dto = CreateUserInput(
        username=data.get("username", ""),
        password=data.get("password", ""),
        role=data.get("role", "user"),
    )
    output = _get_services().user_service.create_user(dto)
    return (
        jsonify({"id": output.id, "username": output.username, "role": output.role}),
        201,
    )


@api_bp.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    output = _get_services().user_service.get_user(id_user, _to_entity(current_user))
    return jsonify({"id": output.id, "username": output.username, "role": output.role})


@api_bp.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.get_json(silent=True) or {}
    dto = UpdatePasswordInput(password=data.get("password", ""))
    output = _get_services().user_service.update_password(
        id_user, dto, _to_entity(current_user)
    )
    return jsonify({"message": f"Usuario {output.id} atualizado com sucesso."})


@api_bp.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    _get_services().user_service.delete_user(id_user, _to_entity(current_user))
    return jsonify({"message": f"Usuario {id_user} deletado com sucesso."})


def register_blueprints(app):
    app.register_blueprint(api_bp)
