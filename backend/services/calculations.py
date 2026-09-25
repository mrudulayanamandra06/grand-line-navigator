import datetime as dt
from typing import Any
from backend.services.seed_data import (
    BOUNTY_REWARDS,
    FACTION_UNITS,
    QUIZ_QUESTIONS,
)


def calculate_catch_up(current_episode: int, episodes_per_day: int, total_episodes: int = 1165) -> dict[str, Any]:
    """Calculate remaining episodes, days, completion date, and percentage."""
    if not isinstance(current_episode, int) or current_episode < 1 or current_episode > total_episodes:
        raise ValueError(f"Current episode must be an integer between 1 and {total_episodes}.")
    if not isinstance(episodes_per_day, int) or episodes_per_day < 1:
        raise ValueError("Episodes per day must be an integer greater than or equal to 1.")

    remaining = max(0, total_episodes - current_episode)
    days = (remaining + episodes_per_day - 1) // episodes_per_day
    completion_date = dt.date.today() + dt.timedelta(days=days)
    completion_percentage = min(float(current_episode) / total_episodes, 1.0)

    return {
        "current_episode": current_episode,
        "episodes_per_day": episodes_per_day,
        "total_episodes": total_episodes,
        "episodes_remaining": remaining,
        "estimated_days": days,
        "estimated_completion_date": completion_date.strftime("%d %B %Y"),
        "completion_percentage": completion_percentage,
    }


def evaluate_quiz(answers: dict[str | int, str]) -> dict[str, Any]:
    """Score quiz answers against the authoritative question bank."""
    if not isinstance(answers, dict):
        raise ValueError("Answers must be provided as a dictionary mapping question IDs to answers.")

    score = 0
    total = len(QUIZ_QUESTIONS)

    for index, question in enumerate(QUIZ_QUESTIONS, start=1):
        q_id_str = str(question.get("id", index))
        submitted_answer = answers.get(q_id_str)
        if submitted_answer is None:
            submitted_answer = answers.get(index)
        if submitted_answer is None:
            submitted_answer = answers.get(str(index))

        if submitted_answer == question["answer"]:
            score += 1

    accuracy = score / total if total > 0 else 0.0

    if score == total:
        feedback = "Perfect score! You are ready for the New World."
        category = "perfect"
    elif score >= 3:
        feedback = "Strong showing, captain. A little more training and you will conquer the Grand Line."
        category = "strong"
    else:
        feedback = "Keep exploring the dashboard and try again to improve your score."
        category = "training"

    return {
        "score": score,
        "total": total,
        "accuracy": accuracy,
        "feedback": feedback,
        "category": category,
    }


def calculate_bounty_milestones(selected_achievements: list[str]) -> dict[str, Any]:
    """Calculate bounty total, rank progression, and milestone percentages."""
    valid_achievements = {item["achievement"] for item in BOUNTY_REWARDS}
    for ach in selected_achievements:
        if ach not in valid_achievements:
            raise ValueError(f"Unknown achievement: '{ach}'")

    reward_total = sum(
        item["reward"] for item in BOUNTY_REWARDS if item["achievement"] in selected_achievements
    )
    maximum_bounty = sum(item["reward"] for item in BOUNTY_REWARDS)

    rank_thresholds = [
        (1_000_000_000, "Yonko-level threat"),
        (500_000_000, "New World supernova"),
        (150_000_000, "Notorious pirate"),
        (0, "Rising rookie"),
    ]

    rank = next(label for threshold, label in rank_thresholds if reward_total >= threshold)
    higher_thresholds = [
        (threshold, label)
        for threshold, label in reversed(rank_thresholds[:-1])
        if threshold > reward_total
    ]
    next_threshold, next_rank = (
        higher_thresholds[0] if higher_thresholds else (maximum_bounty, "Legendary ceiling")
    )
    berries_to_next_rank = max(0, next_threshold - reward_total)
    progress_percentage = min(reward_total / maximum_bounty, 1.0) if maximum_bounty > 0 else 0.0

    return {
        "total_bounty": reward_total,
        "threat_classification": rank,
        "next_rank": next_rank,
        "amount_needed_for_next_rank": berries_to_next_rank,
        "progress_percentage": progress_percentage,
        "maximum_bounty": maximum_bounty,
    }


def calculate_readiness(power: int, defense: int, speed: int, loyalty: int) -> int:
    """Calculate member readiness as the rounded average of four 0–100 stats."""
    for stat_name, val in [
        ("power", power),
        ("defense", defense),
        ("speed", speed),
        ("loyalty", loyalty),
    ]:
        if not isinstance(val, int) or val < 0 or val > 100:
            raise ValueError(f"Stat '{stat_name}' must be an integer between 0 and 100.")
    return round((power + defense + speed + loyalty) / 4)


def simulate_battle(pirate_unit_names: list[str], marine_unit_names: list[str]) -> dict[str, Any]:
    """Execute deterministic faction battle simulation."""
    all_pirate_names = {u["name"] for u in FACTION_UNITS["Pirates"]}
    all_marine_names = {u["name"] for u in FACTION_UNITS["Marines"]}

    for name in pirate_unit_names:
        if name not in all_pirate_names:
            raise ValueError(f"Unknown Pirate unit: '{name}'")
    for name in marine_unit_names:
        if name not in all_marine_names:
            raise ValueError(f"Unknown Marine unit: '{name}'")

    pirate_roster = [u for u in FACTION_UNITS["Pirates"] if u["name"] in pirate_unit_names]
    marine_roster = [u for u in FACTION_UNITS["Marines"] if u["name"] in marine_unit_names]

    pirate_score = sum(u["power"] + u["defense"] + u["speed"] for u in pirate_roster)
    marine_score = sum(u["power"] + u["defense"] + u["speed"] for u in marine_roster)

    pirate_score += len(pirate_roster) * 7
    marine_score += len(marine_roster) * 7

    # If the scores are equal, Pirates win (deterministic tie-break rule)
    winner = "Pirates" if pirate_score >= marine_score else "Marines"

    return {
        "pirate_score": pirate_score,
        "marine_score": marine_score,
        "winner": winner,
    }
