from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from routers.json_response import json_response
from sql_interface import crud
from sql_interface.database import get_db


router = APIRouter()


class CreateAnswerReqParams(BaseModel):
    text: str
    user_name: str

    class Config:
        alias_generator = to_camel


@router.post("/themes/{theme_id}/answers")
def create_answer(
    theme_id: int,
    params: CreateAnswerReqParams,
    db: Session = Depends(get_db),
):
    db_theme = crud.get_theme(db, theme_id)

    if db_theme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified theme does not exist."
        )
    
    created_answer = crud.create_answer(db, params.text,
                                        params.user_name, theme_id)

    return json_response({
        "id": created_answer.id,
        "text": created_answer.text,
        "userName": created_answer.user_name,
        "likes": created_answer.likes,
        "themeId": created_answer.theme_id,
    })


class IncrementAnswerLikesReqParams(BaseModel):
    increment: int

    class Config:
        alias_generator = to_camel


@router.post("/answers/{answer_id}/likes")
def increment_answer_likes(
    answer_id: int,
    params: IncrementAnswerLikesReqParams,
    db: Session = Depends(get_db),
):
    db_answer = crud.get_answer(db, answer_id)

    if db_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified answer does not exist."
        )
    
    updated_answer = crud.increment_answer_likes(db, answer_id,
                                                params.increment)

    return json_response({
        "id": updated_answer.id,
        "text": updated_answer.text,
        "userName": updated_answer.user_name,
        "likes": updated_answer.likes,
        "themeId": updated_answer.theme_id,
    })

