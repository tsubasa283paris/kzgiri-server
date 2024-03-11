import datetime
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from . import models, schemas

# ----------------------------------------------------------------
# theme
# ----------------------------------------------------------------

def get_theme(db: Session, id: int):
    return db.query(models.Theme) \
        .filter(
            models.Theme.id == id
        ) \
        .first()


@dataclass
class GetThemes:
    themes: List[models.Theme]
    themes_count: int


def get_themes(db: Session):
    query = db.query(models.Theme)
    total_count = query.count()
    return GetThemes(
        db.query(models.Theme) \
            .all(),
        total_count
    )


def create_theme(db: Session, text: str, released_at: datetime.datetime):
    db_theme = models.Theme(
        text=text,
        released_at=released_at
    )
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme


# ----------------------------------------------------------------
# answer
# ----------------------------------------------------------------

def get_answer(db: Session, id: int):
    db_answer = db.query(models.Answer) \
        .filter(
            models.Answer.id == id
        ) \
        .first()
    return db_answer

@dataclass
class GetAnswers:
    answers: List[models.Answer]
    answers_count: int

def get_answers(
    db: Session, theme_id: int
):
    query = db.query(models.Answer) \
        .filter(
            models.Answer.theme_id == theme_id
        ) \
        .order_by(
            models.Answer.created_at.asc()
        )
    total_count = query.count()
    return GetAnswers(
        query \
            .all(),
        total_count
    )

def create_answer(db: Session, text: str, user_name: str, theme_id: int):
    db_answer = models.Answer(
        text=text,
        user_name=user_name,
        theme_id=theme_id,
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def increment_answer_likes(db: Session, answer_id: int, increment: int):
    db_answer = db.query(models.Answer) \
        .filter(models.Answer.id == answer_id) \
        .first()
    db_answer.likes += increment

    db.commit()

    return db_answer
