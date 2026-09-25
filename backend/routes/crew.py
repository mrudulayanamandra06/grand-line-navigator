from flask import Blueprint, jsonify, request
from backend.models import SavedCrew, db, get_or_create_user
from backend.routes import error_response
from backend.services.calculations import calculate_readiness
from backend.services.seed_data import CREW_MEMBERS

crew_bp = Blueprint("crew", __name__, url_prefix="/api/users")
VALID_MEMBER_NAMES = set(CREW_MEMBERS.keys())


@crew_bp.route("/<user_id>/crew", methods=["GET"])
def get_crew(user_id):
    user = get_or_create_user(external_id=user_id)
    saved = SavedCrew.query.filter_by(user_id=user.id).first()

    if not saved:
        return jsonify({
            "user_id": user_id,
            "crew": None,
        }), 200

    return jsonify({
        "user_id": user_id,
        "crew": saved.to_dict(),
    }), 200


@crew_bp.route("/<user_id>/crew", methods=["PUT"])
def save_crew(user_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    crew_name = str(data.get("crew_name", "The Grand Line Crew")).strip() or "The Grand Line Crew"
    captain = data.get("captain")
    members = data.get("members", [])
    member_stats = data.get("member_stats", {})

    # Validation: Captain
    if not captain or captain not in VALID_MEMBER_NAMES:
        return error_response(f"Unknown or missing captain: '{captain}'.", code="invalid_captain", status_code=422)

    # Validation: Members list
    if not isinstance(members, list):
        return error_response("Field 'members' must be a list of member names.", status_code=400)

    if len(members) > 9:
        return error_response("A crew cannot have more than 9 non-captain members.", code="too_many_members", status_code=422)

    # Check for duplicate members
    if len(members) != len(set(members)):
        return error_response("Crew members list cannot contain duplicates.", code="duplicate_members", status_code=422)

    # Check captain not in members
    if captain in members:
        return error_response(f"Captain '{captain}' cannot also be listed as an additional crew member.", code="captain_in_members", status_code=422)

    # Check unknown members
    for m in members:
        if m not in VALID_MEMBER_NAMES:
            return error_response(f"Unknown crew member: '{m}'.", code="unknown_member", status_code=422)

    # Validation: Member stats
    if not isinstance(member_stats, dict):
        return error_response("Field 'member_stats' must be a dictionary.", status_code=400)

    for member_name, stats in member_stats.items():
        if member_name not in VALID_MEMBER_NAMES:
            return error_response(f"Stats provided for unknown member: '{member_name}'.", code="unknown_stat_member", status_code=422)
        if not isinstance(stats, dict):
            return error_response(f"Stats for '{member_name}' must be an object with stat keys.", status_code=400)
        for stat_key in ["power", "defense", "speed", "loyalty"]:
            val = stats.get(stat_key, 70)
            if not isinstance(val, int) or val < 0 or val > 100:
                return error_response(
                    f"Stat '{stat_key}' for member '{member_name}' must be an integer between 0 and 100.",
                    code="invalid_stat_value",
                    status_code=422,
                )

    user = get_or_create_user(external_id=user_id)
    saved = SavedCrew.query.filter_by(user_id=user.id).first()

    if not saved:
        saved = SavedCrew(
            user_id=user.id,
            crew_name=crew_name,
            captain=captain,
            members=members,
            member_stats=member_stats,
        )
        db.session.add(saved)
    else:
        saved.crew_name = crew_name
        saved.captain = captain
        saved.members = members
        saved.member_stats = member_stats

    db.session.commit()

    return jsonify({
        "message": "Crew configuration saved successfully.",
        "crew": saved.to_dict(),
    }), 200


@crew_bp.route("/<user_id>/crew", methods=["DELETE"])
def delete_crew(user_id):
    user = get_or_create_user(external_id=user_id)
    SavedCrew.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    return jsonify({
        "message": "Saved crew deleted successfully.",
        "user_id": user_id,
    }), 200
