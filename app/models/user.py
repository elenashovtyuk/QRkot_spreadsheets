from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


# создадим модель User на основе готовой базовой модели пользователя
# из библиотеки  FastAPI и нашей базовой модели
class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователей."""
    pass
