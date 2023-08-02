from sqlalchemy import Column, Text, Integer, ForeignKey
from .base import InvestBaseModel


class Donation(InvestBaseModel):
    """Модель для пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Сделано пожертвование {self.full_amount} '
            f'и оставлен комментарий {self.comment}'
        )
