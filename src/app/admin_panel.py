from datetime import datetime, timedelta

import jwt
from sqladmin import Admin, ModelView
from src.db.models import Post
from fastapi import Request, Form, APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.status import HTTP_302_FOUND
from src.config.config import ADMIN_PASSWORD, ADMIN_LOGIN, SECRET_KEY, ALGORITHM
from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key, algorithm):
        super().__init__(secret_key)
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def authenticate(self, request: Request):
        token = request.cookies.get("access_token")  # токен храним в куках

        if not token:
            return RedirectResponse(url="/admin/login", status_code=302)

        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            return False

        return True


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.header, Post.text]
    name = "Post"
    name_plural = "Posts"
    icon = "fa fa-pen"


admin_router = APIRouter()


@admin_router.get("/admin/login")
def login_form():
    return HTMLResponse(
        """
        <form method="post">
            <input name="username" />
            <input type="password" name="password" />
            <button type="submit">Login</button>
        </form>
    """
    )


@admin_router.post("/admin/login")
def login_post(username: str = Form(), password: str = Form()):
    if username == ADMIN_LOGIN and password == ADMIN_PASSWORD:
        expire = datetime.utcnow() + timedelta(hours=1)
        to_encode = {"sub": str(username), "exp": expire}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=3600
        )
        return response

    return RedirectResponse(url="/admin/login", status_code=302)


@admin_router.get("/admin/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("access_token")
    return response
