from sqlalchemy import Column, Integer
# имопртируем функцию для создания базового класса
# для моделей, а также импортируем функцию sessionmaker
# которая позволяет множественно создавать сессии
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
# все классы и функции для асинхронной работы
# находятся в модуле sqlalchemy.ext.asyncio
# импортируем функцию для создания асинхронного движка
# а также класс AsyncSession, с помощью которого создаются
# сессии для асинхронной работы
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.config import settings
# создаем базовый класс для будущих моделей
# применяя функцию declarative_base()


# расширим базовый класс для наших моделей
class PreBase:

    @declared_attr
    def __tablename__(cls):
        # именем таблицы будет название модели в нижнем регистре
        return cls.__name__.lower()
    # во все таблицы будет добавлено поле ID
    id = Column(Integer, primary_key=True)


# создаем базовый класс для наших моделей на основе расширенного
# класса PreBase
Base = declarative_base(cls=PreBase)

# создаем асинхронный движок и в него передаем параметры для подключения к БД
engine = create_async_engine(settings.database_url)

# создаем асинхронную сессию
async_session = AsyncSession(engine)

# указываем переменную, которой будет присвоен класс
# именно поэтому обозначаем ее с большой буквы
# функция sessionmaker возвращает класс сессии
# по сути функция sessionmaker предоставляет фабрику
# сессий(сеансов), связанных с этим движком
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


# Асинхронный генератор сессий.
async def get_async_session():
    # Через асинхронный контекстный менеджер и sessionmaker
    # открывается сессия.
    async with AsyncSessionLocal() as async_session:
        # Генератор с сессией передается в вызывающую функцию.
        yield async_session
        # Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
        # и при выходе из контекстного менеджера сессия будет закрыта.
