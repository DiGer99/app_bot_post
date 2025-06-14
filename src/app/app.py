from fastapi import FastAPI

from src.app.admin_panel import PostAdmin, admin_router
from src.app.crud_endpoints import crud_router
from src.db.models import engine, db_main
from src.config.config import SECRET_KEY, ALGORITHM
from src.reg.registration import reg_router
from src.app.admin_panel import AdminAuth

import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin


app = FastAPI()
app.include_router(reg_router)
app.include_router(crud_router)
app.include_router(admin_router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
admin = Admin(app, engine, authentication_backend=AdminAuth(SECRET_KEY, ALGORITHM))
admin.add_view(PostAdmin)


def main():
    db_main()
    uvicorn.run(app=app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()