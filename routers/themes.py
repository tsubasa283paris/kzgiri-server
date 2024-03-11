import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from routers.json_response import json_response
from sql_interface import crud
from sql_interface.database import get_db


router = APIRouter()


@router.get("/themes/{theme_id}")
def read_theme(
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
            "likes": db_answer.likes,
            "createdAt": db_answer.created_at,
        })
    
    answers.sort(key=lambda x: x["createdAt"])

    return json_response({
        "id": db_theme.id,
        "text": db_theme.text,
        "releasedAt": db_theme.released_at,
        "answers": answers
    })


@router.get("/themes")
def read_themes(
    db: Session = Depends(get_db),
):
    get_themes_result = crud.get_themes(db)

    themes = []
    for db_theme in get_themes_result.themes:
        themes.append({
            "id": db_theme.id,
            "text": db_theme.text,
            "releasedAt": db_theme.released_at,
            "createdAt": db_theme.created_at,
        })
    themes.sort(key=lambda x: x["createdAt"], reverse=True)
    return json_response({
        "themesCountAll": get_themes_result.themes_count,
        "themes": themes,
    })


class CreateThemeReqParams(BaseModel):
    text: str
    released_at: str

    class Config:
        alias_generator = to_camel


@router.post("/themes")
def create_themes(
    params: CreateThemeReqParams,
    db: Session = Depends(get_db),
):
    released_at = datetime.datetime.fromisoformat(params.released_at)
    created_theme = crud.create_theme(db, params.text, released_at)

    return json_response({
        "id": created_theme.id,
        "text": created_theme.text,
        "releasedAt": created_theme.released_at,
    })
