from flask import Blueprint, jsonify, request
from backend.routes import error_response
from backend.services.calculations import calculate_catch_up
from backend.services.seed_data import (
    ARC_DATA,
    CHARACTERS,
    CREW_MEMBERS,
    DEVIL_FRUITS,
    DEVIL_FRUIT_AWAKENINGS,
    DEVIL_FRUIT_DETAILS,
    DEVIL_FRUIT_TYPE_GUIDE,
    FACTION_UNITS,
)

catalog_bp = Blueprint("catalog", __name__, url_prefix="/api")


@catalog_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "grand-line-navigator-api"
    }), 200


@catalog_bp.route("/arcs", methods=["GET"])
def get_arcs():
    return jsonify(ARC_DATA), 200


@catalog_bp.route("/characters", methods=["GET"])
def get_characters():
    return jsonify(CHARACTERS), 200


@catalog_bp.route("/devil-fruits", methods=["GET"])
def get_devil_fruits():
    return jsonify(DEVIL_FRUITS), 200


@catalog_bp.route("/devil-fruit-types", methods=["GET"])
def get_devil_fruit_types():
    return jsonify({
        "types": DEVIL_FRUIT_TYPE_GUIDE,
        "awakenings": DEVIL_FRUIT_AWAKENINGS,
        "details": DEVIL_FRUIT_DETAILS,
    }), 200


@catalog_bp.route("/crew-members", methods=["GET"])
def get_crew_members():
    return jsonify(CREW_MEMBERS), 200


@catalog_bp.route("/factions", methods=["GET"])
def get_factions():
    return jsonify(FACTION_UNITS), 200


@catalog_bp.route("/catch-up/calculate", methods=["POST"])
def catch_up_calculate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    if "current_episode" not in data or "episodes_per_day" not in data:
        return error_response("Both 'current_episode' and 'episodes_per_day' are required.", status_code=400)

    try:
        current_episode = int(data["current_episode"])
        episodes_per_day = int(data["episodes_per_day"])
    except (TypeError, ValueError):
        return error_response("Episode values must be valid integers.", status_code=400)

    try:
        result = calculate_catch_up(current_episode, episodes_per_day)
        return jsonify(result), 200
    except ValueError as e:
        return error_response(str(e), status_code=422)
