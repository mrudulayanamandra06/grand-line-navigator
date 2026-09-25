def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "grand-line-navigator-api"


def test_catalog_endpoints(client):
    for endpoint in [
        "/api/arcs",
        "/api/characters",
        "/api/devil-fruits",
        "/api/devil-fruit-types",
        "/api/crew-members",
        "/api/factions",
    ]:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Endpoint {endpoint} failed"


def test_catch_up_calculator_valid(client):
    res = client.post(
        "/api/catch-up/calculate",
        json={"current_episode": 100, "episodes_per_day": 5},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["episodes_remaining"] == 1065
    assert data["estimated_days"] == 213
    assert "estimated_completion_date" in data
    assert 0 < data["completion_percentage"] < 1.0


def test_catch_up_calculator_invalid_payload(client):
    # Missing fields
    res = client.post("/api/catch-up/calculate", json={"current_episode": 100})
    assert res.status_code == 400
    assert "error" in res.get_json()

    # Out of range episode
    res = client.post(
        "/api/catch-up/calculate",
        json={"current_episode": 2000, "episodes_per_day": 3},
    )
    assert res.status_code == 422
    assert "error" in res.get_json()

    # Negative episodes per day
    res = client.post(
        "/api/catch-up/calculate",
        json={"current_episode": 50, "episodes_per_day": 0},
    )
    assert res.status_code == 422
    assert "error" in res.get_json()
