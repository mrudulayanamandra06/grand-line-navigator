from backend.services.calculations import simulate_battle


def test_deterministic_battle_scoring(client):
    payload = {
        "user_id": "battle-user-1",
        "pirate_units": ["Straw Hat Captain", "Three-Sword Swordsman"],
        "marine_units": ["Fleet Admiral", "Admiral of Light"],
    }
    # Calculation:
    # Pirate: (96+82+94) + (91+88+83) + 2*7 = 272 + 262 + 14 = 548
    # Marine: (95+91+76) + (92+79+99) + 2*7 = 262 + 270 + 14 = 546
    res = client.post("/api/battles/simulate", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["pirate_score"] == 548
    assert data["marine_score"] == 546
    assert data["winner"] == "Pirates"
    assert "id" in data


def test_pirates_win_on_tie(client):
    # Test service level tie condition directly
    # Even if pirate_score == marine_score, Pirates win
    from unittest.mock import patch

    # Mock FACTION_UNITS or unit lookups to return identical scores
    equal_units = {
        "Pirates": [{"name": "P1", "power": 10, "defense": 10, "speed": 10}],
        "Marines": [{"name": "M1", "power": 10, "defense": 10, "speed": 10}],
    }
    with patch("backend.services.calculations.FACTION_UNITS", equal_units):
        outcome = simulate_battle(["P1"], ["M1"])
        assert outcome["pirate_score"] == 37  # 30 + 7
        assert outcome["marine_score"] == 37  # 30 + 7
        assert outcome["winner"] == "Pirates"


def test_battle_persistence_and_history(client):
    user_id = "battle-history-user"
    client.post(
        "/api/battles/simulate",
        json={
            "user_id": user_id,
            "pirate_units": ["Straw Hat Captain"],
            "marine_units": ["Marine Strategist"],
        },
    )

    res = client.get(f"/api/users/{user_id}/battles?limit=10")
    assert res.status_code == 200
    battles = res.get_json()["battles"]
    assert len(battles) == 1
    assert battles[0]["winner"] == "Pirates"
    assert battles[0]["pirate_units"] == ["Straw Hat Captain"]


def test_reject_unknown_faction_unit(client):
    res = client.post(
        "/api/battles/simulate",
        json={
            "pirate_units": ["Fake Pirate Unit"],
            "marine_units": ["Fleet Admiral"],
        },
    )
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "unknown_unit"
