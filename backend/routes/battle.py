from flask import Blueprint, jsonify, request
from backend.models import BattleResult, db, get_or_create_user
from backend.routes import error_response
from backend.services.calculations import simulate_battle

battle_bp = Blueprint("battle", __name__, url_prefix="/api")


@battle_bp.route("/battles/simulate", methods=["POST"])
def simulate_battle_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    pirate_units = data.get("pirate_units", [])
    marine_units = data.get("marine_units", [])
    user_id = data.get("user_id", "local-user")

    if not isinstance(pirate_units, list) or not isinstance(marine_units, list):
        return error_response("Both 'pirate_units' and 'marine_units' must be lists.", status_code=400)

    try:
        outcome = simulate_battle(pirate_units, marine_units)
    except ValueError as e:
        return error_response(str(e), code="unknown_unit", status_code=422)

    user = get_or_create_user(external_id=user_id)

    battle = BattleResult(
        user_id=user.id,
        pirate_units=pirate_units,
        marine_units=marine_units,
        pirate_score=outcome["pirate_score"],
        marine_score=outcome["marine_score"],
        winner=outcome["winner"],
    )
    db.session.add(battle)
    db.session.commit()

    return jsonify({
        "id": battle.id,
        "pirate_score": outcome["pirate_score"],
        "marine_score": outcome["marine_score"],
        "winner": outcome["winner"],
        "created_at": battle.created_at.isoformat(),
    }), 201


@battle_bp.route("/users/<user_id>/battles", methods=["GET"])
def get_user_battles(user_id):
    try:
        limit = int(request.args.get("limit", 10))
        if limit < 1:
            limit = 10
    except (TypeError, ValueError):
        limit = 10

    user = get_or_create_user(external_id=user_id)
    battles = (
        BattleResult.query.filter_by(user_id=user.id)
        .order_by(BattleResult.created_at.desc())
        .limit(limit)
        .all()
    )

    return jsonify({
        "user_id": user_id,
        "battles": [b.to_dict() for b in battles],
    }), 200
