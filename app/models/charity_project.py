from sqlalchemy import Column, String, Text

from .base import InvestBaseModel
from app.constants import MAX_LENGTH


class CharityProject(InvestBaseModel):
    """Модель проектов для пожертвований."""
    name = Column(String(MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
