from flask import Blueprint, jsonify, request
from backend.models import QuizAttempt, db, get_or_create_user
from backend.routes import error_response
from backend.services.calculations import evaluate_quiz
from backend.services.seed_data import QUIZ_QUESTIONS

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/quiz")


@quiz_bp.route("/questions", methods=["GET"])
def get_quiz_questions():
    """Return quiz questions without exposing the correct answers."""
    sanitized = [
        {
            "id": q.get("id", idx),
            "question": q["question"],
            "options": q["options"],
        }
        for idx, q in enumerate(QUIZ_QUESTIONS, start=1)
    ]
    return jsonify(sanitized), 200


@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("Invalid JSON payload; object expected.", status_code=400)

    player_name = str(data.get("player_name", "Anonymous Captain")).strip() or "Anonymous Captain"
    user_id = data.get("user_id", "local-user")
    answers = data.get("answers")

    if not isinstance(answers, dict):
        return error_response("Field 'answers' must be an object mapping question numbers to answers.", status_code=400)

    try:
        evaluation = evaluate_quiz(answers)
    except ValueError as e:
        return error_response(str(e), status_code=422)

    user = get_or_create_user(external_id=user_id)

    attempt = QuizAttempt(
        user_id=user.id,
        player_name=player_name,
        score=evaluation["score"],
        total_questions=evaluation["total"],
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        "id": attempt.id,
        "player_name": player_name,
        "score": evaluation["score"],
        "total": evaluation["total"],
        "accuracy": evaluation["accuracy"],
        "feedback": evaluation["feedback"],
        "category": evaluation["category"],
    }), 201


@quiz_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        limit = int(request.args.get("limit", 10))
        if limit < 1:
            limit = 10
    except (TypeError, ValueError):
        limit = 10

    # Ordered by score descending, then newest attempt (created_at descending)
    attempts = (
        QuizAttempt.query
        .order_by(QuizAttempt.score.desc(), QuizAttempt.created_at.desc(), QuizAttempt.id.desc())
        .limit(limit)
        .all()
    )

    leaderboard = [
        {
            "Rank": rank,
            "Pirate": att.player_name,
            "Score": att.score,
            "Total": att.total_questions,
            "Accuracy": f"{att.score / att.total_questions:.0%}" if att.total_questions > 0 else "0%",
            "created_at": att.created_at.isoformat(),
        }
        for rank, att in enumerate(attempts, start=1)
    ]

    return jsonify({"leaderboard": leaderboard}), 200
