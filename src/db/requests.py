import random

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
    post = Post(header=header, text=body, user=user)
    session.add(post)
    session.commit()


@get_session
def get_all_posts_db(session):
    stmt = select(Post)
    res = [post for post in session.scalars(stmt)]
    return res


@get_session
def edit_post_db(session, header: str, body: str, post_id: int):
    stmt = update(Post).where(Post.id == post_id).values(header=header, text=body)
    session.execute(stmt)
    session.commit()


@get_session
def delete_post_db(session, post_id: int):
    stmt = delete(Post).where(Post.id == post_id)
    session.execute(stmt)
    session.commit()


@get_session
def add_new_user_login_pwd(session, user: User):
    session.add(user)
    session.commit()


@get_session
def authenticate_user(session: Session, login: str, password: str):
    stmt = select(User).where(User.login == login)
    user = session.execute(stmt).scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="user do not registered"
        )
    if not validate_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token error"
        )
    return user


@get_session
def get_user_db(session: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    user = session.execute(stmt).scalar()
    return user


@get_session
def get_user_db_by_login(session: Session, login: str):
    stmt = select(User).where(User.login == login)
    user = session.execute(stmt).scalar()
    return user


@get_session
def generate_bind_code(session: Session, login: str) -> str:
    code = str(random.randint(100000, 999999))
    user = session.execute(select(User).where(User.login == login))
    user.bind_tg_code = code
    session.commit()
    return code


@get_session
def bind_tg_to_api(session: Session, code: str, tg_id: int):
    user = session.query(User).filter(User.bind_tg_code == code).first()
    if not user:
        return "Код недействителен или не найден"
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="code not found")

    user.tg_id = tg_id
    user.bind_tg_code = None
    session.commit()
    return "Телеграм успешно привязан"


@get_session
def get_user_from_tg_id(session: Session, tg_id: int):
    user = session.execute(select(User).filter(User.tg_id == tg_id)).scalar()
    return user


@get_session
def get_posts_user(session: Session, user_id: int):
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    return posts


@get_session
def get_post_from_header(session: Session, header: str):
    post = session.query(Post).filter(Post.header == header)
    return post
