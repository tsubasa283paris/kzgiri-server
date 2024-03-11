from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from routers.json_response import json_response
from sql_interface import crud
from sql_interface.database import get_db


router = APIRouter()


@router.get("/themes/{theme_id}/answers")
def read_answers(
    theme_id: int,
    db: Session = Depends(get_db),
):
    db_theme = crud.get_theme(db, theme_id)

    if db_theme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified theme does not exist."
        )

    get_answers_result = crud.get_answers(db, theme_id)

    answers = []
    for db_answer in get_answers_result.answers:
        answers.append({
            "id": db_answer.id,
            "text": db_answer.text,
            "userName": db_answer.user_name,
            "createdAt": db_answer.created_at,
        })
    
    answers.sort(key=lambda x: x["createdAt"], reverse=True)

    return json_response({
        "answersCountAll": get_answers_result.answers_count,
        "answers": answers,
    })


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
        "themeId": created_answer.theme_id,
    })

