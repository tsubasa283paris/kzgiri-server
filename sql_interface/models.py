from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import functions

from .database import Base


# ----------------------------------------------------------------
# definition of common columns as Mixin
# ----------------------------------------------------------------

# createdAt and updatedAt
class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(True),
            default=functions.now(),
            nullable=False
        )
    
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(True),
            default=functions.now(),
            onupdate=functions.now(),
            nullable=False
        )


# ----------------------------------------------------------------
# definition of tables
# ----------------------------------------------------------------

class Theme(Base, TimestampMixin):
    __tablename__ = "theme"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    text = Column(
        String(256),
    )

    released_at = Column(
        DateTime(True),
        default=None,
        nullable=True,
    )

    answers = relationship("Answer", back_populates="theme")


class Answer(Base, TimestampMixin):
    __tablename__ = "answer"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    text = Column(
        String(256),
    )

    user_name = Column(
        String(128),
    )

    theme_id = Column(
        ForeignKey("theme.id", ondelete="CASCADE"),
    )

    theme = relationship("Theme", back_populates="answers")
