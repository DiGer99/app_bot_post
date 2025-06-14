import random
from datetime import timedelta
import jwt
from fastapi import APIRouter, Form, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from fastapi.exceptions import HTTPException
from starlette import status
from fastapi.responses import RedirectResponse

from src.config.config import SECRET_KEY, ALGORITHM
from src.schemes.schemes import UserSchema, Token
from src.reg.utils import hash_password, create_access_token
from src.db.requests import add_new_user_login_pwd, authenticate_user
from src.db.models import User

import logging

log = logging.getLogger(__name__)

reg_router = APIRouter(prefix="/reg", tags=["auth"])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bearer_scheme = HTTPBearer(auto_error=False)


def verify_token(
    # token: str = Depends(oauth2_scheme),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id


@reg_router.post("")
def registration_user(login: str = Form(), password: str = Form()):
    user: UserSchema = UserSchema(login=login, password=password)
    code = str(random.randint(100000, 999999))
    hash_pwd: bytes = hash_password(user.password)
    hashed_user: User = User(
        login=user.login,
        password=hash_pwd,
        bind_tg_code=code
    )
    add_new_user_login_pwd(hashed_user)

    return {
        "code": code,
        "message": "https://t.me/for_post_get_bot"
    }


@reg_router.post("/auth/token")
async def login_for_access_token(
    # user: UserSchema = Depends(authenticate_user),
    login: str = Form(),
    password: str = Form(),
) -> Token:
    user_sch = UserSchema(login=login, password=password)
    user = authenticate_user(user_sch.login, user_sch.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
