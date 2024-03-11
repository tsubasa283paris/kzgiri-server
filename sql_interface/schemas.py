import datetime
from typing import List

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


# ----------------------------------------------------------------
# common fields
# ----------------------------------------------------------------

class CommonRead(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime


# ----------------------------------------------------------------
# theme
# ----------------------------------------------------------------

class ThemeBase(BaseModel):
    id: int
    text: str
    released_at: datetime.datetime

    class Config:
        orm_mode = True


class ThemeRead(ThemeBase, CommonRead):
    pass


class ThemeReadDeep(ThemeRead):
    answers: "List[AnswerRead]"


class ThemeWrite(ThemeBase):
    released_at: datetime.datetime

    class Config:
        alias_generator = to_camel


# ----------------------------------------------------------------
# answer
# ----------------------------------------------------------------

class AnswerBase(BaseModel):
    text: str
    user_name: str

    class Config:
        orm_mode = True


class AnswerRead(AnswerBase, CommonRead):
    id: int


class AnswerWrite(AnswerBase):
    theme_id: int

    class Config:
        alias_generator = to_camel


# ----------------------------------------------------------------
# update forward references
# ----------------------------------------------------------------
ThemeReadDeep.model_rebuild()
