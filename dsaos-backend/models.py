from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    codeforces_handle = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    solved_problems = relationship(
        "UserSolvedProblem",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)
    tags = Column(JSON, nullable=True)
    contest_id = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class UserSolvedProblem(Base):
    __tablename__ = "user_solved_problems"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    solved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    verdict = Column(String, nullable=False)

    user = relationship("User", back_populates="solved_problems")
    problem = relationship("Problem")


class ContestHistory(Base):
    __tablename__ = "contest_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    contest_id = Column(Integer, nullable=False, index=True)
    contest_name = Column(String, nullable=False)
    rank = Column(Integer, nullable=True)
    old_rating = Column(Integer, nullable=True)
    new_rating = Column(Integer, nullable=True)
    participated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
