def test_bounty_calculation_tiers(client):
    # Rising rookie (0 - 150M)
    res = client.post(
        "/api/bounty/calculate",
        json={"selected_achievements": ["Complete an East Blue arc"]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_bounty"] == 30_000_000
    assert data["threat_classification"] == "Rising rookie"
    assert data["next_rank"] == "Notorious pirate"
    assert data["amount_needed_for_next_rank"] == 120_000_000

    # Notorious pirate (150M - 500M)
    res = client.post(
        "/api/bounty/calculate",
        json={"selected_achievements": ["Defeat a Warlord-level opponent"]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_bounty"] == 150_000_000
    assert data["threat_classification"] == "Notorious pirate"

    # Yonko-level threat (>= 1B)
    res = client.post(
        "/api/bounty/calculate",
        json={"selected_achievements": ["Liberate a country from a Yonko"]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_bounty"] == 1_000_000_000
    assert data["threat_classification"] == "Yonko-level threat"


def test_bounty_claim_and_reset(client):
    user_id = "test-bounty-user"

    # Initially empty
    res = client.get(f"/api/users/{user_id}/rewards")
    assert res.status_code == 200
    assert res.get_json()["claimed_rewards"] == []

    # Claim one reward
    res = client.post(
        f"/api/users/{user_id}/rewards/claim",
        json={"achievements": ["Complete an East Blue arc"]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "Complete an East Blue arc" in data["claimed_rewards"]
    assert data["newly_claimed_count"] == 1

    # Claim duplicate - should not duplicate
    res = client.post(
        f"/api/users/{user_id}/rewards/claim",
        json={"achievements": ["Complete an East Blue arc", "Defeat a Warlord-level opponent"]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["claimed_rewards"]) == 2
    assert data["newly_claimed_count"] == 1

    # Reset
    res = client.delete(f"/api/users/{user_id}/rewards")
    assert res.status_code == 200
    assert res.get_json()["claimed_rewards"] == []

    # Verify reset survived
    res = client.get(f"/api/users/{user_id}/rewards")
    assert res.status_code == 200
    assert res.get_json()["claimed_rewards"] == []


def test_reject_unknown_achievement(client):
    user_id = "test-bounty-user-2"
    res = client.post(
        f"/api/users/{user_id}/rewards/claim",
        json={"achievements": ["Become Hokage"]},
    )
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "unknown_achievement"
