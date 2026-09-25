from flask import Blueprint, jsonify, request
from backend.models import FavoriteFruit, db, get_or_create_user
from backend.routes import error_response
from backend.services.seed_data import DEVIL_FRUITS

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api/users")
VALID_FRUIT_NAMES = {fruit["name"] for fruit in DEVIL_FRUITS}


@favorites_bp.route("/<user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    user = get_or_create_user(external_id=user_id)
    favorites = FavoriteFruit.query.filter_by(user_id=user.id).order_by(FavoriteFruit.created_at.asc()).all()
    return jsonify({
        "user_id": user_id,
        "favorites": [fav.fruit_name for fav in favorites],
    }), 200


@favorites_bp.route("/<user_id>/favorites", methods=["POST"])
def add_favorite(user_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    fruit_name = data.get("fruit_name")
    if not fruit_name or not isinstance(fruit_name, str):
        return error_response("Field 'fruit_name' is required and must be a string.", status_code=400)

    fruit_name = fruit_name.strip()
    if fruit_name not in VALID_FRUIT_NAMES:
        return error_response(f"Unknown Devil Fruit name: '{fruit_name}'.", code="unknown_fruit", status_code=422)

    user = get_or_create_user(external_id=user_id)

    existing = FavoriteFruit.query.filter_by(user_id=user.id, fruit_name=fruit_name).first()
    if existing:
        return error_response(
            f"'{fruit_name}' is already in favorites for user '{user_id}'.",
            code="duplicate_favorite",
            status_code=409,
        )

    new_fav = FavoriteFruit(user_id=user.id, fruit_name=fruit_name)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({
        "message": f"Added '{fruit_name}' to favorites.",
        "user_id": user_id,
        "fruit_name": fruit_name,
    }), 201


@favorites_bp.route("/<user_id>/favorites/<fruit_name>", methods=["DELETE"])
def remove_favorite(user_id, fruit_name):
    user = get_or_create_user(external_id=user_id)
    fav = FavoriteFruit.query.filter_by(user_id=user.id, fruit_name=fruit_name).first()

    if not fav:
        return error_response(
            f"Favorite '{fruit_name}' not found for user '{user_id}'.",
            code="not_found",
            status_code=404,
        )

    db.session.delete(fav)
    db.session.commit()

    return jsonify({
        "message": f"Removed '{fruit_name}' from favorites.",
        "user_id": user_id,
        "fruit_name": fruit_name,
    }), 200
