from flask import Flask, jsonify

from ..domain import ForbiddenException, NotFoundException, ValidationException


def register_error_handlers(app: Flask):
    @app.errorhandler(ValidationException)
    def handle_validation(exc):
        return jsonify({"message": str(exc)}), 400

    @app.errorhandler(ForbiddenException)
    def handle_forbidden(exc):
        return jsonify({"message": str(exc)}), 403

    @app.errorhandler(NotFoundException)
    def handle_not_found(exc):
        return jsonify({"message": str(exc)}), 404

    @app.errorhandler(Exception)
    def handle_generic(exc):
        return jsonify({"message": "Erro interno no servidor."}), 500
