from fastapi import FastAPI, Form
from src.db.requests import (
    add_post_db,
    get_all_posts_db,
    edit_post_db,
    delete_post_db
)
from src.reg.registration import reg_router
import uvicorn

app = FastAPI()
app.include_router(reg_router)


@app.post("/add")
def add_post(
        header=Form(),
        body=Form()
):
    add_post_db(header=header, body=body)
    return {"message": "post added"}


@app.get("/get")
def get_posts():
    return get_all_posts_db()


@app.post("/edit")
def edit_post(
        header=Form(),
        body=Form(),
        post_id=Form()
):
    edit_post_db(
        header=header,
        body=body,
        post_id=post_id
    )

    return {"message": "post updated"}


@app.post("/delete")
def delete_post(post_id: int):
    delete_post_db(post_id=post_id)
    return {"message": "post successfully deleted"}


if __name__ == "__main__":
    uvicorn.run(app=app, reload=True)
