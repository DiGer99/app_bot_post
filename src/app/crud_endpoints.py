import logging

from fastapi import Form, APIRouter
from fastapi.params import Depends

from src.db.requests import (
    get_user_db,
    add_post_db,
    get_all_posts_db,
    edit_post_db,
    delete_post_db,
)
from src.reg.registration import verify_token

log = logging.getLogger(__name__)

crud_router = APIRouter(tags=["crud"])
# dependencies=[Depends(verify_token)]


@crud_router.post("/add")
def add_post(
    user_id: int = Depends(verify_token), header: str = Form(), body: str = Form()
):
    user = get_user_db(user_id=user_id)
    add_post_db(
        header=header,
        body=body,
        user=user,
    )
    return {"message": "post added"}


@crud_router.get("/get")
def get_posts(user_id: int = Depends(verify_token)):
    return get_all_posts_db(user_id=user_id)


@crud_router.put("/edit")
def edit_post(
    user_id: int = Depends(verify_token), header=Form(), body=Form(), post_id=Form()
):
    edit_post_db(user_id=user_id, header=header, body=body, post_id=post_id)
    return {"message": "post updated"}


@crud_router.delete("/delete")
def delete_post(
    post_id: int,
    user_id: int = Depends(verify_token),
):
    delete_post_db(user_id=user_id, post_id=post_id)
    return {"message": "post successfully deleted"}
