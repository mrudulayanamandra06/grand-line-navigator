from flask import Blueprint, jsonify, request
from backend.models import ClaimedReward, db, get_or_create_user
from backend.routes import error_response
from backend.services.calculations import calculate_bounty_milestones
from backend.services.seed_data import BOUNTY_REWARDS

bounty_bp = Blueprint("bounty", __name__, url_prefix="/api")
VALID_ACHIEVEMENTS_MAP = {item["achievement"]: item["reward"] for item in BOUNTY_REWARDS}


@bounty_bp.route("/bounty/rewards", methods=["GET"])
def get_bounty_rewards():
    return jsonify(BOUNTY_REWARDS), 200


@bounty_bp.route("/bounty/calculate", methods=["POST"])
def calculate_bounty():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    selected_achievements = data.get("selected_achievements", [])
    if not isinstance(selected_achievements, list):
        return error_response("Field 'selected_achievements' must be a list of strings.", status_code=400)

    try:
        result = calculate_bounty_milestones(selected_achievements)
        return jsonify(result), 200
    except ValueError as e:
        return error_response(str(e), status_code=422)


@bounty_bp.route("/users/<user_id>/rewards", methods=["GET"])
def get_user_rewards(user_id):
    user = get_or_create_user(external_id=user_id)
    claimed = ClaimedReward.query.filter_by(user_id=user.id).all()
    return jsonify({
        "user_id": user_id,
        "claimed_rewards": [cr.achievement for cr in claimed],
    }), 200


@bounty_bp.route("/users/<user_id>/rewards/claim", methods=["POST"])
def claim_rewards(user_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    achievements = data.get("achievements", [])
    if not isinstance(achievements, list):
        return error_response("Field 'achievements' must be a list of achievement strings.", status_code=400)

    # Server-side validation: Reject unknown achievements
    for ach in achievements:
        if ach not in VALID_ACHIEVEMENTS_MAP:
            return error_response(f"Unknown achievement: '{ach}'.", code="unknown_achievement", status_code=422)

    user = get_or_create_user(external_id=user_id)

    existing_claimed = {
        cr.achievement for cr in ClaimedReward.query.filter_by(user_id=user.id).all()
    }

    newly_claimed = []
    for ach in achievements:
        if ach not in existing_claimed:
            reward_val = VALID_ACHIEVEMENTS_MAP[ach]
            new_record = ClaimedReward(user_id=user.id, achievement=ach, reward=reward_val)
            db.session.add(new_record)
            newly_claimed.append(ach)

    if newly_claimed:
        db.session.commit()

    all_claimed = [
        cr.achievement for cr in ClaimedReward.query.filter_by(user_id=user.id).all()
    ]

    return jsonify({
        "user_id": user_id,
        "claimed_rewards": all_claimed,
        "newly_claimed_count": len(newly_claimed),
    }), 200


@bounty_bp.route("/users/<user_id>/rewards", methods=["DELETE"])
def reset_user_rewards(user_id):
    user = get_or_create_user(external_id=user_id)
    ClaimedReward.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    return jsonify({
        "message": "Claimed milestones successfully reset.",
        "user_id": user_id,
        "claimed_rewards": [],
    }), 200
