from datetime import datetime, UTC
from typing import List

from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

url = "sqlite:///users_posts.db"
engine = create_engine(
    url=url
)


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(30))
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    bind_tg_code: Mapped[str] = mapped_column(unique=True, nullable=True)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")


def db_main():
    Base.metadata.create_all(bind=engine)
