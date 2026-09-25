import time


def test_quiz_answers_not_in_questions_response(client):
    res = client.get("/api/quiz/questions")
    assert res.status_code == 200
    questions = res.get_json()
    assert len(questions) == 10
    for q in questions:
        assert "question" in q
        assert "options" in q
        assert "answer" not in q, f"Security violation: Correct answer exposed in question {q}"


def test_quiz_scoring_all_correct(client):
    answers = {
        "1": "Monkey D. Luffy",
        "2": "Mera Mera no Mi",
        "3": "Kaido",
        "4": "Thousand Sunny",
        "5": "Roronoa Zoro",
        "6": "Nami",
        "7": "Gomu Gomu",
        "8": "Water 7 / Enies Lobby",
        "9": "Tony Tony Chopper",
        "10": "Logia",
    }
    res = client.post(
        "/api/quiz/submit",
        json={"player_name": "Pirate King", "answers": answers},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["score"] == 10
    assert data["total"] == 10
    assert data["category"] == "perfect"


def test_quiz_scoring_partial_and_feedback(client):
    answers = {
        "1": "Monkey D. Luffy",
        "2": "Mera Mera no Mi",
        "3": "Kaido",
        "4": "Wrong Ship",
        "5": "Wrong Swordsman",
    }
    res = client.post(
        "/api/quiz/submit",
        json={"player_name": "Rookie", "answers": answers},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["score"] == 3
    assert data["category"] == "strong"


def test_leaderboard_ordering(client):
    # Submit lower score first
    client.post(
        "/api/quiz/submit",
        json={"player_name": "Captain Low", "answers": {"1": "Monkey D. Luffy"}},
    )

    # Submit higher score next
    client.post(
        "/api/quiz/submit",
        json={
            "player_name": "Captain High",
            "answers": {
                "1": "Monkey D. Luffy",
                "2": "Mera Mera no Mi",
                "3": "Kaido",
            },
        },
    )

    # Submit medium score next
    client.post(
        "/api/quiz/submit",
        json={
            "player_name": "Captain Mid",
            "answers": {
                "1": "Monkey D. Luffy",
                "2": "Mera Mera no Mi",
            },
        },
    )

    res = client.get("/api/quiz/leaderboard?limit=10")
    assert res.status_code == 200
    leaderboard = res.get_json()["leaderboard"]
    assert len(leaderboard) >= 3
    # Check descending score order
    scores = [entry["Score"] for entry in leaderboard]
    assert scores == sorted(scores, reverse=True)
    assert leaderboard[0]["Pirate"] == "Captain High"
    assert leaderboard[0]["Score"] == 3
