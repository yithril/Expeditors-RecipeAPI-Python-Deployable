from flask import jsonify
from werkzeug.exceptions import BadRequest, HTTPException

from app.schemas.errors import build_api_error


def register_error_handlers(app):
    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        if error.description and "Failed to decode JSON" in error.description:
            return jsonify(build_api_error(400, "Malformed JSON request body", [])), 400
        return jsonify(build_api_error(400, error.description or "Bad request", [])), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        if error.description and "Invalid value for parameter" in error.description:
            return jsonify(build_api_error(400, error.description, [])), 400
        return "", 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        if error.code == 404:
            return "", 404
        return jsonify(build_api_error(error.code, error.description, [])), error.code
