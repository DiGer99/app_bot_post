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
engine = create_engine(url)


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(30))
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")


Base.metadata.create_all(bind=engine)