from sqladmin import Admin, ModelView
from src.db.models import Post
from fastapi import Request, Form, APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.status import HTTP_302_FOUND
from src.config.config import ADMIN_PASSWORD, ADMIN_LOGIN
from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if request.session.get("admin_logged_in"):
            return True
        return RedirectResponse(url="/admin/login")


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.header, Post.text]
    name = "Post"
    name_plural = "Posts"
    icon = "fa fa-pen"


admin_router = APIRouter()


@admin_router.get("/admin/login")
def login_form():
    return HTMLResponse("""
        <form method="post">
            <input name="username" />
            <input type="password" name="password" />
            <button type="submit">Login</button>
        </form>
    """)


@admin_router.post("/admin/login")
def login_post(request: Request, username: str = Form(), password: str = Form()):
    if username == ADMIN_LOGIN and password == ADMIN_PASSWORD:
        request.session["admin_logged_in"] = True
        return RedirectResponse("/admin", status_code=HTTP_302_FOUND)
    return HTMLResponse("Invalid credentials", status_code=401)


