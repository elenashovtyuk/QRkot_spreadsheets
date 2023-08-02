from fastapi_users import schemas
# создаем 3 схемы, наследующиеся от классов библиотеки FastAPI Users

# schemas.BaseUser[int] - схема с базовыми полями модели пользователя.
# в квадратных скобках укажем тип данных для id пользователя

# schemas.BaseUserCreate - схема для создания пользователя.
# в нее обязательно должны быть переданы email и password

# schemas.BaseUserUpdate - схема для обновления объекта пользователя
# все поля опциональны


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
