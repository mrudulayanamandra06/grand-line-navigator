from datetime import datetime, timezone
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


def utc_now():
    return datetime.now(timezone.utc)


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(64), unique=True, nullable=False, default="local-user")
    display_name = db.Column(db.String(100), nullable=False, default="Local Captain")
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    favorite_fruits = db.relationship("FavoriteFruit", backref="user", cascade="all, delete-orphan", lazy=True)
    quiz_attempts = db.relationship("QuizAttempt", backref="user", cascade="all, delete-orphan", lazy=True)
    claimed_rewards = db.relationship("ClaimedReward", backref="user", cascade="all, delete-orphan", lazy=True)
    saved_crew = db.relationship("SavedCrew", backref="user", uselist=False, cascade="all, delete-orphan", lazy=True)
    battle_results = db.relationship("BattleResult", backref="user", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "display_name": self.display_name,
            "created_at": self.created_at.isoformat(),
        }


class FavoriteFruit(db.Model):
    __tablename__ = "favorite_fruits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"), nullable=False)
    fruit_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    __table_args__ = (
        UniqueConstraint("user_id", "fruit_name", name="uq_user_favorite_fruit"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "fruit_name": self.fruit_name,
            "created_at": self.created_at.isoformat(),
        }


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"), nullable=True)
    player_name = db.Column(db.String(100), nullable=False, default="Anonymous Captain")
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "player_name": self.player_name,
            "score": self.score,
            "total_questions": self.total_questions,
            "created_at": self.created_at.isoformat(),
        }


class ClaimedReward(db.Model):
    __tablename__ = "claimed_rewards"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"), nullable=False)
    achievement = db.Column(db.String(150), nullable=False)
    reward = db.Column(db.BigInteger, nullable=False)
    claimed_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    __table_args__ = (
        UniqueConstraint("user_id", "achievement", name="uq_user_achievement"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "achievement": self.achievement,
            "reward": self.reward,
            "claimed_at": self.claimed_at.isoformat(),
        }


class SavedCrew(db.Model):
    __tablename__ = "saved_crews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"), unique=True, nullable=False)
    crew_name = db.Column(db.String(100), nullable=False)
    captain = db.Column(db.String(100), nullable=False)
    members = db.Column(db.JSON, nullable=False)
    member_stats = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "crew_name": self.crew_name,
            "captain": self.captain,
            "members": self.members if isinstance(self.members, list) else json.loads(self.members or "[]"),
            "member_stats": self.member_stats if isinstance(self.member_stats, dict) else json.loads(self.member_stats or "{}"),
            "updated_at": self.updated_at.isoformat(),
        }


class BattleResult(db.Model):
    __tablename__ = "battle_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_profiles.id"), nullable=True)
    pirate_units = db.Column(db.JSON, nullable=False)
    marine_units = db.Column(db.JSON, nullable=False)
    pirate_score = db.Column(db.Integer, nullable=False)
    marine_score = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "pirate_units": self.pirate_units if isinstance(self.pirate_units, list) else json.loads(self.pirate_units or "[]"),
            "marine_units": self.marine_units if isinstance(self.marine_units, list) else json.loads(self.marine_units or "[]"),
            "pirate_score": self.pirate_score,
            "marine_score": self.marine_score,
            "winner": self.winner,
            "created_at": self.created_at.isoformat(),
        }


def get_or_create_user(external_id="local-user", display_name="Local Captain") -> UserProfile:
    """Ensure a user profile exists for the given external_id."""
    user = UserProfile.query.filter_by(external_id=external_id).first()
    if not user:
        user = UserProfile(external_id=external_id, display_name=display_name)
        db.session.add(user)
        db.session.commit()
    return user
