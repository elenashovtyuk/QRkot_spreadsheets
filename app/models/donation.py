from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import InvestBaseModel


class Donation(InvestBaseModel):
    """Модель пожертвований."""
    user_id = Column(
        Integer,
        ForeignKey('user.id')
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Сделано пожертвование {self.full_amount} '
            f'и оставлен комментарий {self.comment}'
        )
