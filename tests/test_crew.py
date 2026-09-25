def test_crew_persistence_and_retrieval(client):
    user_id = "captain-luffy"

    # Initially None
    res = client.get(f"/api/users/{user_id}/crew")
    assert res.status_code == 200
    assert res.get_json()["crew"] is None

    # Save a valid crew
    payload = {
        "crew_name": "Straw Hat Pirates",
        "captain": "Monkey D. Luffy",
        "members": ["Roronoa Zoro", "Nami", "Vinsmoke Sanji"],
        "member_stats": {
            "Monkey D. Luffy": {"power": 95, "defense": 85, "speed": 90, "loyalty": 100},
            "Roronoa Zoro": {"power": 92, "defense": 88, "speed": 82, "loyalty": 98},
        },
    }
    res = client.put(f"/api/users/{user_id}/crew", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["crew"]["crew_name"] == "Straw Hat Pirates"
    assert data["crew"]["captain"] == "Monkey D. Luffy"
    assert len(data["crew"]["members"]) == 3

    # Retrieve and verify persistence
    res = client.get(f"/api/users/{user_id}/crew")
    assert res.status_code == 200
    crew = res.get_json()["crew"]
    assert crew is not None
    assert crew["captain"] == "Monkey D. Luffy"
    assert "Roronoa Zoro" in crew["members"]
    assert crew["member_stats"]["Monkey D. Luffy"]["power"] == 95


def test_crew_validation_captain_in_members(client):
    user_id = "test-crew-err-1"
    payload = {
        "crew_name": "Test Crew",
        "captain": "Monkey D. Luffy",
        "members": ["Monkey D. Luffy", "Zoro"],
    }
    res = client.put(f"/api/users/{user_id}/crew", json=payload)
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "captain_in_members"


def test_crew_validation_duplicate_members(client):
    user_id = "test-crew-err-2"
    payload = {
        "crew_name": "Test Crew",
        "captain": "Monkey D. Luffy",
        "members": ["Nami", "Nami"],
    }
    res = client.put(f"/api/users/{user_id}/crew", json=payload)
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "duplicate_members"


def test_crew_validation_too_many_members(client):
    user_id = "test-crew-err-3"
    # 10 members + 1 captain = 11 total (exceeds maximum 9 additional members)
    payload = {
        "crew_name": "Test Crew",
        "captain": "Monkey D. Luffy",
        "members": [
            "Roronoa Zoro", "Nami", "Usopp", "Vinsmoke Sanji",
            "Tony Tony Chopper", "Nico Robin", "Franky", "Brook",
            "Jinbe", "Shanks"
        ],
    }
    res = client.put(f"/api/users/{user_id}/crew", json=payload)
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "too_many_members"


def test_crew_validation_invalid_stats_range(client):
    user_id = "test-crew-err-4"
    payload = {
        "crew_name": "Test Crew",
        "captain": "Monkey D. Luffy",
        "members": ["Roronoa Zoro"],
        "member_stats": {
            "Roronoa Zoro": {"power": 150, "defense": 70, "speed": 70, "loyalty": 70},
        },
    }
    res = client.put(f"/api/users/{user_id}/crew", json=payload)
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "invalid_stat_value"
