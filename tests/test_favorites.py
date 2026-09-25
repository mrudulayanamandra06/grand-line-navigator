def test_save_and_remove_favorite(client):
    user_id = "test-user-1"

    # Initially empty
    res = client.get(f"/api/users/{user_id}/favorites")
    assert res.status_code == 200
    assert res.get_json()["favorites"] == []

    # Add favorite
    res = client.post(
        f"/api/users/{user_id}/favorites",
        json={"fruit_name": "Gomu Gomu no Mi"},
    )
    assert res.status_code == 201

    # Verify saved
    res = client.get(f"/api/users/{user_id}/favorites")
    assert res.status_code == 200
    assert res.get_json()["favorites"] == ["Gomu Gomu no Mi"]

    # Remove favorite
    res = client.delete(f"/api/users/{user_id}/favorites/Gomu Gomu no Mi")
    assert res.status_code == 200

    # Verify empty again
    res = client.get(f"/api/users/{user_id}/favorites")
    assert res.status_code == 200
    assert res.get_json()["favorites"] == []


def test_duplicate_favorite_protection(client):
    user_id = "test-user-2"

    # Add first time
    res = client.post(
        f"/api/users/{user_id}/favorites",
        json={"fruit_name": "Mera Mera no Mi"},
    )
    assert res.status_code == 201

    # Add second time - should be rejected with 409 Conflict
    res = client.post(
        f"/api/users/{user_id}/favorites",
        json={"fruit_name": "Mera Mera no Mi"},
    )
    assert res.status_code == 409
    data = res.get_json()
    assert data["error"]["code"] == "duplicate_favorite"


def test_favorites_survive_new_request(client):
    user_id = "test-user-3"

    # Add multiple favorites
    client.post(f"/api/users/{user_id}/favorites", json={"fruit_name": "Gomu Gomu no Mi"})
    client.post(f"/api/users/{user_id}/favorites", json={"fruit_name": "Ope Ope no Mi"})

    # Separate request checking persistence
    res = client.get(f"/api/users/{user_id}/favorites")
    assert res.status_code == 200
    favorites = res.get_json()["favorites"]
    assert "Gomu Gomu no Mi" in favorites
    assert "Ope Ope no Mi" in favorites
    assert len(favorites) == 2


def test_reject_unknown_fruit(client):
    user_id = "test-user-4"
    res = client.post(
        f"/api/users/{user_id}/favorites",
        json={"fruit_name": "Fake Devil Fruit 9000"},
    )
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "unknown_fruit"
