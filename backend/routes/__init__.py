from flask import jsonify


def error_response(message: str, code: str = "validation_error", status_code: int = 400):
    return jsonify({
        "error": {
            "code": code,
            "message": message,
        }
    }), status_code
