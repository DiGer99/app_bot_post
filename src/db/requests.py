from fastapi import HTTPException
from starlette import status

from src.db.models import engine, Post, User
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from src.schemes.schemes import UserSchema
from src.reg.utils import validate_password


def get_session(func):
    def wrapper(*args, **kwargs):
        with Session(bind=engine) as session:
            return func(session, *args, **kwargs)
    return wrapper


@get_session
def add_post_db(session, header: str, body: str, user: User | None = None):
    post = Post(
        header=header,
        text=body,
        user = user
    )
    session.add(post)
    session.commit()


@get_session
def get_all_posts_db(session):
    stmt = select(Post)
    res = [post for post in session.scalars(stmt)]
    return res


@get_session
def edit_post_db(
        session,
        header: str,
        body: str,
        post_id: int
):
    stmt = update(Post).where(Post.id==post_id).values(
        header=header,
        text=body
    )
    session.execute(stmt)
    session.commit()


@get_session
def delete_post_db(session, post_id: int):
    stmt = delete(Post).where(Post.id==post_id)
    session.execute(stmt)
    session.commit()


@get_session
def add_new_user_login_pwd(session, user: User):
    session.add(user)
    session.commit()


@get_session
def authenticate_user(
        session: Session,
        login: str,
        password: str
):
    stmt = select(User).where(User.login == login)
    user = session.execute(stmt).scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user do not registered"
        )
    if not validate_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error"
        )
    return user


@get_session
def get_user_db(
        session: Session,
        user_id: int
):
    stmt = select(User).where(User.id==user_id)
    user = session.execute(stmt).scalar()
    return user
