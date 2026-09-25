import os
from typing import Any
from dotenv import load_dotenv
import requests

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000").rstrip("/")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "local-user")
DEFAULT_TIMEOUT = (3.0, 5.0)  # (connect timeout, read timeout)

_session = requests.Session()


class APIError(Exception):
    """Custom exception raised when the backend REST API returns an error or is unreachable."""

    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


def _request(method: str, path: str, **kwargs) -> Any:
    url = f"{BACKEND_URL}{path}"
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    try:
        response = _session.request(method, url, **kwargs)
    except requests.exceptions.ConnectionError:
        raise APIError(
            f"Could not connect to backend at {BACKEND_URL}. Ensure the Flask server is running.",
            status_code=None,
            code="connection_refused",
        )
    except requests.exceptions.Timeout:
        raise APIError(
            f"Request to {url} timed out.",
            status_code=None,
            code="timeout",
        )
    except requests.exceptions.RequestException as e:
        raise APIError(
            f"Network error communicating with backend: {str(e)}",
            status_code=None,
            code="network_error",
        )

    try:
        data = response.json()
    except ValueError:
        if response.ok:
            return response.text
        raise APIError(
            f"Backend returned non-JSON response with HTTP {response.status_code}.",
            status_code=response.status_code,
            code="invalid_json",
        )

    if not response.ok:
        error_info = data.get("error", {}) if isinstance(data, dict) else {}
        err_msg = error_info.get("message") or f"Backend request failed with status {response.status_code}."
        err_code = error_info.get("code") or f"http_{response.status_code}"
        raise APIError(err_msg, status_code=response.status_code, code=err_code)

    return data


def check_health() -> bool:
    """Return True if backend is healthy, False otherwise."""
    try:
        data = _request("GET", "/api/health")
        return isinstance(data, dict) and data.get("status") == "ok"
    except APIError:
        return False


def get_arcs() -> dict[str, Any]:
    return _request("GET", "/api/arcs")


def get_characters() -> dict[str, Any]:
    return _request("GET", "/api/characters")


def get_devil_fruits() -> list[dict[str, Any]]:
    return _request("GET", "/api/devil-fruits")


def get_devil_fruit_types() -> dict[str, Any]:
    return _request("GET", "/api/devil-fruit-types")


def get_crew_members() -> dict[str, str]:
    return _request("GET", "/api/crew-members")


def get_factions() -> dict[str, list[dict[str, Any]]]:
    return _request("GET", "/api/factions")


def calculate_catch_up(current_episode: int, episodes_per_day: int) -> dict[str, Any]:
    return _request(
        "POST",
        "/api/catch-up/calculate",
        json={"current_episode": current_episode, "episodes_per_day": episodes_per_day},
    )


def get_favorites(user_id: str = DEFAULT_USER_ID) -> list[str]:
    data = _request("GET", f"/api/users/{user_id}/favorites")
    return data.get("favorites", [])


def add_favorite(fruit_name: str, user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request(
        "POST",
        f"/api/users/{user_id}/favorites",
        json={"fruit_name": fruit_name},
    )


def remove_favorite(fruit_name: str, user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request("DELETE", f"/api/users/{user_id}/favorites/{fruit_name}")


def get_quiz_questions() -> list[dict[str, Any]]:
    return _request("GET", "/api/quiz/questions")


def submit_quiz(player_name: str, answers: dict[str | int, str], user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request(
        "POST",
        "/api/quiz/submit",
        json={"player_name": player_name, "answers": answers, "user_id": user_id},
    )


def get_quiz_leaderboard(limit: int = 10) -> list[dict[str, Any]]:
    data = _request("GET", f"/api/quiz/leaderboard?limit={limit}")
    return data.get("leaderboard", [])


def get_bounty_rewards() -> list[dict[str, Any]]:
    return _request("GET", "/api/bounty/rewards")


def calculate_bounty(selected_achievements: list[str]) -> dict[str, Any]:
    return _request(
        "POST",
        "/api/bounty/calculate",
        json={"selected_achievements": selected_achievements},
    )


def get_claimed_rewards(user_id: str = DEFAULT_USER_ID) -> list[str]:
    data = _request("GET", f"/api/users/{user_id}/rewards")
    return data.get("claimed_rewards", [])


def claim_rewards(achievements: list[str], user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request(
        "POST",
        f"/api/users/{user_id}/rewards/claim",
        json={"achievements": achievements},
    )


def reset_claimed_rewards(user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request("DELETE", f"/api/users/{user_id}/rewards")


def get_saved_crew(user_id: str = DEFAULT_USER_ID) -> dict[str, Any] | None:
    data = _request("GET", f"/api/users/{user_id}/crew")
    return data.get("crew")


def save_crew(crew_data: dict[str, Any], user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request(
        "PUT",
        f"/api/users/{user_id}/crew",
        json=crew_data,
    )


def delete_saved_crew(user_id: str = DEFAULT_USER_ID) -> dict[str, Any]:
    return _request("DELETE", f"/api/users/{user_id}/crew")


def simulate_battle(
    pirate_units: list[str], marine_units: list[str], user_id: str = DEFAULT_USER_ID
) -> dict[str, Any]:
    return _request(
        "POST",
        "/api/battles/simulate",
        json={
            "user_id": user_id,
            "pirate_units": pirate_units,
            "marine_units": marine_units,
        },
    )


def get_user_battles(limit: int = 10, user_id: str = DEFAULT_USER_ID) -> list[dict[str, Any]]:
    data = _request("GET", f"/api/users/{user_id}/battles?limit={limit}")
    return data.get("battles", [])
